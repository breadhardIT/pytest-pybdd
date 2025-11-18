import logging

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
LOG = logging.getLogger(__name__)

class S3Repository:
    """
    A repository for working with s3 document bucket
    Args:
        endpoint_url (str): The url for accessing to the s3 service
        access_key (str): The access_key for s3 requests
        secret_key (str): The secret_key for s3 requests
        bucket (str): The bucket name
    """
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, bucket: str):
        self.client : BaseClient = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.bucket : str = bucket

    def generate_presigned_url_for_get(self, key: str, expiration: int = 3600) -> str:
        """
        Generates a presigned URL for being accessed from consumers
        Args:
            key (str): the object key (refers to path in S3 bucket)
            expiration (int): The duration of the generated URL in seconds (3600 by default)
        Returns:
            url (str): The generated URL
        """
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expiration,
        )

    def upload_file(self,content: bytes, key: str):
        """
        Upload a file to the bucket in the specified path
        Args:
            key (str): The key (file name and path)
            content: Content in bytes
        """
        LOG.info(f"Saving file {key}")
        self.client.put_object(Bucket = self.bucket,Key = key,Body=content)

    def file_exists(self,key: str) -> bool:
        LOG.info(f"Getting file {key}")
        try:
            self.client.get_object(
                Bucket=self.bucket,
                Key=key
            )
            return True
        except ClientError:
            return False

    def delete_file(self, key: str):
        """
        Delete the file specified in file_path
        Args:
            key (str): The path and file name of the file to delete
        """
