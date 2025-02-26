from pathlib import Path
from urllib.parse import urlparse


def get_scheme(source: str) -> str:
    """
    Determine the protocol scheme for a given source.

    Args:
        source: A URL or file path.
    
    Returns:
        One of: 'http', 'https', 'ftp', 's3', 'gs', 'local', or 'snippet'.
    """
    parsed = urlparse(source)
    if parsed.scheme in {"http", "https", "ftp", "s3", "gs"}:
        return parsed.scheme
    if Path(source).exists():
        return "local"
    return "snippet"