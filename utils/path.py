import os
from pathlib import Path
from git import Repo

def get_git_root(path=os.getcwd()) -> Path:
    git_repo = Repo(path, search_parent_directories=True)
    git_root = Path(git_repo.git.rev_parse("--show-toplevel"))
    return git_root