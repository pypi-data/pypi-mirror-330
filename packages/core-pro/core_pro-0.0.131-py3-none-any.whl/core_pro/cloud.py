import boto3
import os
from pathlib import Path
from tqdm import tqdm
from google.cloud import storage
import datetime
import polars as pl
import json


class AWS:
    def __init__(self, bucket_name: str):
        dict_ = {
            "endpoint_url": "https://s3g.data-infra.shopee.io",
            "aws_access_key_id": os.environ["PRESTO_USER"],
            "aws_secret_access_key": os.environ["PRESTO_PASSWORD"],
        }
        self.bucket_name = bucket_name
        self.client = boto3.client("s3", **dict_)
        self.my_bucket = boto3.resource("s3", **dict_).Bucket(self.bucket_name)
        self.status = f"[green3]🐸 S3:[/]"

    def get_all_files(self):
        print(f"{self.status} [Get] All files in: {self.bucket_name}")
        return [_.key for _ in self.my_bucket.objects.all()]

    def delete_file(self, key: str):
        self.client.delete_object(Bucket=self.bucket_name, Key=key)
        print(f"{self.status} [Remove]: {key}")

    def get_file_size(self, key: str):
        return self.my_bucket.Object(key).content_length

    def upload_file(self, file: Path, folder: str = None):
        file_size = file.stat().st_size
        desc = f"[Upload] {file.name}, size: {file_size / 1024**2:,.2f}MB"
        location = f"{folder}/{file.stem}" if folder else file.stem
        with tqdm(total=file_size, unit="B", unit_scale=True, desc=desc) as pbar:
            self.my_bucket.upload_file(
                file, Key=location, Callback=lambda x: pbar.update(x)
            )

    def download_file(self, path: Path, key: str):
        file_size = self.get_file_size(key)
        desc = f"[Download] {key}, size: {file_size / 1024 ** 2:,.2f}MB"
        with tqdm(total=file_size, unit="B", unit_scale=True, desc=desc) as pbar:
            self.my_bucket.download_file(
                Key=key,
                Filename=path / key.split("/")[-1],
                Callback=lambda x: pbar.update(x),
            )

    def create_presigned_url(self, key: str, expiration: int = 900):
        url = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=expiration,
        )
        print(f"{self.status} [Pre-signed] {key} in {expiration / 3600}h")
        return url

    def convert_dataframe_flink_config(
        self, df: pl.DataFrame, key: str, table_name: str, primary_key: str, file_type: str = "parquet",
    ):
        # dict mapping
        type_mapping = {
            pl.Datetime: "datetime",
            pl.Int8: "int",
            pl.Int32: "int",
            pl.Int64: "bigint",
            pl.UInt32: "int",
            pl.Categorical: "string",
            pl.String: "string",
            pl.Float32: "float",
            pl.Float64: "double",
        }

        # convert to flink config
        flink_schema = [
            {"field": field, "type": type_mapping.get(dtype)}
            for field, dtype in dict(df.schema).items()
        ]
        flink_schema = json.dumps(flink_schema)

        # convert to sql script
        sql_schema = [
            f"{field} {type_mapping.get(dtype)}" for field, dtype in dict(df.schema).items()
        ]
        sql_schema = ",\n ".join(sql_schema)

        config = f"""
        [FLINK CONFIG]
        source {{
            S3FileSource {{
                datasource_name = "my_s3"
                path = "s3a://{self.bucket_name}/{key}"
                format = "{file_type}"
                schema = "{flink_schema}"
                endpoint = "https://s3g.data-infra.shopee.io"
                bucket = "{self.bucket_name}"
                access_key = "{os.environ['PRESTO_USER']}"
                secret_key = "{os.environ['PRESTO_PASSWORD']}"
                ignore-parse-errors = "false"
                skip-first-data-row = "true"
                result_table_name = "s3FileSource"
              }}
        }}
        
        [CREATE SQL TABLE]:
        CREATE TABLE {table_name} (
        {sql_schema}
        PRIMARY KEY ({primary_key})
        )
        """
        print(config)


class Gcloud:
    def __init__(self, json_path: str):
        self.client = storage.Client.from_service_account_json(str(json_path))
        self.status = f"[green3]🐻‍❄️ Gcloud:[/]"
        self.bucket_name = "kevin-bi"
        self.bucket = self.client.bucket(self.bucket_name)

    def download_file(self, blob_path: str, file_path: Path):
        blob = self.bucket.blob(blob_path)
        blob.download_to_filename(file_path)
        print(f"{self.status} download {blob_path}")

    def upload_file(self, blob_path: str, file_path: Path):
        blob_path_full = f"{blob_path}/{file_path.name}"
        blob = self.bucket.blob(blob_path_full)
        blob.upload_from_filename(file_path)
        print(f"{self.status} upload {file_path.stem} to {blob_path}")
        return blob_path_full

    def generate_download_signed_url_v4(self, blob_file, minutes=15):
        blob = self.bucket.blob(blob_file)
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=minutes),
            method="GET",
        )
        print(
            f"{self.status} Presigned [{blob_file}] in {minutes} mins \n" f"Url: {url}"
        )
        return url
