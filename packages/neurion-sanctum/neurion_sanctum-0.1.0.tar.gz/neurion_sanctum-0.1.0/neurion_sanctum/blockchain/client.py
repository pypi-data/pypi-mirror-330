from neurionpy.sanctum.interface import SanctumQuery,SanctumMessage
from neurionpy.synapse.client import NeurionClient
from .wallet import get_wallet
from ..setting import get_network


def get_query_client() -> SanctumQuery:
    """Get query client."""
    return NeurionClient(get_network(), get_wallet()).sanctum


def get_message_client() -> SanctumMessage:
    """Get message client."""
    return NeurionClient(get_network(), get_wallet()).sanctum.tx
