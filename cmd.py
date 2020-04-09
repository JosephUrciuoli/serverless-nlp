import fire
import secrets
import os
import boto3
import pprint

# Documents to extract features from. This could be provide via API or other method in practice
DOCS = ["FL.1942.1.pdf", "FL.1943.10.pdf", "FL.1943.12.pdf"]


class Jobs:
    def __init__(self):
        args = {
            "region_name": "us-east-1",
            "aws_access_key_id": os.environ.get("aws_access_key_id"),
            "aws_secret_access_key": os.environ.get("aws_secret_access_key"),
        }
        self.batch_client = boto3.client("batch", **args)

    def submit_jobs(self):
        for doc in DOCS:
            hash = secrets.token_hex(4)
            print(f"Submitting job for {doc} with hash {hash}")
            job = self.batch_client.submit_job(
                jobName=f"serverless-nlp-extraction-{hash}",
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
