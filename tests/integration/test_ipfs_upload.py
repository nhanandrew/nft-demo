from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.create_metadata import upload_to_ipfs
from metadata.sample_metadata import metadata_template
from brownie import network, AdvancedCollectible
import pytest


def can_ipfs_upload():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip
    # Act
    advanced_collectible = AdvancedCollectible[-1]
