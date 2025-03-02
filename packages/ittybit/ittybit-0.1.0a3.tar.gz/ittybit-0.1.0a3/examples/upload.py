from __future__ import annotations

import os

from ittybit import IttyBit
from ittybit.types.file_create_response import FileCreateResponse

# Initialize the client
client = IttyBit(
    api_key="your-api-key",
)

def upload_file(filepath: str) -> None:
    """
    Example of uploading a file with metadata.
    
    Args:
        filepath: Path to the file to upload
    """
    filename = os.path.basename(filepath)
    
    # Open the file in binary mode
    with open(filepath, "rb") as file:
        # Upload with metadata and options
        response: FileCreateResponse = client.uploader.upload(
            file=file,
            filename=filename,
            # Optional parameters
            folder="/uploads",  # Destination folder
            label="My uploaded file",
            alt="Alternative text",
            title="File title",
            metadata={
                "description": "Example file upload",
                "tags": ["example", "upload"],
                "custom_field": "value"
            },
            content_type="video/mp4",  # Or appropriate MIME type
            async_upload=False,  # Set to True for async processing
            timeout=3600,  # Upload timeout in seconds
        )
    
    print(f"Upload complete! File ID: {response.file_id}")
    print(f"Media ID: {response.media_id}")


def main() -> None:
    # Example usage
    try:
        upload_file("path/to/video.mp4")
    except Exception as e:
        print(f"Upload failed: {e}")


if __name__ == "__main__":
    main()
