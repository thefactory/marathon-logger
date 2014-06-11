Event logging service for [Marathon](https://github.com/mesosphere/marathon) Mesos framework.

## Overview

marathon-logger is a Marathon event subscriber that logs each event it receives.

On launch, it registers itself with the Marathon server. On exit, it deregisters itself.

Each event is stored in-memory and printed to stdout, and the most recent `MAX_LENGTH` events available via a HTTP
`GET` to `/events`.

## Usage

### Running the service
```console
$ python marathon-logger.py -h
usage: marathon-logger.py [-h] [-m MARATHON_URL] [-c CALLBACK_URL]
                          [-l MAX_LENGTH] [-p PORT]

Marathon Logging Service

optional arguments:
  -h, --help            show this help message and exit
  -m MARATHON_URL, --marathon-url MARATHON_URL
                        Marathon server URL (http[s]://<host>:<port>[<path>])
  -c CALLBACK_URL, --callback-url CALLBACK_URL
                        callback URL for this service
                        (http[s]://<host>:<port>[<path>]/events
  -l MAX_LENGTH, --max-length MAX_LENGTH
                        Max number of events to store in memory (default: 100)
  -p PORT, --port PORT  Port to listen on (default: 5000)
```

To start marathon-logger, simply run `marathon-logger.py` and provide the URL of the Marathon server and the addressable
callback URL of the service.

Example:
```bash
python marathon-logger.py \
    -m http://marathon.mycompany.com/ \
    -c http://marathon-logger.mycompany.com/events \
    -l 10000
```

### Retrieving events
The most recent `MAX_LENGTH` events are available via a HTTP `GET` to `/events`.

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