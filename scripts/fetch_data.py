from utils.path import get_git_root
import requests
import zipfile

download_path = get_git_root() / "data" / "raw"
# download_path.mkdir(parents=True, exist_ok=True)

base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action"

package_url = base_url + "/package_show"
params = {"id": "bike-share-toronto-ridership-data"}

package_resp = requests.get(package_url, params=params)

package_resp.raise_for_status()

package = package_resp.json()

for i, resource in enumerate(package["result"]["resources"]):
    if not resource["datastore_active"]:
        url = base_url + "/resource_show?id=" + resource["id"]
        resource_metadata = requests.get(url).json()
        # print(resource_metadata)

        try:
            resp = requests.get(resource_metadata["result"]["url"], stream=True)
            resp.raise_for_status()
            
            # download relevant data files (check for filetype/unzip)
            # check if file already exists, maybe have a save of the metadata somewhere to prevent redundancy
            file_type = "." + resource_metadata["result"]["format"].lower()
            file_name = resource_metadata["result"]["name"] + file_type
            with open(download_path/file_name, "wb") as f:
                f.write(resp.content)
                f.close()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")

# if __name__ == "__main__":
#     main()