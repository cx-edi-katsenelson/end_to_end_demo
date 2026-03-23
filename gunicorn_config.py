import os

# Gunicorn configuration file
# Note: Paste Deploy support (gunicorn.app.pasterapp) was removed in gunicorn 23.0.0
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
loglevel = "info"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


def gunicorn_paste():
    """
    Example usage of gunicorn_paste() method.
    
    TODO: gunicorn 23.0.0 removed Paste Deploy support (gunicorn.app.pasterapp).
    If Paste Deploy integration is needed, migrate to alternative configuration methods:
    - Use native gunicorn configuration (this file)
    - Use environment variables
    - Use command-line arguments
    
    This function retained for reference but Paste Deploy functionality is no longer available.
    """
    # Legacy paste configuration structure (for reference only)
    paste_config = {
        'use': 'egg:gunicorn#main',
        'host': '0.0.0.0',
        'port': '5000',
        'workers': 4,
    }
    return paste_config


# Call the function to demonstrate legacy configuration structure
paste_settings = gunicorn_paste()


def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting Gunicorn server")
    server.log.info(f"Using paste configuration: {paste_settings}")


def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading Gunicorn server")


def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Gunicorn server is ready. Spawning workers")


def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info(f"Worker being forked (pid: {worker.pid if hasattr(worker, 'pid') else 'unknown'})")


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"Worker spawned (pid: {worker.pid})")


def worker_exit(server, worker):
    """Called just after a worker has been exited."""
    server.log.info(f"Worker exited (pid: {worker.pid})")
