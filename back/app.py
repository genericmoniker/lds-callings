from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from back.log import setup_logging, banner

app = Flask(__name__)
app.config.from_object('back.config')
setup_logging(app.logger)
banner(app.logger, ' web ')
db = SQLAlchemy(app)

import back.views  # Import views to add routes.
