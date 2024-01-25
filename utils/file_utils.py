import aiofiles
import os

async def save_file_async(file, storage_directory):
    """
    Save an uploaded file asynchronously.

    Parameters:
    - file: UploadFile - The uploaded file.
    - storage_directory: str - The directory where the file should be saved.
    """
    file_path = os.path.join(storage_directory, file.filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)