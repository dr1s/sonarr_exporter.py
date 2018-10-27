FROM alpine:3.8

RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip setuptools && \
    pip3 install pipenv

WORKDIR /exporter

COPY sonarr_exporter/sonarr_exporter.py sonarr_exporter.py
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --deploy --system

EXPOSE 9314

ENTRYPOINT python3 sonarr_exporter.py
