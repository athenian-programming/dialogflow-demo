import logging
import platform
import sys
import time


def add_http_prefix(url):
    return url if url.startswith('http://') or url.startswith('https://') else 'http://' + url


def is_raspi():
    return platform.system() == 'Linux'


def is_windows():
    return sys.platform == 'win32'


def is_python3():
    return sys.version_info[0] >= 3


def current_time_millis():
    return int(round(time.time() * 1000))


def waitForKeyboardInterrupt():
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass


def setup_logging(filename=None,
                  filemode='a',
                  stream=sys.stderr,
                  level=logging.INFO,
                  format='%(asctime)s %(name)-10s %(funcName)-10s():%(lineno)i: %(levelname)-6s %(message)s'):
    if filename:
        logging.basicConfig(filename=filename, filemode=filemode, level=level, format=format)
    else:
        logging.basicConfig(stream=stream, level=level, format=format)
