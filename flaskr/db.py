#DEFINE AND ACCESS THE DATABASE

#create a connection to SQLite

import sqlite3

import click

#current_app and g are special objects

#g is unique for each request as it's used to store data that may be accessed
#by multiple functions

#cirrent_app also handles requests

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g:

        #connects to the pointed file
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        
        #tells the connections to return rows that behave like dictionary
        g.db.row_factory = sqlite3.Row

    return g.db

#checks if a connection was created by checking if g.db was set
#closes connection if it exists, this will be called after each request
def close_db(e=None):
    db = g.pop("db",None)

    if db is not None:
        db.close()


