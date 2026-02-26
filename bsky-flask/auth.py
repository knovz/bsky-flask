"""Blueprint with auth related endpoints"""

import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
from atproto import Client

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        # We'll try to login with bluesky credentials
        username = request.form["username"]
        password = request.form["password"]

        bsky = Client()
        profile_view = bsky.login(username, password)
        current_app.logger.info(
            "Logged in as %s (@%s)",
            profile_view.display_name,
            profile_view.handle,
        )
        # TODO handle errors
        session.clear()
        session["user_id"] = profile_view.handle
        # persist client or tokens
        return redirect(url_for("index"))

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    """bp.before_app_request register the function to run before any view function, at each request"""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = {"id": user_id}


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    """decorator for views that require a user to be logged in"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
