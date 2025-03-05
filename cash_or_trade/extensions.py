from flask_sqlalchemy import SQLAlchemy
import boto3
from decouple import config

database = SQLAlchemy()

s3_client = boto3.client(
    's3',
    aws_access_key_id=config('S3_ACCESS_KEY'),
    aws_secret_access_key=config('S3_SECRET_ACCESS_KEY')
    )