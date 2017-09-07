from web.app import create_app

create_app()

# Add views to the app...
from web.views import *

# gUnicorn takes over at this point.
