import uuid

from back.app import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer)

    def tenant(self):
        return str(self.unit)

    def generate_auth_token(self, expires_in=600):
        key = app.config['SECRET_KEY']
        return uuid.uuid4()  # TODO

    @staticmethod
    def verify_auth_token(token):
        return None  # TODO - if valid, return the user
