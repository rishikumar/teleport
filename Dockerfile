FROM python:3.6

COPY requirements.txt /
RUN \
    pip install -r /requirements.txt \
    && rm -rf requirements.txt

COPY . /teleport
WORKDIR /teleport

