import random
import requests

from google.protobuf.json_format import MessageToDict
from neurion_ganglion.blockchain.query import get_allowed_ips, ion_by_ion_address, get_pathway

# ==========================
# Pathway Class
# ==========================

class Pathway:
    def __init__(self, *args, **kwargs):
        """Prevent direct instantiation. Must use `Pathway.of()`."""
        raise RuntimeError("Use `Pathway.of(id)` to create an Pathway.")

    @classmethod
    def of(cls,id: int):
        """
        Pathway to dynamically handle execution tasks.

        Args:
            id (int): ID of the Pathway.
        """
        pathway_response=get_pathway(id)
        pathway=pathway_response.pathway
        pathway_dict = MessageToDict(pathway)
        self = object.__new__(cls)  # Manually create instance
        for key, value in pathway_dict.items():
            setattr(self, key, value)
        return self

    def call(self,body: dict):
        print("Calling Ganglion server...")
        # Get the ganglion server addresss
        ips_response=get_allowed_ips()
        ip=random.choice(ips_response.ips)
        # get the endpoint of the ganglion server
        ganglion_server_endpoint=f"http://{ip}:8000"
        response = requests.post(f"{ganglion_server_endpoint}/pathway/{self.id}", json=body)
        return response.json()