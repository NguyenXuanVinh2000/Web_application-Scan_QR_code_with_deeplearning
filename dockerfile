FROM python:3
FROM tensorflow/serving:1.15.0-gpu


COPY ./models/ /models/

COPY ./models.config /models/models.config
ENV MODEL_CONFIG_FILE=/models/models.config


WORKDIR /code

ADD . /code

RUN apt-get update && apt-get install python3-pip -y

RUN pip3 install --upgrade setuptools && pip3 install --upgrade pip

