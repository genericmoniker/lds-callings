from sqlalchemy import text


def ensure_tenant(db, tenant):
    sql = text(f"CREATE SCHEMA IF NOT EXISTS unit_{tenant};")
    db.engine.execute(sql.execution_options(autocommit=True))
    activate_tenant(db, tenant)
    db.create_all()  # TODO: Fix "psycopg2.ProgrammingError: no schema has been selected to create i"


def activate_tenant(db, tenant):
    sql = text(f"SET search_path TO {tenant};")
    db.engine.execute(sql.execution_options(autocommit=True))
