"""

This module is used to extract features from the lines extracted from documents
using BERT encodings. This package leverages the bert-as-a-server package to create the
embeddings.

Example:
        feature_extractor = FeatureExtractor(document) # document is of class Document
        encoded_doc = feature_extractor.encode()
        feature_extractor.end()

Todo:
    * lines --> sentences for a better representation of the embeddings
    * try different BERT models
    * train the BERT model for a specific task before encoding


"""

from bert_serving.client import BertClient


class FeatureExtractor:
    """Uses Bert-as-a-Server to set up a BertClient and embed text in a Document.

        Attributes:
            document (Document): This object encompasses the extracted text from one of the
                PDF documents. There is an encoding field on each Line which is where the
                embedding from BERT will be included, and where the text that gets encoded will
                be provided.
            _bc (BertClient): Connection to the BertServer which can be used for encoding.

    """

    def __init__(self, document):
        self._document = document
        self._bc = BertClient()

    def encode(self):
        """ encodes the text in the Document object, and then adds it to the encoding attribute """
        text_lines = [line.text for line in self._document.lines]
        encodings = self._bc.encode(text_lines)
        for (line, encoding) in zip(self._document.lines, encodings):
            line.encoding = encoding
        return self._document

    def end(self):
        """ Closes the BertClient connection to BertServer """
        self._bc.close()
