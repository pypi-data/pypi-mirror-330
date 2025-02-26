from packaging import version

from dguard.asr.aliasr import (  # Ensure that __version__ is defined in your package's __init__.py
    __version__,
)


def get_pypi_version(package_name):
    import requests

    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return version.parse(data["info"]["version"])
    else:
        raise Exception("Failed to retrieve version information from PyPI.")
