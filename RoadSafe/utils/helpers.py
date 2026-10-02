# =========================================================
# ROADSAFE - utils/helpers.py
# =========================================================

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename


# ---------------------------------------------------------
# FILE SETTINGS
# ---------------------------------------------------------

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


# ---------------------------------------------------------
# FILE HELPERS
# ---------------------------------------------------------

def allowed_file(filename, allowed_extensions=None):
    """Check whether a file extension is allowed."""

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    if allowed_extensions is None:
        allowed_extensions = ALLOWED_IMAGE_EXTENSIONS

    return extension in allowed_extensions


def get_file_extension(filename):
    """Get file extension without dot."""

    if not filename or "." not in filename:
        return ""

    return filename.rsplit(".", 1)[1].lower()


def generate_unique_filename(filename):
    """Generate a secure unique filename."""

    filename = secure_filename(filename)

    extension = get_file_extension(filename)
    unique_id = uuid.uuid4().hex[:12]

    if extension:
        return f"{unique_id}.{extension}"

    return unique_id


def ensure_upload_folder(folder):
    """Create upload folder if it does not exist."""

    os.makedirs(folder, exist_ok=True)

    return folder


def save_uploaded_file(file, upload_folder):
    """Save uploaded image and return filename."""

    if file is None:
        return None

    if not file.filename:
        return None

    if not allowed_file(file.filename):
        return None

    ensure_upload_folder(upload_folder)

    filename = generate_unique_filename(
        file.filename
    )

    filepath = os.path.join(
        upload_folder,
        filename
    )

    file.save(filepath)

    return filename


# ---------------------------------------------------------
# TEXT HELPERS
# ---------------------------------------------------------

def clean_text(value):
    """Remove extra spaces from text."""

    if value is None:
        return ""

    return " ".join(
        str(value).strip().split()
    )


def clean_multiline_text(value):
    """Clean multiline text."""

    if value is None:
        return ""

    lines = []

    for line in str(value).splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def truncate_text(text, max_length=100):
    """Shorten text for cards."""

    text = clean_text(text)

    if len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."


# ---------------------------------------------------------
# DATE / TIME HELPERS
# ---------------------------------------------------------

def now():
    """Return current datetime."""

    return datetime.now()


def format_datetime(
    value,
    format_string="%d %b %Y, %I:%M %p"
):
    """Format datetime for UI."""

    if not value:
        return ""

    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value

    return value.strftime(format_string)


def time_ago(value):
    """Return relative time such as 5m ago."""

    if not value:
        return ""

    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return ""

    difference = datetime.now() - value
    seconds = int(difference.total_seconds())

    if seconds < 60:
        return "Just now"

    minutes = seconds // 60

    if minutes < 60:
        return f"{minutes}m ago"

    hours = minutes // 60

    if hours < 24:
        return f"{hours}h ago"

    days = hours // 24

    if days < 30:
        return f"{days}d ago"

    months = days // 30

    if months < 12:
        return f"{months}mo ago"

    years = months // 12

    return f"{years}y ago"


# ---------------------------------------------------------
# ROADSAFE HELPERS
# ---------------------------------------------------------

def normalize_category(category):
    """Normalize report category."""

    if not category:
        return "Other"

    category = clean_text(category)

    categories = {
        "pothole": "Pothole",
        "road damage": "Road Damage",
        "street light": "Street Light",
        "traffic signal": "Traffic Signal",
        "water logging": "Water Logging",
        "garbage": "Garbage",
        "broken divider": "Broken Divider",
        "illegal parking": "Illegal Parking",
        "accident": "Accident",
        "other": "Other"
    }

    return categories.get(
        category.lower(),
        "Other"
    )


def normalize_severity(severity):
    """Normalize severity."""

    if not severity:
        return "medium"

    severity = str(
        severity
    ).strip().lower()

    if severity not in {
        "low",
        "medium",
        "high",
        "critical"
    }:
        return "medium"

    return severity


def normalize_status(status):
    """Normalize report status."""

    if not status:
        return "Open"

    statuses = {
        "open": "Open",
        "under review": "Under Review",
        "in progress": "In Progress",
        "resolved": "Resolved",
        "rejected": "Rejected"
    }

    return statuses.get(
        str(status).strip().lower(),
        "Open"
    )


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

def calculate_percentage(value, total):
    """Calculate percentage safely."""

    try:
        value = float(value)
        total = float(total)
    except (TypeError, ValueError):
        return 0

    if total == 0:
        return 0

    return round(
        (value / total) * 100,
        2
    )


def get_report_statistics(reports):
    """Create dashboard statistics."""

    stats = {
        "total": 0,
        "open": 0,
        "under_review": 0,
        "in_progress": 0,
        "resolved": 0,
        "rejected": 0,
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    for report in reports:

        if isinstance(report, dict):
            status = report.get("status")
            severity = report.get("severity")
        else:
            status = getattr(
                report,
                "status",
                None
            )

            severity = getattr(
                report,
                "severity",
                None
            )

        status = normalize_status(status)
        severity = normalize_severity(severity)

        stats["total"] += 1

        status_key = {
            "Open": "open",
            "Under Review": "under_review",
            "In Progress": "in_progress",
            "Resolved": "resolved",
            "Rejected": "rejected"
        }.get(status)

        if status_key:
            stats[status_key] += 1

        if severity in {
            "low",
            "medium",
            "high",
            "critical"
        }:
            stats[severity] += 1

    stats["resolution_rate"] = calculate_percentage(
        stats["resolved"],
        stats["total"]
    )

    return stats


# ---------------------------------------------------------
# PAGINATION
# ---------------------------------------------------------

def paginate(items, page=1, per_page=10):
    """Simple pagination."""

    try:
        page = max(1, int(page))
    except (TypeError, ValueError):
        page = 1

    try:
        per_page = max(1, int(per_page))
    except (TypeError, ValueError):
        per_page = 10

    total = len(items)

    pages = (
        (total + per_page - 1)
        // per_page
    )

    start = (page - 1) * per_page
    end = start + per_page

    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": pages,
        "has_previous": page > 1,
        "has_next": page < pages
    }


# ---------------------------------------------------------
# SAFE CONVERSION
# ---------------------------------------------------------

def safe_int(value, default=0):
    """Safely convert to integer."""

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    """Safely convert to float."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------
# RESPONSE HELPERS
# ---------------------------------------------------------

def success_response(message="Success", data=None):
    """Create success response."""

    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(
    message="Something went wrong.",
    errors=None
):
    """Create error response."""

    return {
        "success": False,
        "message": message,
        "errors": errors
    }