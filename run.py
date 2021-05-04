import argparse
import logging.config

import src.s3_bucket as s3
import src.rds_db as rds

logging.config.fileConfig('config/logging/local.conf')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Sub-parser for uploading data to S3 bucket
    sb_upload = subparsers.add_parser("upload", description="upload data to S3 buckets")
    sb_upload.add_argument('--s3_path', required=True, help='path to store raw data on S3')
    sb_upload.add_argument('--local_path', required=True, help='local path of raw data')
    sb_upload.set_defaults(func=s3.upload_to_s3)

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="create database")
    sb_create.set_defaults(func=rds.create_db)

    # Parse args and run corresponding pipeline
    args = parser.parse_args()
    args.func(args)
