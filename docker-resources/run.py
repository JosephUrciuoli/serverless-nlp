from src.text_extractor import TextExtractor
from src.extract_features import ExtractFeatures
from src.utils import doc_to_dataframe, write_to_s3
import os

s3BucketName = "serverless-nlp"
documentName = "documents/FL.1943.12.pdf"
feature_directory = "output/"

if __name__ == "__main__":
    os.system(
        "bert-serving-start -model_dir bert/uncased_L-12_H-768_A-12/ -port=5555 &"
    )

    # extract necessary data from the document
    extractor = TextExtractor()
    text = extractor.extract(bucket=s3BucketName, key=documentName)

    # retrieve features from the document
    ef = ExtractFeatures(text)
    encoded_doc = ef.encode()
    ef.end()

    # format the document into a dataframe
    df = doc_to_dataframe(text)
    res = write_to_s3(df, s3BucketName, "output/FL.1943.12.csv")
    print(
        f'Attempted to write result to {s3BucketName + "/output/FL.1943.12.csv"}. Result: {"SUCCCESS" if res else "FAIL"}'
    )
