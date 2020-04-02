from bert_serving.client import BertClient


class FeatureExtractor:
    def __init__(self, document):
        self._document = document
        self._bc = BertClient()

    def encode(self):
        text_lines = [line.text for line in self._document.lines]
        encodings = self._bc.encode(text_lines)
        for (line, encoding) in zip(self._document.lines, encodings):
            line.encoding = encoding
        return self._document

    def end(self):
        self._bc.close()
