FROM dr1s/pipenv-alpine:3.8-python3.7

COPY sonarr_exporter/sonarr_exporter.py sonarr_exporter.py

EXPOSE 9314

ENTRYPOINT python3 sonarr_exporter.py
