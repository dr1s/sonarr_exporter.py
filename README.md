# sonarr_exporter.py

A prometheus exporter for sonarr written in Python 3.

# Content
- [sonarr_exporter.py](#sonarrexporterpy)
- [Content](#content)
- [Metrics Example](#metrics-example)
- [Setup](#setup)
	- [pip](#pip)
	- [manual](#manual)
	- [Docker](#docker)
		- [docker-hub](#docker-hub)
		- [manual](#manual)
- [Usage](#usage)
	- [Usage Example](#usage-example)
- [Prometheus config](#prometheus-config)

# Metrics Example

    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",major="3",minor="7",patchlevel="0",version="3.7.0"} 1.0
    # HELP sonarr_series series
    # TYPE sonarr_series gauge
    sonarr_series 56.0
    # HELP sonarr_wanted_missing wanted missing
    # TYPE sonarr_wanted_missing gauge
    sonarr_wanted_missing 6.0
    # HELP sonarr_queue queue
    # TYPE sonarr_queue gauge
    sonarr_queue 0.0
    # HELP sonarr_coming_episodes coming episodes
    # TYPE sonarr_coming_episodes gauge
    sonarr_coming_episodes 4.0

# Setup

## pip
    pip3 install --upgrade git+https://github.com/dr1s/sonarr_exporter.py.git

## manual
    git clone https://github.com/dr1s/sonarr_exporter.py.git
    cd sonarr_exporter.py
    pip3 install -r requirements.txt
    cd sonarr_exporter
    ./sonarr_exporter.py

## Docker

### docker-hub
    docker pull dr1s/sonarr_exporter
    docker run --net=host -t dr1s/sonarr_exporter

### manual
    git clone https://github.com/dr1s/sonarr_exporter.py.git
    docker build -t dr1s/sonarr_exporter .
    docker run -d -p 9314:9314 -t dr1s/sonarr_exporter

# Usage
    usage: sonarr_exporter.py [-h] [-s SONARR] [-p PORT] [-i INTERFACE]
                              [-a API_KEY]

    sonarr_exporter

    optional arguments:
      -h, --help            show this help message and exit
      -s SONARR, --sonarr SONARR
                            sonarr address
      -p PORT, --port PORT  port sonarr_exporter is listening on
      -i INTERFACE, --interface INTERFACE
                            interface sonarr_exporter will listen on
      -a API_KEY, --api-key API_KEY
                            sonarr api token

## Usage Example

    sonarr_exporter --sonarr http://localhost:8989 --interface 0.0.0.0 --port 9314 --api-key <api_key>

The previous used arguements are the default options. If nothing needs to be changed, sonarr_exporter can be started without arguments.

# Prometheus config
    - job_name: 'sonarr'
      static_configs:
      - targets: ['pi.hole:9314']
