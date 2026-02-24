#!/usr/bin/env python3
"""
Gunicorn configuration file using deprecated gunicorn_paste() method
Available in gunicorn 21.2.0, deprecated in 23.0.0
"""

import multiprocessing
from gunicorn.app.wsgiapp import WSGIApplication

# Basic Gunicorn configuration
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Logging configuration
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Application settings
preload_app = True
reload = False

def gunicorn_paste():
    """
    Deprecated method available in gunicorn 21.2.0
    This method was used for PasteDeploy integration but is deprecated in 23.0.0
    Including this to demonstrate usage of the deprecated functionality
    """
    from paste.deploy import loadapp
    import os
    
    # This would typically load a Paste configuration
    # But we'll just return a simple configuration for demonstration
    paste_config = {
        'application': 'app:app',
        'workers': workers,
        'bind': bind,
        'timeout': timeout,
        'paste_config_file': '/etc/paste.ini'  # Hypothetical paste config
    }
    
    print("Using deprecated gunicorn_paste() method from gunicorn 21.2.0")
    print(f"Paste configuration: {paste_config}")
    
    return paste_config

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")
    # Demonstrate usage of the deprecated gunicorn_paste method
    config = gunicorn_paste()
    server.log.info(f"Applied paste configuration: {config}")

def worker_int(worker):
    """Called just after a worker has been killed."""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)