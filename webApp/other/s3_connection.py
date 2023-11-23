
from boto3.session import Session
from boto3 import client


class S3Connection:
    """
    Contains the methods to connect to the S3 bucket,
    and download the files from the bucket.

    Dependency requiered for web app and the mobile app
    """

    def __init__(self) -> None:
        # Connection to the S3 bucket
        self._s3_connection: Session = client(
            "s3",
            aws_access_key_id="AKIA5RCYKSQAPI3AKL3K",
            aws_secret_access_key="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",
        )
        # Files in the S3 bucket
        __files = self._s3_connection.list_objects(Bucket="test-medway-bucket")["Contents"]
        # Daily reports
        self.__daily_reports: list[str] = [
            file["Key"].split("/")[-1].split(".")[0]
            for file in __files
            if "daily_reports" in file["Key"] and file["Key"] != "daily_reports/"
        ]
        # Monthly reports
        self.__monthly_reports: list[str] = [
            file["Key"].split("/")[-1].split(".")[0]
            for file in __files
            if "monthly_reports" in file["Key"] and file["Key"] != "monthly_reports/"
        ]


    def get_file_names(self, folder: str) -> list[str]:
        """
        Returns the file names from the S3 bucket

        Parameters:
            - :param:`folder` (str): The folder in the S3 bucket from where the file names will be returned

        Returns:
            - list[str]: The file names from the S3 bucket
        """

        if folder == "daily_reports":
            return self.__daily_reports
        elif folder == "monthly_reports":
            return self.__monthly_reports
        else:
            return []


    def download(self, folder: str, download_path: str ,file_name: str) -> None:
        """
        Downloads the file from the S3 bucket

        Parameters:
            - :param:`folder` (str): The folder in the S3 bucket where the file is located
            - :param:`download_path` (str): The path where the file will be downloaded
            - :param:`file_name` (str): The name of the file to be downloaded

        Returns:
            - None
        """

        self._s3_connection.download_file(
            "test-medway-bucket",               # Bucket name - S3 bucket
            f"{folder}/{file_name}.pdf",        # Key - Path to the file in the S3 bucket
            f"{download_path}/{file_name}.pdf"  # Filename - Path where the file will be downloaded
        )
