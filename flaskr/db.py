import sqlite3
from datetime import datetime

import click
from flask import current_app
from flask import g

# g is a namespace object that can store data during an application context.
# This is a good place to store resources during a request.

# A proxy to the application handling the current request.
# This is useful to access the application without needing to import it, or if it can’t be imported,


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


# click.command defines a command line command that calls the function it decorates.
# It can be called with
#   flask --app flaskr init-db


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables"""
    init_db()
    click.echo("Initialized the database")


# Tell python to interpret timestamps as datetime.datetime
sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


# Register the init and close db functions with the app
# app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
# app.cli.add_command() adds a new command that can be called with the flask command.


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
