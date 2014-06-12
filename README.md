Event logging service for [Marathon](https://github.com/mesosphere/marathon) Mesos framework.

## Overview

marathon-logger is a Marathon event subscriber that logs each event to a pluggable event store.

On launch, it registers itself with the Marathon server. On exit, it deregisters itself.

## Usage

### Installing the requirements
You'll need the [flask](http://flask.pocoo.org/) and [marathon](https://github.com/thefactory/marathon-python) Python packages:
```bash
pip install -r requirements.txt
```

### Running the service
```console
$ python marathon-logger.py -h
usage: marathon-logger.py [-h] -m MARATHON_URL -c CALLBACK_URL
                          [-e EVENT_STORE] [-p PORT]

Marathon Logging Service

optional arguments:
  -h, --help            show this help message and exit
  -m MARATHON_URL, --marathon-url MARATHON_URL
                        Marathon server URL (http[s]://<host>:<port>[<path>])
  -c CALLBACK_URL, --callback-url CALLBACK_URL
                        callback URL for this service
                        (http[s]://<host>:<port>[<path>]/events
  -e EVENT_STORE, --event-store EVENT_STORE
                        event store connection string (default: in-
                        memory://localhost/)
  -p PORT, --port PORT  Port to listen on (default: 5000)
```

To start marathon-logger, simply run `marathon-logger.py` and provide the URL of the Marathon server and the addressable
callback URL of the service.

Example:
```bash
python marathon-logger.py \
    -m http://marathon.mycompany.com/ \
    -c http://marathon-logger.mycompany.com/events \
    -e in-memory://localhost/?max_length=1000
```

### Retrieving events
Events are available via a HTTP `GET` to `/events`. _Note: not available with the `syslog` store type_

Example (using [httpie](https://github.com/jakubroztocil/httpie)):
```console
$ http GET localhost:5000/events
HTTP/1.0 200 OK
Content-Length: 394
Content-Type: application/json
Date: Wed, 11 Jun 2014 16:47:43 GMT
Server: Werkzeug/0.9.6 Python/2.7.5

{
    "events": [
        {
            "appId": "myapp",
            "eventType": "status_update_event",
            "host": "mesos-slave1.mycompany.com",
            "ports": [
                31705
            ],
            "slaveId": "20140609-224851-3187802122-5050-1365-2",
            "taskId": "myapp_1-1402505159061",
            "taskStatus": "TASK_KILLED",
            "timestamp": "2014-06-11T16:47:17.850Z"
        }
    ]
}
```

## Event Stores

### In-Memory
Store up to `max_length` events in memory. Safe for multiple threads, but not for multiple processes.

Parameters:
* `max_length` - [optional, default: 100] max number of events to store

Example connection string
```
in-memory://localhost/?max_length=1000
```

### Syslog (UDP)
Forward events to a syslog server via UDP. This event store has no retrieval capability, so `GET /events` will always
return zero results.

Example connection string:
```
syslog://localhost:514/
```
