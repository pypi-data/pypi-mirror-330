from typing import Dict, Optional, List
from pathlib import Path

PATH_LOOKUPS = [
    {
        "local": Path("/assets"),
        "remote": Path(
            "/media/storage/Files/Dayne/WebDev/Websites/proj_ceonstock/assets"
        ),
    },
    {
        "local": Path("/storage"),
        "remote": Path(
            "/media/storage/Files/Dayne/WebDev/Websites/proj_ceonstock/local_storage"
        ),
    },
]


class PathResolver:
    def __init__(self, path_lookups: List[Dict[str, Path]]):
        self.path_lookups = path_lookups

    def local_to_remote(self, local_path: Path) -> Optional[Path]:
        for path in PATH_LOOKUPS:
            try:
                return Path(path["remote"] / local_path.relative_to(path["local"]))
            except ValueError:  # local_path is not a child of the tested path.
                pass

    def remote_to_local(self, remote_path: Path) -> Optional[Path]:
        for path in PATH_LOOKUPS:
            try:
                return Path(path["local"] / remote_path.relative_to(path["remote"]))
            except ValueError:  # local_path is not a child of the tested path.
                pass
