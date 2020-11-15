from fastapi import UploadFile

from appstore.exceptions.appstore_exceptions import InvalidFile


def file_is_valid(file: UploadFile) -> bool:
    if file is None:
        raise InvalidFile

    if file.content_type.capitalize() != "image/jpeg":
        raise

    return True
