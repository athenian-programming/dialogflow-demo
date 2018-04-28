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

from session import Session

install_aliases()

import json
import os
from question import Question
import argparse
import logging
from flask import Flask
from flask import request
from flask import make_response
from utils import setup_logging
from flask import Response

PORT = 'port'
LOG_LEVEL = 'loglevel'

logger = logging.getLogger(__name__)

# Flask app should start in global layout
http = Flask(__name__)


@http.route('/', methods=['GET'])
def root():
    return Response('Hello World!', mimetype='text/plain')


@http.route('/test', methods=['GET'])
def test():
    return Response('You have reached the test endpoint', mimetype='text/plain')


@http.route('/sessions', methods=['GET'])
def sessions():
    global sessions
    resp = str(len(sessions)) + ' current sessions:\n' + str([("Session: " + str(s)) for s in sessions.values()])
    return Response(resp, mimetype='text/plain')


@http.route('/webhook', methods=['POST'])
def webhook():
    global sessions

    req = request.get_json(silent=True, force=True)

    print("The request is:")
    print(json.dumps(req, indent=4))

    # Lookup info in database
    session_id = req["session"]

    # Add to sessions map if not present
    if (session_id not in sessions):
        try:
            source = req["originalDetectIntentRequest"]["payload"]["source"]
        except KeyError:
            source = "unknown"

        sessions[session_id] = Session(session_id, source)

    intent = req["queryResult"]["intent"]["displayName"]
    if (intent == "questions"):
        answer = "What do you think about gun control"
    else:
        answer = "This is my response to: " + req["queryResult"]["queryText"]

    resp = {"fulfillmentText": answer}

    print("\n\nResponding with:")
    resp = json.dumps(resp, indent=4)
    print(resp)
    print("\n\n")

    r = make_response(resp)
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


def load_dummy_data():
    global questions, sessions
    questions = [Question("What do you thing about gun control 1"),
                 Question("What do you thing about gun control 2"),
                 Question("What do you thing about gun control 3"),
                 Question("What do you thing about gun control 4"),
                 Question("What do you thing about gun control 5")]

    sessions = {}


if __name__ == '__main__':
    load_dummy_data()
    main()
