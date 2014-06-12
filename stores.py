import collections
import logging
import logging.handlers
import urlparse


class InMemoryStore(object):

    def __init__(self, url):
        qa = urlparse.parse_qs(url.query)
        max_length = int(qa.get('max_length', ['100'])[0])
        self.events = collections.deque(maxlen=max_length)

    def save(self, event):
        print event
        self.events.append(event)

    def list(self):
        return list(self.events)


class SyslogUdpStore(object):

    def __init__(self, url):
        server = url.netloc
        port = url.port or logging.handlers.SYSLOG_UDP_PORT
        address = (server, port)

        self.log = logging.getLogger('marathon-logger')
        facility = logging.handlers.SysLogHandler.LOG_USER
        h = logging.handlers.SysLogHandler(address, facility)
        f = logging.Formatter('marathon-logger: %(message)s')
        h.setFormatter(f)
        self.log.addHandler(h)
        self.log.setLevel(logging.getLevelName('INFO'))

    def save(self, event):
        self.log.info(event)

    def list(self):
        return []