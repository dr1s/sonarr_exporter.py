FROM alpine:3.8
MAINTAINER dr1s

RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip setuptools && \
    pip3 install virtualenv

WORKDIR /sonarr_exporter

COPY . /sonarr_exporter

RUN virtualenv -p python3 /env && \
    /env/bin/python3 setup.py install && \
    rm -rf /sonarr_exporter

EXPOSE 9314

ENTRYPOINT ["/env/bin/sonarr_exporter"]
