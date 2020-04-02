import os
import boto3
import logging
import csv
from botocore.exceptions import ClientError, NoCredentialsError

LOG = logging.getLogger("serverless-nlp")

def _get_aws_args():
    args = {"region_name": "us-east-1"}
    if os.environ.get("env", "dev") == "dev":
        LOG.info("Running in dev mode. Using environment keys.")
        # only provide credentials in local versions - IAM role used in prod
        args.update(
            {
                "aws_access_key_id": os.environ.get("aws_access_key_id"),
                "aws_secret_access_key": os.environ.get("aws_secret_access_key"),
            }
        )
    return args


def get_client(type):
    args = _get_aws_args()
    return boto3.client(type, **args)


def doc_to_dict(doc):
    LOG.info("Unpacking to dictionary...")
    doc_dict = [line.__dict__ for line in doc.lines]
    for line in doc_dict:
        encoding_dict = {
            f"feat_{index}": val for index, val in enumerate(line["encoding"])
        }
        line.update(encoding_dict)
        del line["encoding"]
    return doc_dict


def _write_to_csv(file, doc_dict):
    try:
        with open(file, "w+") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=doc_dict[0].keys())
            writer.writeheader()
            writer.writerows(doc_dict)
            return True
    except IOError as e:
        LOG.error("I/O error writing to .csv.", e)
    return False


def _upload_file(csv_file, bucket, object_name):
    s3_client = get_client("s3")
    try:
        response = s3_client.upload_file(csv_file, bucket, object_name)
        LOG.info("Done")
    except ClientError as e:
        LOG.error("Client Error", e)
        return False
    except FileNotFoundError as e:
        LOG.error("The file was not found", e)
        return False
    except NoCredentialsError as e:
        LOG.error("Credentials not available", e)
        return False
    return True


def write_to_s3(doc_dict, bucket, object_name):
    csv_file = "tmp/output.csv"
    LOG.info("Writing to csv...")
    did_write = _write_to_csv(csv_file, doc_dict)
    if not did_write:
        return False
    LOG.info("Done. Putting object...")
    success = _upload_file(csv_file, bucket, object_name)
    return success
