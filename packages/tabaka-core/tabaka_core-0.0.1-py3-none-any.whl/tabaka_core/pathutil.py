import os
from tabaka_core.models import ALLOWED_BASE_DIR


def secure_path(path: str) -> str:
    """
    Securely joins a given path with the allowed base directory, preventing
    directory traversal vulnerabilities.

    Args:
        path (str): The path to be secured. It should *not* start with a slash.

    Returns:
        str: The absolute path after securely joining it with the base directory.

    Raises:
        ValueError: If the resulting path is not within the allowed base directory,
                    or if the input path is absolute.
    """
    if os.path.isabs(path):
        raise ValueError("Path must be relative, not absolute.")

    # Normalize the path to remove any ".." components and ensure consistent path separators
    normalized_path = os.path.normpath(path)

    # Construct the absolute path by joining with the allowed base directory
    abs_path = os.path.abspath(os.path.join(ALLOWED_BASE_DIR, normalized_path))

    # Canonicalize the path to resolve symbolic links
    abs_path = os.path.realpath(abs_path)

    # Check that the resulting path is still within the allowed base directory
    if not abs_path.startswith(ALLOWED_BASE_DIR):
        raise ValueError(
            "Attempted access outside of allowed base directory. Path must reside within the virtual file system."
        )

    return abs_path
