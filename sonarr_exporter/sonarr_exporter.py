#!/usr/bin/env python3
#
# Copyright 2018 Daniel Schmitz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__VERSION__ = '0.1.dev0'

import argparse
import requests
import threading

from prometheus_client import Gauge, generate_latest
from wsgiref.simple_server import make_server, WSGIRequestHandler, WSGIServer


class sonarr_exporter:
    class _SilentHandler(WSGIRequestHandler):
        """WSGI handler that does not log requests."""

        def log_message(self, format, *args):
            """Log nothing."""

    def __init__(self, url, api_key):
        self.url = url + '/api'
        self.api_key = api_key
        self.metrics_data = dict()
        self.metrics = dict()

    def get_from_api(self, url, data={}):
        headers = {'X-Api-Key': self.api_key}
        res = requests.get(url, headers=headers, json=data)
        return res

    def get_data(self):
        res = self.get_from_api('%s/series' % self.url)
        self.metrics_data['series'] = len(res.json())

        res = self.get_from_api('%s/wanted/missing/' % self.url)
        self.metrics_data['wanted_missing'] = len(res.json())

        res = self.get_from_api('%s/queue' % self.url)
        self.metrics_data['queue'] = len(res.json())

        res = self.get_from_api('%s/calendar' % self.url)
        self.metrics_data['coming_episodes'] = len(res.json())

    def generate_latest(self):
        self.get_data()
        for metric in self.metrics_data:
            if not metric in self.metrics:
                self.metrics[metric] = Gauge('sonarr_%s' % metric.lower(),
                                             metric.replace('_', ' '))
            self.metrics[metric].set(self.metrics_data[metric])

        return generate_latest()

    def make_prometheus_app(self):
        def prometheus_app(environ, start_response):
            output = self.generate_latest()
            status = str('200 OK')
            headers = [(str('Content-type'), str('text/plain'))]
            start_response(status, headers)
            return [output]

        return prometheus_app

    def make_server(self, interface, port):
        server_class = WSGIServer

        if ':' in interface:
            if getattr(server_class, 'address_family') == socket.AF_INET:
                server_class.address_family = socket.AF_INET6

        print("* Listening on %s:%s" % (interface, port))
        self.httpd = make_server(
            interface,
            port,
            self.make_prometheus_app(),
            server_class=server_class,
            handler_class=self._SilentHandler)
        t = threading.Thread(target=self.httpd.serve_forever)
        t.start()


def main():
    parser = argparse.ArgumentParser(description='sonarr_exporter')
    parser.add_argument(
        '-s', '--sonarr', help='sonarr address', default='http://localhost:8989')
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        help='port sonarr_exporter is listening on',
        default=9314)
    parser.add_argument(
        '-i',
        '--interface',
        help='interface sonarr_exporter will listen on',
        default='0.0.0.0')
    parser.add_argument(
        '-a', '--api-key', help='sonarr api token', default=None)
    args = parser.parse_args()

    exporter = sonarr_exporter(args.sonarr, args.api_key)
    exporter.make_server(args.interface, args.port)


if __name__ == '__main__':
    main()
