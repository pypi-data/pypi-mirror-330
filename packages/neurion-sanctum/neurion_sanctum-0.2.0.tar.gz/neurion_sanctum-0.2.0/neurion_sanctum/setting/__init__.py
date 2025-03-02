import os
from functools import lru_cache

from neurionpy.synapse.config import NetworkConfig

@lru_cache()
def get_network()->NetworkConfig:
    network=os.getenv("NEURION_NETWORK", "alphanet")
    if network.lower() == "mainnet":
        return NetworkConfig.neurion_mainnet()
    elif network.lower() == "alphanet":
        return NetworkConfig.neurion_alpha_testnet()
    elif network.lower() == "betanet":
        return NetworkConfig.neurion_beta_testnet()
    elif network.lower() == "localnet":
        return NetworkConfig.neurion_localnet()
    return NetworkConfig.neurion_alpha_testnet()