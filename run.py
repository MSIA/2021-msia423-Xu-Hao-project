import argparse
import src.store_data_to_s3 as upload

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Upload data to S3 bucket
    sb_upload = subparsers.add_parser("upload", description="upload data to S3 buckets")
    sb_upload.add_argument('--s3_path', required=True, help='path to store raw data on S3')
    sb_upload.add_argument('--local_path', required=True, help='local path of raw data')
    sb_upload.set_defaults(func=upload.upload_to_s3)

    args = parser.parse_args()
    args.func(args)
