import os
from app import app
import boto3, botocore
# from config import S3_KEY, S3_SECRET, S3_BUCKET

# s3 = boto3.client(
#    "s3",
#    aws_access_key_id=app.config["S3_KEY"],
#    aws_secret_access_key=app.config["S3_SECRET"]
# )

# def upload_file_to_s3(file, username, acl="public-read"):

#     try:

#         s3.upload_fileobj(
#             file,
#             app.config.get("S3_BUCKET"),
#             "{}/{}".format(username, file.filename),
#             ExtraArgs={
#                 "ACL": acl,   
#                 "ContentType": file.content_type
#             }
#         )

#     except Exception as e:
#         # This is a catch all exception, edit this part to fit your needs.
#         print("Something Happened: ", e)
#         return e
     
#     return "{}/{}".format(username, file.filename)

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config["S3_KEY"],
   aws_secret_access_key=app.config["S3_SECRET"]
)


def upload_file_to_s3(file, username, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            app.config.get("S3_BUCKET"),
            "{}/{}".format(username,file.filename),
            ExtraArgs={
                "ACL": acl,
                "ContentType" : file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}/{}".format(username, file.filename)