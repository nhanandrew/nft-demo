from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_flavor
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests


def main():
    advanced_collectible = AdvancedCollectible[-1]
    num_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"You have created {num_of_advanced_collectible} collectibles!")
    for token_id in range(num_of_advanced_collectible):
        flavor = get_flavor(advanced_collectible.tokenIdToFlavor(token_id))
        metadata_file_name = (
            f".\metadata{network.show_active()}\{token_id}-{flavor}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists!")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = flavor
            collectible_metadata["description"] = f"A bottle of {flavor} Robitussin"
            image_path = Path(
                "img/" + flavor.lower().replace("_", "-") + ".png"
            ).__str__()
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-SEVERE.png" -> 0-SEVERE.png
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
