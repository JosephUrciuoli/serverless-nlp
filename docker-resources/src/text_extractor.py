import boto3
import time
import os
from .types import Line, Document


# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DJHVHB#__sid=js0


class TextExtractor:
    def __init__(self):
        args = {"region_name": "us-east-1"}
        if os.environ.get("env", "dev") == "dev":
            # only provide credentials in local versions - IAM role used in prod
            args.update(
                {
                    "aws_access_key_id": os.environ.get("aws_access_key_id"),
                    "aws_secret_access_key": os.environ.get("aws_secret_access_key"),
                }
            )
        self._client = boto3.client("textract", **args)

    def extract(self, bucket=None, key=None):
        if not all([bucket, key]):
            raise ValueError("Bucket and Key required to extract.")
        print(f"Extracting document {key} from {bucket}.")

        job_id = self._start_job(bucket, key)
        if not job_id:
            return

        final_status = self._poll_job(job_id)
        print(f"Final status of job {final_status}.")

        pages = self._get_results(job_id)

        document = self._structure_doc(pages)
        return document

    def _structure_doc(self, pages):
        document = Document()
        for page in pages:
            for block in page["Blocks"]:
                if block["BlockType"] != "LINE":
                    continue
                line = Line(
                    id=block["Id"],
                    text=block["Text"],
                    confidence=block["Confidence"],
                    page=block["Page"],
                    geometry=block["Geometry"],
                )
                document.lines.append(line)
        return document

    def _poll_job(self, job_id):
        if not job_id:
            raise ValueError("Job ID required to monitor.")
        print(f"Monitoring job: {job_id}")

        status = "IN_PROGRESS"
        while status == "IN_PROGRESS":
            time.sleep(3)
            response = self._client.get_document_text_detection(JobId=job_id)
            status = response["JobStatus"]
            print(f"Job status: {status}")

        return status

    def _start_job(self, bucket, key):
        try:
            response = self._client.start_document_text_detection(
                DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
            )
        except Exception as e:
            print(f"Unable to extract document {key} from {bucket}. Error: {str(e)}")
            raise e

        return response["JobId"]

    def _get_results(self, job_id):
        pages = []
        response = self._client.get_document_text_detection(JobId=job_id)

        pages.append(response)
        print("Resultset page received: 1")
        next_token = None
        if "NextToken" in response:
            next_token = response["NextToken"]

        while next_token:
            response = self._client.get_document_text_detection(
                JobId=job_id, NextToken=next_token
            )

            pages.append(response)
            print(f"Resultset page received: {len(pages)}")
            next_token = None
            if "NextToken" in response:
                next_token = response["NextToken"]

        return pages
