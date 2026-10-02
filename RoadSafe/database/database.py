# =========================================================
# ROADSAFE - database/database.py
# =========================================================

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# =========================================================
# DATABASE INSTANCE
# =========================================================

db = SQLAlchemy()


# =========================================================
# USER MODEL
# =========================================================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    username = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # One user can create many reports
    reports = db.relationship(
        "Report",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # -----------------------------------------------------
    # PASSWORD
    # -----------------------------------------------------

    def set_password(self, password):
        """Hash and save password."""

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):
        """Check password against stored hash."""

        return check_password_hash(
            self.password_hash,
            password
        )

    # -----------------------------------------------------
    # DICTIONARY
    # -----------------------------------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }


# =========================================================
# REPORT MODEL
# =========================================================

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    title = db.Column(
        db.String(150),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    severity = db.Column(
        db.String(20),
        default="medium",
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Open",
        nullable=False
    )

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    address = db.Column(
        db.String(300),
        nullable=True
    )

    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    image = db.Column(
        db.String(255),
        nullable=True
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -----------------------------------------------------
    # USER RELATION
    # -----------------------------------------------------

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # -----------------------------------------------------
    # DICTIONARY
    # -----------------------------------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "image": self.image,
            "user_id": self.user_id,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            )
        }


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db(app):
    """
    Connect SQLAlchemy with Flask application
    and create database tables.
    """

    db.init_app(app)

    with app.app_context():
        db.create_all()


# =========================================================
# CREATE DEFAULT DATABASE
# =========================================================

def create_tables(app):
    """Create all database tables."""

    with app.app_context():
        db.create_all()


# =========================================================
# DELETE ALL TABLES
# =========================================================

def drop_tables(app):
    """
    WARNING:
    This deletes all database tables and data.
    """

    with app.app_context():
        db.drop_all()


# =========================================================
# GET USER BY EMAIL
# =========================================================

def get_user_by_email(email):
    """Find user using email."""

    if not email:
        return None

    return User.query.filter_by(
        email=email.strip().lower()
    ).first()


# =========================================================
# GET USER BY USERNAME
# =========================================================

def get_user_by_username(username):
    """Find user using username."""

    if not username:
        return None

    return User.query.filter_by(
        username=username.strip()
    ).first()


# =========================================================
# GET REPORT BY ID
# =========================================================

def get_report_by_id(report_id):
    """Find report by ID."""

    try:
        report_id = int(report_id)
    except (TypeError, ValueError):
        return None

    return Report.query.get(report_id)


# =========================================================
# CREATE USER
# =========================================================

def create_user(
    name,
    username,
    email,
    password
):
    """Create a new user."""

    user = User(
        name=name.strip(),
        username=username.strip(),
        email=email.strip().lower()
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


# =========================================================
# CREATE REPORT
# =========================================================

def create_report(
    title,
    category,
    description,
    severity,
    latitude,
    longitude,
    user_id,
    address=None,
    image=None
):
    """Create a new RoadSafe report."""

    report = Report(
        title=title.strip(),
        category=category,
        description=description.strip(),
        severity=severity,
        latitude=float(latitude),
        longitude=float(longitude),
        address=address,
        image=image,
        user_id=user_id
    )

    db.session.add(report)
    db.session.commit()

    return report


# =========================================================
# UPDATE REPORT STATUS
# =========================================================

def update_report_status(
    report_id,
    status
):
    """Update report status."""

    report = get_report_by_id(
        report_id
    )

    if not report:
        return None

    report.status = status

    db.session.commit()

    return report


# =========================================================
# DELETE REPORT
# =========================================================

def delete_report(report_id):
    """Delete a report."""

    report = get_report_by_id(
        report_id
    )

    if not report:
        return False

    db.session.delete(report)
    db.session.commit()

    return True