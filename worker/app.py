from application.database import Database

db = None


def create_app():
    global db
    db = Database()
