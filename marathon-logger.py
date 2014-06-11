#!/usr/bin/env python

import argparse
import atexit
import collections
import sys

from flask import Flask, request, jsonify

import marathon

app = Flask(__name__)
events = None  # re-initialize later

def on_exit(marathon_client, callback_url):
    marathon_client.delete_event_subscription(callback_url)

def record_event(event):
    events.append(event)
    print event

@app.route('/events', methods=['POST'])
def event_receiver():
    event = request.get_json()
    record_event(event)
    return ""

@app.route('/events', methods=['GET'])
def list_events():
    return jsonify({'events': list(events)})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Marathon Logging Service')
    parser.add_argument('-m', '--marathon-url', help='Marathon server URL (http[s]://<host>:<port>[<path>])')
    parser.add_argument('-c', '--callback-url', help='callback URL for this service (http[s]://<host>:<port>[<path>]/events')
    parser.add_argument('-l', '--max-length', help='Max number of events to store in memory (default: 100)', type=int, default=100)
    parser.add_argument('-p', '--port', help='Port to listen on (default: 5000)', type=int, default=5000)
    args = parser.parse_args()

    if not args.marathon_url:
        print "Marathon URL must be passed"
        sys.exit(1)

    if not args.callback_url:
        print "Callback URL must be passed"
        sys.exit(1)

    events = collections.deque(maxlen=args.max_length)
    m = marathon.MarathonClient(args.marathon_url)
    m.create_event_subscription(args.callback_url)
    atexit.register(on_exit, m, args.callback_url)

    app.run(port=args.port)
