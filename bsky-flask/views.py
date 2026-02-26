"""views blueprint. Index"""

from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    g,
)

bp = Blueprint("views", __name__)  # No prefix, this is the root


# Is there an "open" timeline? Or @login_required?
@bp.route("/")
def index():
    cursor = request.args.get("cursor", "", type="str")
    current_app.logger.info("cursor: %s", cursor)
    # We could manage the cursor in session
    # But this makes it more consistent to move to REST API

    # 2026-02-09T22:57:51.314Z
    if "bsky" in g:
        timeline = g.bsky.get_timeline(limit=4, cursor=cursor)
        # cursor = timeline.cursor
        feed = timeline.feed
        cursor = timeline.cursor
    else:
        feed = []
        cursor = None

    return render_template("views/timeline.html", feed=feed, cursor=cursor)
