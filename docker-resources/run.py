import os
import logging
from src.text_extractor import TextExtractor
from src.feature_extractor import FeatureExtractor
from src.utils import doc_to_dict, write_to_s3

s3BucketName = "serverless-nlp"
documentName = "documents/FL.1943.12.pdf"
feature_directory = "output/"

# create logger
LOG = logging.getLogger('serverless-nlp')
LOG.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
LOG.addHandler(ch)

if __name__ == "__main__":
    os.system(
        "bert-serving-start -model_dir bert/uncased_L-12_H-768_A-12/ -port=5555 &"
    )

    # extract necessary data from the document
    extractor = TextExtractor()
    text = extractor.extract(bucket=s3BucketName, key=documentName)

    # retrieve features from the document
    ef = FeatureExtractor(text)
    encoded_doc = ef.encode()
    ef.end()

    # format the document into a dataframe
    doc = doc_to_dict(text)
    res = write_to_s3(doc, s3BucketName, "output/FL.1943.12.csv")
    LOG.debug(
        f'Attempted to write result to {s3BucketName + "/output/FL.1943.12.csv"}. Result: {"SUCCCESS" if res else "FAIL"}'
    )
