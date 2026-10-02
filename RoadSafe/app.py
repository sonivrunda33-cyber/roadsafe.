# =========================================================
# ROADSAFE - app.py
# =========================================================

import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory
)

from config import Config
from database.database import (
    db,
    User,
    Report,
    create_user,
    create_report,
    get_user_by_email,
    get_user_by_username,
    get_report_by_id
)
from utils.helpers import (
    save_uploaded_file,
    get_report_statistics,
    normalize_category,
    normalize_severity
)
from utils.validators import (
    validate_email,
    validate_password,
    validate_username,
    validate_name,
    validate_report,
    passwords_match
)

# =========================================================
# APP INITIALIZATION
# =========================================================

app = Flask(__name__)

app.config.from_object(Config)

# Database
db.init_app(app)


# =========================================================
# CREATE DATABASE
# =========================================================

with app.app_context():
    db.create_all()


# =========================================================
# CREATE UPLOAD DIRECTORY
# =========================================================

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# =========================================================
# TEMPLATE CONTEXT
# =========================================================

@app.context_processor
def inject_global_variables():
    """Make common variables available in templates."""

    from datetime import datetime

    return {
        "app_name": app.config.get(
            "APP_NAME",
            "RoadSafe"
        ),
        "current_year": datetime.now().year
    }


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():
    """RoadSafe homepage."""

    reports = Report.query.order_by(
        Report.created_at.desc()
    ).limit(6).all()

    all_reports = Report.query.all()

    stats = get_report_statistics(
        all_reports
    )

    return render_template(
        "index.html",
        reports=reports,
        stats=stats
    )


# =========================================================
# MAP
# =========================================================

@app.route("/map")
def map_page():
    """Display interactive road safety map."""

    reports = Report.query.order_by(
        Report.created_at.desc()
    ).all()

    reports_json = []

    for report in reports:

        reports_json.append({
            "id": report.id,
            "title": report.title,
            "category": report.category,
            "description": report.description,
            "severity": report.severity,
            "status": report.status,
            "latitude": report.latitude,
            "longitude": report.longitude,
            "address": report.address,
            "image": report.image
        })

    return render_template(
        "map.html",
        reports=reports,
        reports_json=reports_json,
        config=app.config
    )


# =========================================================
# REPORT
# =========================================================

