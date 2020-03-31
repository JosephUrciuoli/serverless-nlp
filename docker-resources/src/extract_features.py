from bert_serving.client import BertClient
from bert_serving.server import BertServer
from bert_serving.server.helper import get_args_parser, get_shutdown_parser


class ExtractFeatures:
    def __init__(self, document):
        self._document = document
        self._server = BertServer(
            get_args_parser().parse_args(
                ["-model_dir", "bert/uncased_L-12_H-768_A-12", "-port", "5555"]
            )
        )
        self._server.start()
        self._bc = BertClient()

    def encode(self):
        text_lines = [line.text for line in self._document.lines]
        encodings = self._bc.encode(text_lines)
        print(encodings)
        for (line, encoding) in zip(self._document.lines, encodings):
            line.encoding = encoding
            print("line after adding encoding", line)
        return self._document

    def end(self):
        self._bc.close()
        shut_args = get_shutdown_parser().parse_args(["-port", "5555"])
        BertServer.shutdown(shut_args)
