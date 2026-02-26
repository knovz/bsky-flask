"""views blueprint. Index"""

from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("views", __name__)  # No prefix, this is the root


# Is there an "open" timeline? Or @login_required?
@bp.route("/")
def index():
    return render_template("views/timeline.html")
