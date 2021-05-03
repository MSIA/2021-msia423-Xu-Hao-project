import os
import re
import argparse
import logging
import boto3
import botocore.exceptions

logger = logging.getLogger(__name__)

def _parse_s3(s3path):
    """
    Parse s3 path.
    Source: https://github.com/MSIA/2021-msia423/blob/main/aws-s3/s3.py
    """
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_to_s3(args):
    """ Upload data to S3 bucket. """
    # connect to s3 using aws access key
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
        logger.info("AWS S3 Connected.")
    except botocore.exceptions.PartialCredentialsError:
        logger.error("AWS Credentials Invalid.")

    # upload all raw pictures under the local path to s3
    bucket_name, s3_store_path = _parse_s3(args.s3_path)
    for root, dirs, files in os.walk(args.local_path):
        for file in files:
            s3.upload_file(os.path.join(root, file), bucket_name, os.path.join(s3_store_path, file))
            logger.info("{} Uploaded.".format(file))
    logger.info("All Image Uploaded to S3.")
