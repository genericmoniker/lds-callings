
# http://docs.sqlalchemy.org/en/latest/core/connections.html#schema-translating
# http://docs.sqlalchemy.org/en/latest/changelog/migration_11.html#multi-tenancy-schema-translation-for-table-objects
# https://stackoverflow.com/questions/42257428/flask-sqlalchemy-how-to-use-create-all-with-schema-translate-map


def ensure_tenant(db, tenant):
    db.engine.update_execution_options(
        schema_translate_map={None: f'unit_{tenant}'}
    )
    sql = f"CREATE SCHEMA IF NOT EXISTS unit_{tenant};"
    db.engine.execute(sql)
    db.create_all()


def activate_tenant(db, tenant):
    db.session.connection(execution_options={
        'schema_translate_map': {None: f'unit_{tenant}'}
    })
