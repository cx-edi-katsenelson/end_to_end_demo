"""
Gunicorn configuration file with deprecated gunicorn_paste() method
Available in gunicorn 21.2.0, deprecated in 23.0.0
"""

import multiprocessing
from gunicorn.app.pasterapp import paste_server


# Server socket
bind = "0.0.0.0:5000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


def gunicorn_paste():
    """
    Deprecated method for Paste deployment compatibility
    Available in gunicorn 21.2.0, deprecated in 23.0.0
    
    This function provides backward compatibility with Paste-based deployments
    """
    # Configuration for paste deployment
    paste_config = {
        'use': 'egg:gunicorn#main',
        'host': '0.0.0.0',
        'port': '5000',
    }
    return paste_config


# Call the deprecated method to demonstrate its usage
paste_configuration = gunicorn_paste()
