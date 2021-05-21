import os
import re
import logging
import boto3
import botocore.exceptions

logger = logging.getLogger(__name__)


def _parse_s3(s3path):
    """Parse s3 path. Source: https://github.com/MSIA/2021-msia423/blob/main/aws-s3/s3.py

    Args:
        s3path (str): full s3 path

    Returns:
        str,str: s3bucket name, s3path to store the data
    """

    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_to_s3(args):
    """Upload raw data to S3 bucket.

    Args:
        args.s3_path (str): target path for uploading raw data on s3 bucket
        args.local_path (str): local path to the raw data directory

    Returns:
        None

    """
    # Connect to s3 using aws access key
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
        logger.info("AWS S3 Connected.")
    except botocore.exceptions.PartialCredentialsError:
        logger.error("AWS Credentials Invalid.")

    # Upload all raw pictures under the local path to s3
    bucket_name, s3_store_path = _parse_s3(args.s3_path)
    if len(list(os.walk(args.local_path))) > 0:
        for root, dirs, files in os.walk(args.local_path):
            for file in files:
                s3.upload_file(os.path.join(root, file), bucket_name, os.path.join(s3_store_path, file))
                logger.info("{} Uploaded.".format(file))  # log progress

    # If a single file path submitted, upload the single file
    else:
        filename = args.local_path.split('/')[-1]
        s3.upload_file(args.local_path, bucket_name, os.path.join(s3_store_path, filename))
        logger.info("{} Uploaded.".format(filename))  # log progress

    logger.info("All Image Uploaded to S3.")