@app.route(
    "/report",
    methods=["GET", "POST"]
)
def report():
    """Create a new road issue report."""

    # ---------------------------------------------
    # LOGIN CHECK
    # ---------------------------------------------

    if "user_id" not in session:

        flash(
            "Please login to report an issue.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # POST REQUEST
    # ---------------------------------------------

    if request.method == "POST":

        data = {

            "title": request.form.get(
                "title",
                ""
            ).strip(),

            "category": request.form.get(
                "category",
                ""
            ).strip(),

            "severity": request.form.get(
                "severity",
                ""
            ).strip(),

            "description": request.form.get(
                "description",
                ""
            ).strip(),

            "latitude": request.form.get(
                "latitude",
                ""
            ).strip(),

            "longitude": request.form.get(
                "longitude",
                ""
            ).strip()
        }


        # -----------------------------------------
        # VALIDATE REPORT
        # -----------------------------------------

        validation = validate_report(
            data
        )

        if not validation["valid"]:

            for error in validation["errors"].values():

                flash(
                    error,
                    "danger"
                )

            return render_template(
                "report.html"
            )


        # -----------------------------------------
        # LOCATION
        # -----------------------------------------

        address = request.form.get(
            "address",
            ""
        ).strip()


        # -----------------------------------------
        # IMAGE
        # -----------------------------------------

        image = request.files.get(
            "image"
        )

        image_filename = None

        if image and image.filename:

            image_filename = save_uploaded_file(
                image,
                app.config["UPLOAD_FOLDER"]
            )

            if image_filename is None:

                flash(
                    "Invalid image. "
                    "Use JPG, PNG or WEBP.",
                    "danger"
                )

                return render_template(
                    "report.html"
                )


        # -----------------------------------------
        # CREATE REPORT
        # -----------------------------------------

        try:

            new_report = create_report(

                title=data["title"],

                category=normalize_category(
                    data["category"]
                ),

                description=data["description"],

                severity=normalize_severity(
                    data["severity"]
                ),

                latitude=float(
                    data["latitude"]
                ),

                longitude=float(
                    data["longitude"]
                ),

                user_id=session["user_id"],

                address=address,

                image=image_filename
            )


            flash(
                "Your report has been submitted successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "dashboard"
                )
            )


        except Exception as error:

            db.session.rollback()

            print(
                "REPORT ERROR:",
                error
            )

            flash(
                "Unable to submit report. "
                "Please try again.",
                "danger"
            )

            return render_template(
                "report.html"
            )


    # ---------------------------------------------
    # GET REQUEST
    # ---------------------------------------------

    return render_template(
        "report.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():
    """Display dashboard."""

    if "user_id" not in session:

        flash(
            "Please login to view dashboard.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


    # Current user's reports
    reports = Report.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Report.created_at.desc()
    ).all()


    # Overall statistics
    all_reports = Report.query.all()

    stats = get_report_statistics(
        all_reports
    )


    return render_template(
        "dashboard.html",
        reports=reports,
        stats=stats
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():
    """Register new user."""

    # Already logged in
    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            password
        )


        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        name_error = validate_name(
            name
        )

        if name_error:

            flash(
                name_error,
                "danger"
            )

            return render_template(
                "register.html"
            )


        username_error = validate_username(
            username
        )

        if username_error:

            flash(
                username_error,
                "danger"
            )

            return render_template(
                "register.html"
            )


        email_error = validate_email(
            email
        )

        if email_error:

            flash(
                email_error,
                "danger"
            )

            return render_template(
                "register.html"
            )


        password_valid, password_error = (
            validate_password(password)
        )

        if not password_valid:

            flash(
                password_error,
                "danger"
            )

            return render_template(
                "register.html"
            )


        if not passwords_match(
            password,
            confirm_password
        ):

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template(
                "register.html"
            )


        # -----------------------------------------
        # DUPLICATE CHECK
        # -----------------------------------------

        if get_user_by_email(email):

            flash(
                "An account with this email already exists.",
                "danger"
            )

            return render_template(
                "register.html"
            )


        if get_user_by_username(username):

            flash(
                "This username is already taken.",
                "danger"
            )

            return render_template(
                "register.html"
            )


        # -----------------------------------------
        # CREATE USER
        # -----------------------------------------

        try:

            user = create_user(
                name=name,
                username=username,
                email=email,
                password=password
            )


            # Automatically login
            session["user_id"] = user.id
            session["username"] = user.username


            flash(
                "Account created successfully!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )


        except Exception as error:

            db.session.rollback()

            print(
                "REGISTER ERROR:",
                error
            )

            flash(
                "Unable to create account.",
                "danger"
            )


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():
    """Login user."""

    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        # -----------------------------------------
        # VALIDATE
        # -----------------------------------------

        if not email or not password:

            flash(
                "Email and password are required.",
                "danger"
            )

            return render_template(
                "login.html"
            )


        # -----------------------------------------
        # FIND USER
        # -----------------------------------------

        user = get_user_by_email(
            email
        )


        if user is None:

            flash(
                "Invalid email or password.",
                "danger"
            )

            return render_template(
                "login.html"
            )


        # -----------------------------------------
        # CHECK PASSWORD
        # -----------------------------------------

        if not user.check_password(
            password
        ):

            flash(
                "Invalid email or password.",
                "danger"
            )

            return render_template(
                "login.html"
            )


        # -----------------------------------------
        # CREATE SESSION
        # -----------------------------------------

        session["user_id"] = user.id

        session["username"] = (
            user.username
        )

        session["user_name"] = (
            user.name
        )


        flash(
            "Welcome back, "
            + user.name
            + "!",
            "success"
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():
    """Logout current user."""

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("index")
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():
    """Display user profile."""

    if "user_id" not in session:

        flash(
            "Please login to view your profile.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


    user = User.query.get(
        session["user_id"]
    )


    if user is None:

        session.clear()

        flash(
            "User account not found.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    reports = Report.query.filter_by(
        user_id=user.id
    ).order_by(
        Report.created_at.desc()
    ).all()


    return render_template(
        "profile.html",
        user=user,
        reports=reports
    )


# =========================================================
# SINGLE REPORT
# =========================================================

@app.route("/report/<int:report_id>")
def report_detail(report_id):
    """Display one report."""

    report_item = get_report_by_id(
        report_id
    )


    if report_item is None:

        return render_template(
            "404.html"
        ), 404


    return render_template(
        "report_detail.html",
        report=report_item
    )


# =========================================================
# UPDATE REPORT STATUS
# =========================================================

@app.route(
    "/report/<int:report_id>/status",
    methods=["POST"]
)
def update_report_status(report_id):
    """Update report status."""

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


    report_item = get_report_by_id(
        report_id
    )


    if report_item is None:

        flash(
            "Report not found.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )


    new_status = request.form.get(
        "status",
        ""
    ).strip()


    valid_statuses = {
        "Open",
        "Under Review",
        "In Progress",
        "Resolved",
        "Rejected"
    }


    if new_status not in valid_statuses:

        flash(
            "Invalid report status.",
            "danger"
        )

        return redirect(
            url_for(
                "dashboard"
            )
        )


    report_item.status = new_status

    db.session.commit()


    flash(
        "Report status updated.",
        "success"
    )


    return redirect(
        url_for("dashboard")
    )


# =========================================================
# UPLOADED FILES
# =========================================================

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found():

    return render_template(
        "404.html"
    ), 404


# =========================================================
# 500 ERROR
# =========================================================

@app.errorhandler(500)
def internal_server_error(error):

    db.session.rollback()

    return (
        render_template(
            "500.html"
        ),
        500
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=app.config.get(
            "DEBUG",
            True
        )
    )
app = Flask(__name__)