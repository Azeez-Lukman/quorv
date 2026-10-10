import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Safe auto-migrate on startup before serving requests
try:
    import django
    django.setup()
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception:
    pass

# Import and instantiate WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


