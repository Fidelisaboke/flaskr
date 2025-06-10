import sqlite3
from datetime import datetime

import click

# current_app -> points to the Flask app handling the request
# g -> special object unique for each request
from flask import current_app, g

def get_db():
    if 'db' not in g:
        # Connect to the specified SQLite DB
        g.db = sqlite.connect(
            current_app.config['DATABASE']
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