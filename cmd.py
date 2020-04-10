"""

This module is used to kick off AWS Batch Jobs for the serverless-nlp project via fire. This module
assumes that all previous setup in both AWS and Docker have been completed. The submit_jobs
function is used to mock up a scenario such as hitting an API with several documents that need to
be OCRed and have features extracted.

Example:
        $ python cmd.py submit_jobs

"""
import pprint
import secrets
import os

import fire
import boto3


# Documents to extract features from. This could be provide via API or other method in practice
DOCS = ["FL.1942.1.pdf", "FL.1943.10.pdf", "FL.1943.12.pdf"]


class Jobs:
    """ Jobs is a class which is used to provide a CLI to users to kick of available functions.

        In order to run used this class, you'll need to have AWS access keys defined in your
        environment to set up the AWS Batch client.

    """

    def __init__(self):
        args = {
            "region_name": "us-east-1",
            "aws_access_key_id": os.environ.get("aws_access_key_id"),
            "aws_secret_access_key": os.environ.get("aws_secret_access_key"),
        }
        self.batch_client = boto3.client("batch", **args)

    def submit_jobs(self):
        """Kicks off the AWS Batch Jobs."""
        for doc in DOCS:
            _hash = secrets.token_hex(4)
            print(f"Submitting job for {doc} with hash {_hash}")
            job = self.batch_client.submit_job(
                jobName=f"serverless-nlp-extraction-{_hash}",
                jobQueue="serverless-nlp-jobqueue",
                jobDefinition="serverless-nlp-jobdefinition:4",
                containerOverrides={
                    "command": ["python", "run.py"],
                    "environment": [
                        {"name": "env", "value": "prod"},
                        {"name": "S3_KEY", "value": f"documents/{doc}"},
                        {"name": "S3_BUCKET", "value": "serverless-nlp"},
                    ],
                },
            )
            print("Job Submitted: ")
            pprint.pprint(job)


if __name__ == "__main__":
    fire.Fire(Jobs)
