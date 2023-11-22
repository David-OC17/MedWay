
from boto3.session import Session
import boto3


class S3Connection:
    """
    Contains the methods to connect to the S3 bucket,
    and download the files from the bucket.

    Dependency requiered for web app and the mobile app
    """

    def __init__(self) -> None:
        self._s3_connection: Session = boto3.client(
            "s3",
            aws_access_key_id="AKIA5RCYKSQAPI3AKL3K",
            aws_secret_access_key="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",
        )
        self.__files: list[str] = [
            file["Key"] for file in self._s3_connection.list_objects(Bucket="test-medway-bucket")["Contents"]
        ]


    def get_file_names(self) -> list[str]:
        """
        Returns the file names from the S3 bucket

        Parameters:
            - No parameters

        Returns:
            - list[str]: The file names from the S3 bucket
        """

        return self.__files


    def download_file(self, file_name: str) -> None:
        """
        Downloads the file from the S3 bucket

        Parameters:
            - file_name (str): The name of the file to download

        Returns:
            - None
        """

        self._s3_connection.download_file(
            "test-medway-bucket",
            file_name,
            f"C:/Users/Dany/Desktop/{file_name}"
        )
