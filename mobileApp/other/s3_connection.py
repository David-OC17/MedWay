
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
            aws_access_key_id = "AKIA5RCYKSQAPI3AKL3K",
            aws_secret_access_key = "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",
            region_name = "us-east-2",
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


    def get_download_link(self, folder: str, file_name: str) -> None:
        """
        Returns a download link for the file in the S3 bucket

        Parameters:
            - :param:`folder` (str): The folder in the S3 bucket where the file is located
            - :param:`file_name` (str): The name of the file to be downloaded

        Returns:
            - :return:`url` (str): The download link for the file in the S3 bucket
        """

        url: str = self._s3_connection.generate_presigned_url(
            ClientMethod = "get_object",
            Params = {"Bucket": "test-medway-bucket", "Key": f"{folder}/{file_name}.pdf"},
            ExpiresIn = 3600,
        )

        return url
