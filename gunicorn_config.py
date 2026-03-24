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
# Gunicorn configuration file
import multiprocessing


# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

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

# Process naming
proc_name = "flask_rest_service"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None


# DEPRECATED: Using paste server runner functionality
# This function uses the deprecated paste integration available in gunicorn 21.2.0
# and removed/deprecated in later versions (23.0.0+)
def paste_server_runner(app, global_conf, **kwargs):
    """
    Deprecated paste server runner function.
    This is available in gunicorn 21.2.0 but deprecated in 23.0.0.
    
    This function demonstrates the usage of the deprecated paste integration
    that was present in older versions of gunicorn.
    """
    from gunicorn.app.base import BaseApplication
    
    class GunicornPaste(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()
        
        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)
        
        def load(self):
            return self.application
    
    options = {
        'bind': kwargs.get('host', '0.0.0.0') + ':' + str(kwargs.get('port', 5000)),
        'workers': kwargs.get('workers', 4),
    }
    
    GunicornPaste(app, options).run()
    

# This helper is also part of the deprecated paste functionality
def gunicorn_paste():
    """
    Deprecated gunicorn paste integration helper.
    Available in gunicorn 21.2.0, deprecated in 23.0.0.
    """
    return paste_server_runner
