from fastapi import UploadFile

from appstore.exceptions.appstore_exceptions import InvalidFileException, UnsupportedMediaTypeException, InvalidFileNameException


def validate_image(file: UploadFile) -> bool:
    if file is None:
        raise InvalidFileException

    if file.content_type.lower() != "image/jpeg" and file.content_type.lower() != "image/png":
        raise UnsupportedMediaTypeException

    if file.filename is None or not (file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".png")):
        raise InvalidFileNameException

    return True
