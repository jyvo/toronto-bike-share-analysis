from utils.path import get_git_root
import requests
import zipfile

def main():
    data_dir = get_git_root() / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)

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

            download_path = data_dir / resource_metadata["result"]["name"]
            download_path.mkdir(parents=True, exist_ok=True)

            try:
                resp = requests.get(resource_metadata["result"]["url"], stream=True)
                resp.raise_for_status()
                
                file_type = "." + resource_metadata["result"]["format"].lower()
                file_name = resource_metadata["result"]["name"] + file_type
                with open(download_path/file_name, "wb") as f:
                    f.write(resp.content)

                if file_type == ".zip":
                    try:
                        with zipfile.ZipFile(download_path/file_name, "r") as ref:
                            ref.extractall(download_path)
                        print(f"Unzipped: {file_name}")
                    except zipfile.BadZipFile:
                        print(f"Failed to unzip the following file: {file_name}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")

if __name__ == "__main__":
    main()