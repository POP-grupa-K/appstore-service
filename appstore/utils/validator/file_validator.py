from fastapi import UploadFile

from appstore.exceptions.appstore_exceptions import InvalidFile, UnsupportedMediaType, InvalidFileName


def file_is_valid(file: UploadFile) -> bool:
    if file is None:
        raise InvalidFile

    if file.content_type.lower() != "image/jpeg" and file.content_type.lower() != "image/png":
        raise UnsupportedMediaType

    if file.filename is None or not (file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".png")):
        raise InvalidFileName

    return True
