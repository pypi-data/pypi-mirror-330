from os import PathLike
from typing import Union

from boto3 import Session


def upload_to_s3(
    session: Session, file_to_upload: str, bucket_name: str, prefix: str
) -> None:
    """Upoad a file to an S3 bucket.

    :param session: The AWS ``Session`` object to use to do the upload.
    :type session: Session
    :param file_to_upload: The name of the file to upload.
    :type file_to_upload: str
    :param bucket_name: The name of the bucket into which to upload the file.
    :type bucket_name: str
    :param prefix: The S3 prefix (path) for the file.
    :type prefix: str
    """
    with open(file_to_upload, "rb") as data:
        session.client("s3").upload_fileobj(data, bucket_name, prefix)


def download_from_s3(
    session: Session, file_to_download: str, bucket_name: str, prefix: str
) -> None:
    """Download a file from an S3 bucket to local disk.

    :param session: The AWS ``Session`` object to use to do the download.
    :type session: Session
    :param file_to_download: The name of the file to create.
    :type file_to_download: str
    :param bucket_name: The name of the bucket from which to download the file.
    :type bucket_name: str
    :param prefix: The S3 prefix of the file to download.
    :type prefix: str
    """
    try:
        with open(file_to_download, "wb") as data:
            session.client("s3").download_fileobj(bucket_name, prefix, data)
    except Exception as e:
        raise Exception(f"Unable to download {bucket_name}/{prefix}: {str(e)}")
