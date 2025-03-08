from flask_sqlalchemy import SQLAlchemy
import boto3
from decouple import config

database = SQLAlchemy()

s3_client = boto3.client(
    's3',
    aws_access_key_id=config('S3_ACCESS_KEY'),
    aws_secret_access_key=config('S3_SECRET_ACCESS_KEY')
    )

def email_client(buyer, item, offer):
    line1 = (f"To: {buyer.username} <{buyer.email}>, {item.user.username} <{item.user.email}>")
    line2 = (f"From: <CompanyName@email.com>")
    line3 = (f"Subject: {buyer.username} has an offer for {item.name}.")
    line4 = (f"Message: {offer}")
    email = [line1, line2, line3, line4]
    return email