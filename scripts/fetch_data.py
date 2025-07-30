import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from utils.path import get_git_root
from utils.unzip import unzip
import requests

def main():
    download_dir = get_git_root() / "data" / "raw"
    download_dir.mkdir(parents=True, exist_ok=True)

    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action"

    package_url = base_url + "/package_show"
    params = {"id": "bike-share-toronto-ridership-data"}

    package_resp = requests.get(package_url, params=params)

    package_resp.raise_for_status()

    package = package_resp.json()

    for _, resource in enumerate(package["result"]["resources"]):
        if not resource["datastore_active"]:
            url = base_url + "/resource_show?id=" + resource["id"]
            resource_metadata = requests.get(url).json()
            # print(resource_metadata)

            resource_dir = download_dir / resource_metadata["result"]["name"]
            resource_dir.mkdir(parents=True, exist_ok=True)

            try:
                resp = requests.get(resource_metadata["result"]["url"], stream=True)
                resp.raise_for_status()
                
                file_type = "." + resource_metadata["result"]["format"].lower()
                file_name = resource_metadata["result"]["name"] + file_type

                with open(resource_dir/file_name, "wb") as f:
                    f.write(resp.content)

                if file_type == ".zip":
                    unzip(resource_dir / file_name, resource_dir)

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
    print("Downloaded all raw data files")

if __name__ == "__main__":
    main()