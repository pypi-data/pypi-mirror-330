from neurionpy.ganglion.interface import GanglionQuery, GanglionMessage
from neurionpy.synapse.client import NeurionClient
from .wallet import get_wallet
from ..setting import get_network


def get_query_client() -> GanglionQuery:
    """Get query client."""
    return NeurionClient(get_network(), get_wallet()).ganglion


def get_message_client() -> GanglionMessage:
    """Get message client."""
    return NeurionClient(get_network(), get_wallet()).ganglion.tx
