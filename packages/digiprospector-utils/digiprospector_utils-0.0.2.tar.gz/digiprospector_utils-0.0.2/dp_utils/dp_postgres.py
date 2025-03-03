from sqlalchemy import MetaData, Table
from sqlalchemy.inspection import inspect
from sqlalchemy.dialects import postgresql

def upsert(engine, db_session, schema, table_name, records=[]):

    metadata = MetaData(schema=schema)
    metadata.bind = engine

    table = Table(table_name, metadata, schema=schema, autoload_with=engine)

    # get list of fields making up primary key
    primary_keys = [key.name for key in inspect(table).primary_key]

    # assemble base statement
    stmt = postgresql.insert(table).values(records)

    # define dict of non-primary keys for updating
    update_dict = {
        c.name: c
        for c in stmt.excluded
        if not c.primary_key
    }

    # cover case when all columns in table comprise a primary key
    # in which case, upsert is identical to 'on conflict do nothing.
    if update_dict == {}:
        return None


    # assemble new statement with 'on conflict do update' clause
    update_stmt = stmt.on_conflict_do_update(
        index_elements=primary_keys,
        set_=update_dict,
    )

    # execute
    result = db_session.execute(update_stmt)
    db_session.commit()
    return result

