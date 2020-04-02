import os
import boto3
import pandas as pd
from io import StringIO
from botocore.exceptions import ClientError


def _get_aws_args():
    args = {"region_name": "us-east-1"}
    if os.environ.get("env", "dev") == "dev":
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


def doc_to_dataframe(doc):
    print('Unpacking to dictionary...')
    doc_dict = [line.__dict__ for line in doc.lines]
    for line in doc_dict:
        encoding_dict = {f"feat_{index}": val for index, val in enumerate(line["encoding"])}
        line.update(encoding_dict)
        del line["encoding"]
    print('Done. Exporting to DataFrame...')
    df = pd.DataFrame(doc_dict)
    print('Dataframe: ', df.head())
    return df


def write_to_s3(df, bucket, object_name):
    s3_client = get_client("s3")
    csv_buf = StringIO()
    print('Writing to buffer...')
    df.to_csv(csv_buf,index=False)
    print('Done. Putting object...')
    csv_buf.seek(0)
    try:
        response = s3_client.put_object(
            Bucket=bucket, Body=csv_buf.getvalue(), Key=object_name
        )
        print('Done', response)
    except ClientError as e:
        print(e)
        return False
    return True
