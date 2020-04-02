FROM python:3.7
LABEL maintainer="Joe Urciuoli"
WORKDIR /usr/src/app

COPY docker-resources/ ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir bert
RUN wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip -O bert/uncased_L-12_H-768_A-12.zip \
&& cd bert && unzip uncased_L-12_H-768_A-12.zip && rm uncased_L-12_H-768_A-12.zip && cd -

