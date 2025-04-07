import os
from fastapi import UploadFile, HTTPException
from pathlib import Path
from datetime import datetime
from app.config import settings

UPLOAD_DIR = "uploads/products"  # Directory where product images will be stored


def save_upload_file(upload_file: UploadFile, product_id: int):
    """
    Save the uploaded file to the server with a unique filename based on product_id.
    Creates the upload directory if it doesn't exist and stores the file.
    """
    try:
        # Create the upload directory if it doesn't already exist
        Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

        # Generate a unique filename using product_id and timestamp
        file_ext = upload_file.filename.split('.')[-1]  # Get the file extension
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp
        filename = f"product_{product_id}_{timestamp}.{file_ext}"  # Unique filename format
        file_path = os.path.join(UPLOAD_DIR, filename)  # Full file path

        # Save the uploaded file to the server
        with open(file_path, "wb") as buffer:
            buffer.write(upload_file.file.read())  # Write the file content to disk

        return file_path  # Return the path where the file is saved
    except Exception as e:
        # Raise an HTTP exception if any error occurs during file saving
        raise HTTPException(
            status_code=500,
            detail=f"Error saving file: {str(e)}"
        )
