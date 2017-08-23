"""Debugging entry point -- in production we run through gunicorn."""
from back.app import app

app.run()
