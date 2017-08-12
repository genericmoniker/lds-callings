from flask import Flask

from back.log import setup_logging, banner

app = Flask(__name__)
setup_logging(app.logger)
banner(app.logger, ' web ')

# Imports to ensure the web application is set up:
import back.views


# Debugging entry point -- in production we run through gunicorn.
if __name__ == "__main__":
    app.run()
