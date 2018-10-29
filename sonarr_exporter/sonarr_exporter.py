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

import argparse
import requests
import threading

from prometheus_metrics import exporter, generate_latest


class sonarr_exporter(exporter):
    def __init__(self, url, api_key):
        super().__init__()
        self.url = url + '/api'
        self.api_key = api_key
        self.metrics_handler.add_metric('sonarr_series')
        self.metrics_handler.add_metric('sonarr_wanted_missing')
        self.metrics_handler.add_metric('sonarr_queue')
        #self.metrics_handler.add_metric('sonarr_coming_episodes')

    def get_from_api(self, url, data={}):
        headers = {'X-Api-Key': self.api_key}
        res = requests.get(url, headers=headers, json=data)
        return res

    def add_update_metric(self, name):
        res = self.get_from_api('%s/%s' % (self.url, name))
        print(res)
        value = len(res.json())
        print(value)
        self.metrics_handler.update_metric('sonarr_%s' % name.replace('/', '_'), value)

    def generate_latest(self):
        self.add_update_metric('series')
        self.add_update_metric('wanted/missing')
        self.add_update_metric('queue')
        #self.add_update_metric('coming_episodes')
        return generate_latest()

    def make_wsgi_app(self):
        def prometheus_app(environ, start_response):
            output = self.generate_latest()
            status = str('200 OK')
            headers = [(str('Content-type'), str('text/plain'))]
            start_response(status, headers)
            return [output]

        return prometheus_app

def main():
    parser = argparse.ArgumentParser(description='sonarr_exporter')
    parser.add_argument(
        '-s',
        '--sonarr',
        help='sonarr address',
        default='http://localhost:8989')
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
