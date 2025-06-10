import sqlite3
from datetime import datetime

import click

# current_app -> points to the Flask app handling the request
# g -> special object unique for each request
from flask import current_app, g

def get_db():
    if 'db' not in g:
        # Connect to the specified SQLite DB
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # Return rows that behave like dicts.
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Closes the DB connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # Open the schema file and execute it
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# A command that calls `init_db()` and prints a success message
@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Database initialized.')


# Convert sqlite3 timestamp values to `datetime.datetime`
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    """Registeres the `close_db` and init_db_command` functions."""

    # Call the `close_db()` functions when cleaning up
    app.teardown_appcontext(close_db)

    # Add the `init_db_command()` to be called with the flask command
    app.cli.add_command(init_db_command)