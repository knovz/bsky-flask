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
from atproto import exceptions

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Present login form if GET.
    Login with Bsky credentials if POST.
    """
    if request.method == "POST":
        # We'll try to login with bluesky credentials
        username = request.form["username"]
        password = request.form["password"]

        bsky = Client()
        try:
            profile_view = bsky.login(username, password)
            current_app.logger.info(
                "Logged in as %s (@%s)",
                profile_view.display_name,
                profile_view.handle,
            )
            session.clear()
            session["user"] = {
                "handle": profile_view.handle,
                "display_name": profile_view.display_name,
            }
            session["bsky"] = bsky.export_session_string()
            return redirect(url_for("index"))
        except exceptions.UnauthorizedError as ue:
            current_app.logger.error("Unauthorized. %s", ue)
            flash(f"{ue.response.status_code} - {ue.response.content.message}")

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    """
    bp.before_app_request register the function to run before any view function,
    at each request
    """
    user = session.get("user")

    if user is None:
        g.user = None
        g.pop("bsky", None)
    else:
        g.user = user
        bsky = Client()
        bsky.login(session_string=session["bsky"])
        g.bsky = bsky


@bp.route("/logout")
def logout():
    """logout, clear session"""
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
