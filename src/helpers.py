"""
Helper methods
"""
from fastapi import UploadFile
from tempfile import NamedTemporaryFile
import os

async def process_file(file: UploadFile):
    contents = await file.read()
    file_copy = NamedTemporaryFile(delete=False)
    counter = 0
    try:
        with file_copy as f:
            f.write(contents)

        with open(file_copy.name) as f:
            for _ in f.readlines():
                counter += 1
    finally:
        file_copy.close()  # Remember to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # unlink (remove) the file

    return str(counter)
