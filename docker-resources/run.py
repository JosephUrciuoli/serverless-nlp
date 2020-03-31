from src.text_extractor import TextExtractor
from src.extract_features import ExtractFeatures

s3BucketName = "serverless-nlp"
documentName = "documents/FL.1943.12.pdf"

if __name__ == "__main__":
    # extract necessary data from the document
    extractor = TextExtractor()
    text = extractor.extract(bucket=s3BucketName, key=documentName)

    # retrieve features from the document
    ef = ExtractFeatures(text)
    encoded_doc = ef.encode()
    print(encoded_doc)
    ef.end()
