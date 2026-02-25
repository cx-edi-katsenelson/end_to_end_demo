import os
from gunicorn.app.base import BaseApplication

# Gunicorn configuration file 
# Updated for gunicorn 23.0.0 - removed deprecated gunicorn_paste() method

bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True

# Log settings
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

class StandaloneApplication(BaseApplication):
    """Custom Gunicorn application for programmatic configuration"""
    
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()
        
        # Configuration updated for gunicorn 23.0.0 - deprecated paste integration removed
        print("Gunicorn configuration loaded successfully using BaseApplication interface")
    
    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)
    
    def load(self):
        return self.application

# Environment-based configuration
if os.getenv('ENVIRONMENT') == 'production':
    workers = int(os.getenv('GUNICORN_WORKERS', 4))
    loglevel = 'warning'
else:
    workers = 2
    loglevel = 'debug'
