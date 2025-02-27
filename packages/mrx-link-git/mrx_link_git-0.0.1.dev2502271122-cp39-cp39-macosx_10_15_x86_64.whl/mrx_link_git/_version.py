import json
from pathlib import Path
from typing import Any

__all__ = ["__version__"]


def _fetchVersion() -> Any:
    # pylint: disable=invalid-name
    HERE = Path(__file__).parent.resolve()
    try:
        pkg_json = json.loads((HERE / "labextension" / "package.json").read_bytes())
        version = pkg_json["version"]
    except:  # pylint: disable=bare-except  # noqa
        version = "0.0.1.dev2502271122"

    return version


__version__ = _fetchVersion()
