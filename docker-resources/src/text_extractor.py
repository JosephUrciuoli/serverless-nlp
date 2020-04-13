"""

This module is used to extract text from PDF documents. The OCRing of the document
is done with AWS' managed service, textract. The result of textract is then dumped
into a Document object for use with other modules in the app.

Example:
        text_extractor = TextExtractor()
        text = extractor.extract(bucket=BUCKET_NAME, key=DOCUMENT_NAME) # returns a Document

"""

import time
import logging
from .utils import get_client
from .types import Line, Document

LOG = logging.getLogger("serverless-nlp")


class TextExtractor:
    """Uses AWS textract to OCR documents and then store them in Document objects

        Attributes:
            _client (AWS Textract Client): Connection to the AWS textract service via boto3

    """

    def __init__(self):
        self._client = get_client("textract")

    def extract(self, bucket: str = None, key: str = None):
        """ main function to run functions that extract the text from a given document
              Args:
                bucket: the S3 bucket
                key: the name (directories + filename) in the S3 bucket of the document

            Returns:
                Document with extracted text for success, None otherwise
        """
        if not all([bucket, key]):
            raise ValueError("Bucket and Key required to extract.")
        LOG.info(f"Extracting document {key} from {bucket}.")

        job_id = self._start_job(bucket, key)
        if not job_id:
            return None

        final_status = self._poll_job(job_id)
        LOG.info(f"Final status of job {final_status}.")

        pages = self._get_results(job_id)

        document = _structure_doc(pages)
        return document

    def _poll_job(self, job_id: str) -> str:
        """ polls for the status of the textract job
              Args:
                job_id: the job ID of the textract conversion process

            Returns:
                status: the status of the textract job
        """
        if not job_id:
            raise ValueError("Job ID required to monitor.")
        LOG.info(f"Monitoring job: {job_id}")

        status = "IN_PROGRESS"
        while status == "IN_PROGRESS":
            time.sleep(3)
            response = self._client.get_document_text_detection(JobId=job_id)
            status = response["JobStatus"]
            LOG.info(f"Job status: {status}")

        return status

    def _start_job(self, bucket: str, key: str) -> str:
        """ submits the job to the textract service
              Args:
                bucket: the S3 bucket
                key: the name (directories + filename) in the S3 bucket of the document

            Returns:
                job_id: the id of the textract job
        """
        try:
            response = self._client.start_document_text_detection(
                DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
            )
        except Exception as e:
            LOG.error(
                f"Unable to extract document {key} from {bucket}. Error: {str(e)}"
            )
            raise e

        return response["JobId"]

    def _get_results(self, job_id: str) -> list:
        """ retrieves the results of the textract job

              Args:
                job_id: the job id of the textract job

            Returns:
                pages: list of pages and associated content from the textract job
        """
        pages = []
        response = self._client.get_document_text_detection(JobId=job_id)

        pages.append(response)
        LOG.info("Resultset page received: 1")
        next_token = None
        if "NextToken" in response:
            next_token = response["NextToken"]

        while next_token:
            response = self._client.get_document_text_detection(
                JobId=job_id, NextToken=next_token
            )

            pages.append(response)
            LOG.info(f"Resultset page received: {len(pages)}")
            next_token = None
            if "NextToken" in response:
                next_token = response["NextToken"]

        return pages


def _structure_doc(pages: list) -> Document:
    """ takes data from the textract job and places it in a Document object

          Args:
            pages: list of pages and associated content from the textract job

        Returns:
            document: Document object with extracted data
    """
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
