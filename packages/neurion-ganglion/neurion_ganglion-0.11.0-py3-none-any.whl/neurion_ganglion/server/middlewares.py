import os
import time
from fastapi import FastAPI, Request, Response, HTTPException
from typing import Callable, Awaitable

from neurionpy.crypto.keypairs import PublicKey
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from neurion_ganglion.blockchain.query import user_pathway_stake, get_pathway
from neurion_ganglion.db.ion_usage import IonUsageDAO
from neurion_ganglion.db.pathway_usage import PathwayUsageDAO
from neurion_ganglion.utils import str_to_bool

AUTH_TICKET_EXPIRY = 36000  # 10 hour


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for request authentication and subscription fee deduction."""

    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.enable_calls_count = str_to_bool(os.getenv("ENABLE_CALLS_COUNT", "False"))
        self.free_ion_calls = os.getenv("FREE_ION_CALLS", 100000)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            """Middleware logic for authentication and fee deduction."""
            path_segments = request.url.path.strip("/").split("/")
            if request.url.path.startswith("/ion/") or request.url.path.startswith("/pathway/"):
                # Extract authentication headers
                headers = request.headers
                timestamp = headers.get("X-Neurion-Timestamp")
                sender = headers.get("X-Neurion-Sender")
                signature = headers.get("X-Neurion-Signature")

                if not (timestamp and sender and signature):
                    raise HTTPException(status_code=400, detail="Missing authentication headers")

                # Check timestamp validity
                current_time = int(time.time())
                if abs(current_time - int(timestamp)) > AUTH_TICKET_EXPIRY:
                    raise HTTPException(status_code=401, detail="Request expired")

                # Verify signature
                if not self.verify_signature(timestamp, sender, signature):
                    raise HTTPException(status_code=401, detail="Invalid signature")

                # Check subscription balance for sender
                if self.enable_calls_count:
                    if request.url.path.startswith("/ion/"):
                        ion_address = path_segments[1]
                        usage = await IonUsageDAO.get_num_of_calls(ion_address, sender) or 0
                        if usage >= int(self.free_ion_calls):
                            raise HTTPException(status_code=402, detail="Free calls limit exceeded")
                    if request.url.path.startswith("/pathway/"):
                        pathway_id = int(path_segments[1])
                        stake_response=user_pathway_stake(sender,pathway_id)
                        stake=stake_response.stake
                        pathway_response=get_pathway(pathway_id)
                        pathway=pathway_response.pathway
                        fee_per_thousand_calls=pathway.fee_per_thousand_calls or 0

                        calls_pending = await PathwayUsageDAO.get_num_of_calls_pending(pathway_id, sender) or 0
                        needed_stake=calls_pending*fee_per_thousand_calls/1000
                        if stake<needed_stake:
                            raise HTTPException(status_code=402, detail="Insufficient balance")


                # Process the request
                response = await call_next(request)
                print(self.enable_calls_count)
                if self.enable_calls_count:
                    if request.url.path.startswith("/ion/"):
                        ion_address = path_segments[1]
                        await IonUsageDAO.increment_usage(ion_address,sender)
                    if request.url.path.startswith("/pathway/"):
                        pathway_id = int(path_segments[1])
                        await PathwayUsageDAO.increment_calls_pending(pathway_id, sender)

                return response

        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        except Exception as e:
            print(f"Unhandled exception in middleware: {e}")
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})


    def verify_signature(self, timestamp: str, sender: str, signature: str) -> bool:
        """Verifies the authenticity of the request using the sender's public key."""
        try:
            # Recover public key from signature and compare
            recovered_pubkey = PublicKey.from_signature_hex(timestamp, signature)
            return recovered_pubkey.to_address() == sender
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False