from sqlalchemy import text

from back.app import db


def ensure_tenant(unit):
    sql = text(f"CREATE SCHEMA IF NOT EXISTS unit_{unit};")
    db.engine.execute(sql.execution_options(autocommit=True))
    db.create_all()


def activate_tenant(user):
    sql = text(f"SET search_path TO {user.tenant};")
    db.engine.execute(sql.execution_options(autocommit=True))
