import os
from gunicorn.app.pasterapp import paste_server


def gunicorn_paste():
    """
    Uses the gunicorn_paste method available in gunicorn 21.2.0
    This method is deprecated in version 23.0.0
    """
    return paste_server


# Gunicorn configuration settings
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 2
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Use the gunicorn_paste function
paste_config = gunicorn_paste()
