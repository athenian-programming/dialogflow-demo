# !/usr/bin/env python
# -*- coding:utf8 -*-

from __future__ import print_function

from future.standard_library import install_aliases

from session import Session

install_aliases()

import json
import os
import argparse
import logging
import redis as Redis
from flask import Flask
from flask import request
from flask import make_response
from utils import setup_logging
from flask import Response
from flask import abort
from session import QUESTIONS

PORT = 'port'
LOG_LEVEL = 'loglevel'

logger = logging.getLogger(__name__)

# Flask app should start in global layout
http = Flask(__name__)

# REDIS_URL is defined when running on Heroku
if os.environ.get("REDIS_URL") == None:
    # REDIS_HOST is defined when running in docker compose
    redis = Redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0)
else:
    redis = Redis.from_url(os.environ.get("REDIS_URL"))


@http.route('/', methods=['GET'])
def root_endpoint():
    return Response('Hello World!!!', mimetype='text/plain')


@http.route('/test', methods=['GET'])
def test_endpoint():
    return Response('You have reached the test endpoint', mimetype='text/plain')


@http.route('/sessions', methods=['GET'])
def sessions_endpoint():
    q_cnt = len(QUESTIONS)

    # Initialize results map
    yes_results = {}
    no_results = {}
    unknown_results = {}
    for i in range(q_cnt):
        yes_results[i] = 0
        no_results[i] = 0
        unknown_results[i] = 0

    # Grab sessions from redis
    sessions = Session.all_sessions(redis)

    # Walk through sessions and count results
    for sv in sessions.values():
        for i in range(q_cnt):
            answer = sv.get_answer(i)
            if answer is None:
                continue
            elif answer.lower() == 'yes':
                yes_results[i] += 1
            elif answer.lower() == 'no':
                no_results[i] += 1
            else:
                unknown_results[i] += 1
                logger.info("Bad answer: " + answer)

    # Display all the results
    resp = "Results: \n"
    for i in range(q_cnt):
        resp += str(QUESTIONS[i])
        resp += "YES" + str(yes_results[i])
        resp += "NO" + str(no_results[i])
        resp += "UNKNOWN" + str(unknown_results[i])

    # Display all the sessions
    resp += '{} current sessions:\n'.format(len(sessions))
    for sv in sessions.values():
        resp += '\n' + str(sv)
    return Response(resp, mimetype='text/plain')


@http.route('/results', methods=['GET'])
def results_endpoint():
    resp = '''
    <html>
        <head>
        </head>
        <body>
            <h1>These are the results:</h1>
        </body>
    </html>
    '''
    return Response(resp, mimetype='text/html')


# Require password with: http://localhost:8080/reset?password=secret
@http.route('/reset', methods=['GET'])
def reset():
    if not request.args or 'password' not in request.args or request.args['password'] != 'secret':
        abort(400)
    Session.clear_all(redis)
    return Response('Sessions reset.', mimetype='text/plain')


@http.route('/webhook', methods=['POST'])
def webhook():
    global redis

    req = request.get_json(silent=True, force=True)

    print('Request:')
    print(json.dumps(req, indent=4))

    session_id = req['session']

    # Add to sessions map if not present
    if (not Session.exists(redis, session_id)):
        try:
            source = req['originalDetectIntentRequest']['payload']['source']
        except KeyError:
            source = 'unknown source'
        Session.create(redis, session_id, source)

    session = Session.fetch(redis, session_id)

    intent = req['queryResult']['intent']['displayName']

    if (intent == 'questions'):
        fulfillment_text = session.next_question(None)
    elif (intent == 'questions.answer'):
        answer = req['queryResult']['queryText']
        fulfillment_text = session.next_question(answer)
    else:
        fulfillment_text = 'Unknown state'

    resp = json.dumps({'fulfillmentText': fulfillment_text}, indent=4)

    print('\n\nResponse:')
    print(resp)
    print('\n\n')

    retval = make_response(resp)
    retval.headers['Content-Type'] = 'application/json'
    return retval


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
    logger.info('Starting webhook listening on port {}'.format(port))
    http.run(debug=False, port=port, host='0.0.0.0')


if __name__ == '__main__':
    main()
