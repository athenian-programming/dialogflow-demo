# !/usr/bin/env python
# -*- coding:utf8 -*-

# Copyright 2017 Google Inc. All Rights Reserved.
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

from __future__ import print_function

from future.standard_library import install_aliases

install_aliases()

import argparse
import logging
import json
import os

from flask import Flask
from flask import request
from flask import Response
from flask import make_response
from utils import setup_logging

PORT = 'port'
LOG_LEVEL = 'loglevel'

logger = logging.getLogger(__name__)

# Flask app should start in global layout
http = Flask(__name__)


@http.route('/', methods=['GET'])
def home():
    return Response('Hello World!', mimetype='text/plain')


@http.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("The request is:")
    print(json.dumps(req, indent=4))

    # Lookup info in database

    speech = "This is my response to: " + req["result"]["resolvedQuery"]
    # res = processRequest(req)
    # res = {"fulfillmentText": speech,
    #       "source": "dialogflow-demo-webhook"}
    result = {"speech": speech}

    result = json.dumps(result, indent=4)
    print("\n\nThis is the response:")
    print(result)
    print("\n\n")

    r = make_response(result)
    r.headers['Content-Type'] = 'application/json'
    return r

def main():
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', dest=PORT, default=8080, help='HTTP port [8080]')
    parser.add_argument('-v', '--verbose', dest=LOG_LEVEL, default=logging.INFO, action='store_const',
                        const=logging.DEBUG, help='Enable debugging info')
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    port = int(os.environ.get('PORT', args[PORT]))
    logger.info("Starting webhook listening on port {}".format(port))
    http.run(debug=False, port=port, host='0.0.0.0')

if __name__ == '__main__':
    main()
