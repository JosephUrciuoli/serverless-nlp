from bert_serving.client import BertClient
from bert_serving.server import BertServer
from bert_serving.server.helper import get_args_parser
import os


class ExtractFeatures:
    def __init__(self, document):
        self._document = document
        self._server = BertServer(
            get_args_parser().parse_args(["-model_dir", "bert/uncased_L-12_H-768_A-12"])
        )
        self._server.start()
        self._bc = BertClient()
        print(self._bc.encode(["First do it", "then do it right", "then do it better"]))
        exit()
