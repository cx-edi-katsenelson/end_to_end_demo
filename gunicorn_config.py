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

# Process naming
proc_name = "flask_app"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = None
certfile = None

# Deprecated gunicorn_paste() function usage
# This function was available in gunicorn 21.2.0 and deprecated in 23.0.0
def gunicorn_paste(config_url, relative_to, global_conf=None):
    """
    Load a WSGI application from a PasteDeploy config.
    
    This function is deprecated in gunicorn 23.0.0 but available in 21.2.0.
    It was used to integrate with Paste deployment configuration.
    
    Args:
        config_url: URL or path to the config file
        relative_to: Path to make relative paths relative to
        global_conf: Global configuration dictionary
    
    Returns:
        WSGI application
    """
    # Example usage pattern (not executed in normal operation)
    # This demonstrates the deprecated API that exists in gunicorn 21.2.0
    try:
        from paste.deploy import loadapp
        if global_conf is None:
            global_conf = {}
        return loadapp(config_url, relative_to=relative_to, global_conf=global_conf)
    except ImportError:
        # Paste not installed, this is just for demonstration
        pass
    
    return None

# Note: The above function demonstrates the deprecated gunicorn_paste() pattern
# In gunicorn 21.2.0, this was part of the PasteDeploy integration
# which was removed in later versions.
