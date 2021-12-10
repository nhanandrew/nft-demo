from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_flavor

flavor_metadata_dict = {
    "SEVERE": "https://ipfs.io/ipfs/QmRTKUTYcMyksrQpYdoAiKATVUzWJq7WPv1PKsErUT1X4a?filename=1-SEVERE.json",
    "MSPAINT": "https://ipfs.io/ipfs/QmWn4si7qwcpDH13BKATTfM1GRKKvncrM63WqysUfgJa9i?filename=3-MSPAINT.json",
    "NIGHTTIME": "https://ipfs.io/ipfs/QmP7md8n2sFFRkHNZs9eemd5Wtq3DEck6nDYNF9dMF2sS3?filename=0-NIGHTTIME.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    num_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {num_of_collectibles} tokenIds")
    for token_id in range(num_of_collectibles):
        flavor = get_flavor(advanced_collectible.tokenIdToFlavor(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, flavor_metadata_dict[flavor])


def set_tokenURI(tokenid, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(tokenid, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"You can now view your NFT at {OPENSEA_URL.format(nft_contract.address, tokenid)}"
    )
    print("Please refresh after 20 mins!")
