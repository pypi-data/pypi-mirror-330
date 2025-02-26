import json
import os
import sys
import types
from pathlib import Path
from shutil import copyfile
from typing import Callable, Dict
from urllib.parse import urlparse

import pystac.item
import requests

from mlstac.utils import get_scheme

# --- Helpers for Text-Based Sources (for JSON and modules) ---

def _fetch_http(source: str) -> str:
    """Fetch content from an HTTP/HTTPS/FTP endpoint."""
    response = requests.get(source)
    response.raise_for_status()
    return response.text

def _fetch_local(source: str) -> str:
    """Read content from the local filesystem."""
    with open(source, "r") as f:
        return f.read()

def _fetch_s3(source: str) -> str:
    """Fetch content from an AWS S3 bucket."""
    try:
        import boto3
    except ImportError as e:
        raise ImportError("Requires boto3: pip install boto3") from e
    parsed = urlparse(source)
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=parsed.netloc, Key=parsed.path.lstrip("/"))
    return obj["Body"].read().decode("utf-8")

def _fetch_gs(source: str) -> str:
    """Fetch content from Google Cloud Storage."""
    try:
        from google.cloud import storage
    except ImportError as e:
        raise ImportError("Requires google-cloud-storage: pip install google-cloud-storage") from e
    parsed = urlparse(source)
    client = storage.Client()
    blob = client.bucket(parsed.netloc).blob(parsed.path.lstrip("/"))
    return blob.download_as_text()

_SCHEME_HANDLERS: Dict[str, Callable[[str], str]] = {
    "http": _fetch_http,
    "https": _fetch_http,
    "ftp": _fetch_http,
    "local": _fetch_local,
    "s3": _fetch_s3,
    "gs": _fetch_gs,
}

def fetch_source(source: str, snippet_suffix: str = "") -> str:
    """
    Retrieve textual content from a given source.

    If the source is a "snippet", a base URL is prepended.

    Args:
        source: A URL, file path, or model identifier.
        snippet_suffix: Suffix to append if the source is a snippet.
    
    Returns:
        The fetched content as a string.
    """
    scheme = get_scheme(source)
    source = f"{source}{snippet_suffix}"
    handler = _SCHEME_HANDLERS.get(scheme)
    if not handler:
        raise ValueError(f"Unsupported scheme: {scheme}")
    try:
        return handler(source)
    except Exception as e:
        raise RuntimeError(f"Failed to load from {source}") from e

# --- Public Text-Based Loaders ---

def load_python_module(source: str, module_name: str = "isp_model_loader") -> types.ModuleType:
    """
    Dynamically load a Python module from the given source.

    Args:
        source: A URI or local file path to the Python code.
        module_name: The name to assign to the imported module.
    
    Returns:
        The loaded module object.
    """
    code = fetch_source(source, snippet_suffix="/load.py")
    module = types.ModuleType(module_name)
    exec(code, module.__dict__)
    sys.modules[module_name] = module
    return module


def load_stac_item(source: str) -> dict:
    """
    Load a STAC JSON item from the given source.

    This function expects the JSON to follow the STAC item specification.
    A snippet-based source will have '/mlm.json' appended to its URL.

    Args:
        source: A URI or local file path to the JSON file.
    
    Returns:
        A dictionary representation of the STAC item.
    """
    content = fetch_source(source, snippet_suffix="/mlm.json")
    return pystac.item.Item.from_dict(json.loads(content))
    

# ---  Downloading Files ---

def download_file(source: str, snippet_suffix: str = "/model.safetensor", outpath: str = ".") -> Path:
    """
    Download a file from the given source and save it in the specified output folder.

    This function handles various protocols (HTTP, local, S3, GS) and uses
    streaming for remote downloads to efficiently write the file to disk.

    Args:
        source: A URL, local file path, or model identifier.
        snippet_suffix: Suffix to append if the source is a snippet.
        outpath: Directory where the file will be saved.
    
    Returns:
        A Path object representing the saved file.
    """
    scheme = get_scheme(source)
    
    # Determine the output filename based on the source path.
    parsed = urlparse(source)
    filename = os.path.basename(parsed.path)
    if not filename:
        # Fallback: use the last part of the snippet_suffix or a default name.
        filename = os.path.basename(snippet_suffix) if snippet_suffix else "downloaded_file"
    
    out_file = Path(outpath) / filename
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    if scheme in {"http", "https", "ftp"}:
        # Streaming download to file
        with requests.get(source, stream=True) as response:
            response.raise_for_status()
            with open(out_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    elif scheme == "local":
        # For local sources, simply copy the file.
        copyfile(source, out_file)
    elif scheme == "s3":
        try:
            import boto3
        except ImportError as e:
            raise ImportError("Requires boto3: pip install boto3") from e
        parsed = urlparse(source)
        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=parsed.netloc, Key=parsed.path.lstrip("/"))
        with open(out_file, "wb") as f:
            f.write(obj["Body"].read())
    elif scheme == "gs":
        try:
            from google.cloud import storage
        except ImportError as e:
            raise ImportError("Requires google-cloud-storage: pip install google-cloud-storage") from e
        parsed = urlparse(source)
        client = storage.Client()
        blob = client.bucket(parsed.netloc).blob(parsed.path.lstrip("/"))
        with open(out_file, "wb") as f:
            f.write(blob.download_as_bytes())
    else:
        raise ValueError(f"Unsupported scheme: {scheme}")
    
    return out_file
