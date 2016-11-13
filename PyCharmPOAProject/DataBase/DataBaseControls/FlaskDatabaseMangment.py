
import sqlite3
from flask import Flask, g

app = Flask(__name__)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    """
    will go to the schema flile
    :return: VOID
    """
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def show_entries(SQL):
    """
    Example show_entries('select title, text from entries order by id desc')
    :param SQL: SQL code that will call table info to be returned
    :return: entries form sql table look up
    """
    db = get_db()
    cur = db.execute(SQL)
    entries = cur.fetchall()
    return entries