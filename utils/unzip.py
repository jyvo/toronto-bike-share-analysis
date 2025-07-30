from pathlib import Path
import zipfile
import shutil

def is_zip(file_name:str):
    return file_name.lower().endswith(".zip")

def unzip(filepath:Path, extract_dir:Path, recur=True, rm_top_level=True) -> bool:
    file_name = filepath.name
    try:
        with zipfile.ZipFile(filepath, "r") as zf:
            namelist = zf.namelist()
            top_level_dirs = set(Path(x).parts[0] for x in namelist if len(Path(x).parts) > 1)

            if rm_top_level and len(top_level_dirs) == 1:
                temp_dir = extract_dir / "__temp"
                temp_dir.mkdir(exist_ok=True)

                zf.extractall(temp_dir)

                top_dir = temp_dir / top_level_dirs.pop()
                for item in top_dir.iterdir():
                    if recur and is_zip(item.name):
                        unzip(top_dir / item.name, extract_dir)
                    else:
                        shutil.move(str(item), extract_dir / item.name)

                shutil.rmtree(temp_dir)
            else:
                zf.extractall(extract_dir)
        print(f"Unzipped: {file_name}")
        return True
    except zipfile.BadZipFile:
        print(f"Failed to unzip the following file: {file_name}")

    return False
