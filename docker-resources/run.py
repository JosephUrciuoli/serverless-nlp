import os
import logging
from src.text_extractor import TextExtractor
from src.feature_extractor import FeatureExtractor
from src.utils import doc_to_dict, write_to_s3

BUCKET_NAME = os.environ.get("S3_BUCKET")
DOCUMENT_NAME = os.environ.get("S3_KEY")
FEATURE_DIRECTORY = "output/"

# create logger
LOG = logging.getLogger("serverless-nlp")
LOG.setLevel(logging.DEBUG)

# create console handler and set level to debug
CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)

# create formatter
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
CH.setFormatter(FORMATTER)

# add ch to logger
LOG.addHandler(CH)

if __name__ == "__main__":
    os.system(
        "bert-serving-start -model_dir bert/uncased_L-12_H-768_A-12/ -port=5555 &"
    )

    # extract necessary data from the document
    extractor = TextExtractor()
    text = extractor.extract(bucket=BUCKET_NAME, key=DOCUMENT_NAME)

    # retrieve features from the document
    ef = FeatureExtractor(text)
    encoded_doc = ef.encode()
    ef.end()

    # format the document into a dataframe
    doc = doc_to_dict(text)
    csv_name = DOCUMENT_NAME.split("/")[-1].replace("pdf", "csv")
    res = write_to_s3(doc, BUCKET_NAME, f"output/{csv_name}")
    LOG.debug(
        f'Attempted to write result to {BUCKET_NAME + "/output/" + csv_name}. Result: {"SUCCCESS" if res else "FAIL"}'
    )
