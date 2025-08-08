import pandas as pd
import os
# from charset_normalizer import from_path

class Dataset:
    def __init__(self, name, data_path, prefix:str=None):
        self._name = name
        self._data_path = data_path
        self._prefix = prefix
        self._data_files = self._load_files()
                
    def _load_files(self) -> dict[str:pd.DataFrame]:
        files = {}
        for file_name in os.listdir(self._data_path):
            file_path = self._data_path / file_name
            if os.path.isfile(file_path) and file_name.lower().endswith('.csv'):
                key_name = file_name if self._prefix is None else f"{self._prefix}_{len(self._data_files)}"

                # placeholder, implement encoding detection for scalability
                # results = from_path(file_path, chunk_size=51200)
                # encoding = getattr(results.best(), 'encoding', None) or 'utf-8'
                try:
                    files[key_name] = pd.read_csv(file_path, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    files[key_name] = pd.read_csv(file_path, encoding='latin1')
        return files


    def list_data_files(self) -> dict[str:pd.DataFrame]:
        return self._data_files
    
    def get_data_files(self, fname:str=None) -> list[pd.DataFrame] | pd.DataFrame:
        if fname is None:
            return self._data_files.values()
        elif fname not in self._data_files:
            raise KeyError(f"{fname} not found in data files.")
        return self._data_files[fname]

    def num_files(self) -> int:
        return len(self._data_files)

    def get_unique_cols(self) -> list[str]:
        return {col for df in self._data_files.values() for col in df.columns}
    
    def get_name(self) -> str:
        return self._name


class LoadData:
    def __init__(self, root_data_path) -> None:
        self._root_path = root_data_path
        self._data_dirs = os.listdir(root_data_path)
        self._datasets = {}

    def get_data_dirs(self) -> list[str]:
        return self._data_dirs
    
    def load_datasets(self, omit:list, prefix:str=None, status_msg:str=True) -> None:
        for d in self._data_dirs:
            if d not in omit:
                self._datasets[d] = Dataset(d, self._root_path / d, prefix)
                if status_msg:
                    print(f"Dataset '{d}' loaded.")
        print("All datasets loaded")

    def list_datasets(self):
        return self._datasets

    def get_datasets(self, name:str=None):
        if name is None:
            return self._datasets.values()
        return self._datasets[name] if name in self._datasets else None
    
    def unpack(self) -> tuple:
        return tuple(self._datasets.values())
    