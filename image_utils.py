import base64
from mimetypes import guess_type
from pathlib import Path


def png_file_to_data_url(image_path: str) -> str:
    """
    Loads a PNG file and returns a data URL with base64-encoded contents.
    Args:
        image_path (str): Path to the PNG file.
    Returns:
        str: Data URL containing the base64-encoded PNG image.
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a PNG.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    mime_type, _ = guess_type(image_path)
    if mime_type != "image/png":
        raise ValueError(f"File is not a PNG image: {image_path}")
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_encoded_data}"
