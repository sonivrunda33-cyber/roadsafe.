# =========================================================
# ROADSAFE - utils/validators.py
# =========================================================

import re


# ---------------------------------------------------------
# REGEX
# ---------------------------------------------------------

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+"
    r"\.[A-Za-z]{2,}$"
)

PHONE_REGEX = re.compile(
    r"^[6-9][0-9]{9}$"
)

USERNAME_REGEX = re.compile(
    r"^[A-Za-z0-9_]{3,30}$"
)


# ---------------------------------------------------------
# REQUIRED
# ---------------------------------------------------------

def is_required(value):
    """Check if value exists."""

    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    return True


def validate_required(
    value,
    field_name="Field"
):
    """Validate required field."""

    if not is_required(value):
        return f"{field_name} is required."

    return None


# ---------------------------------------------------------
# EMAIL
# ---------------------------------------------------------

def is_valid_email(email):
    """Check email format."""

    if not email:
        return False

    email = str(email).strip()

    return bool(
        EMAIL_REGEX.match(email)
    )


def validate_email(email):
    """Validate email."""

    if not email:
        return "Email is required."

    if not is_valid_email(email):
        return "Please enter a valid email address."

    return None


# ---------------------------------------------------------
# PASSWORD
# ---------------------------------------------------------

def validate_password(
    password,
    min_length=8
):
    """
    Validate password.

    Returns:
        (True, None)
        or
        (False, error_message)
    """

    if not password:
        return (
            False,
            "Password is required."
        )

    if len(password) < min_length:
        return (
            False,
            f"Password must contain at least "
            f"{min_length} characters."
        )

    if not any(
        char.isupper()
        for char in password
    ):
        return (
            False,
            "Password must contain at least "
            "one uppercase letter."
        )

    if not any(
        char.islower()
        for char in password
    ):
        return (
            False,
            "Password must contain at least "
            "one lowercase letter."
        )

    if not any(
        char.isdigit()
        for char in password
    ):
        return (
            False,
            "Password must contain at least "
            "one number."
        )

    return (
        True,
        None
    )


def passwords_match(
    password,
    confirm_password
):
    """Check whether passwords match."""

    if not password:
        return False

    return password == confirm_password


# ---------------------------------------------------------
# USERNAME
# ---------------------------------------------------------

def is_valid_username(username):
    """Check username format."""

    if not username:
        return False

    return bool(
        USERNAME_REGEX.match(
            username.strip()
        )
    )


def validate_username(username):
    """Validate username."""

    if not username:
        return "Username is required."

    username = username.strip()

    if len(username) < 3:
        return (
            "Username must contain "
            "at least 3 characters."
        )

    if len(username) > 30:
        return (
            "Username cannot exceed "
            "30 characters."
        )

    if not is_valid_username(username):
        return (
            "Username can contain only "
            "letters, numbers and underscore."
        )

    return None


# ---------------------------------------------------------
# PHONE
# ---------------------------------------------------------

def is_valid_phone(phone):
    """Validate Indian mobile number."""

    if not phone:
        return False

    phone = re.sub(
        r"\D",
        "",
        str(phone)
    )

    return bool(
        PHONE_REGEX.match(phone)
    )


def validate_phone(phone):
    """Validate phone number."""

    if not phone:
        return "Phone number is required."

    if not is_valid_phone(phone):
        return (
            "Please enter a valid "
            "10-digit mobile number."
        )

    return None


# ---------------------------------------------------------
# NAME
# ---------------------------------------------------------

def validate_name(
    name,
    field_name="Name"
):
    """Validate person's name."""

    if not name:
        return f"{field_name} is required."

    name = str(name).strip()

    if len(name) < 2:
        return (
            f"{field_name} must contain "
            f"at least 2 characters."
        )

    if len(name) > 100:
        return (
            f"{field_name} cannot exceed "
            f"100 characters."
        )

    if not re.match(
        r"^[A-Za-zÀ-ÿ\s.'-]+$",
        name
    ):
        return (
            f"{field_name} contains "
            f"invalid characters."
        )

    return None


# ---------------------------------------------------------
# LOCATION
# ---------------------------------------------------------

def is_valid_latitude(latitude):
    """Validate latitude."""

    try:
        latitude = float(latitude)
    except (TypeError, ValueError):
        return False

    return -90 <= latitude <= 90


def is_valid_longitude(longitude):
    """Validate longitude."""

    try:
        longitude = float(longitude)
    except (TypeError, ValueError):
        return False

    return -180 <= longitude <= 180


def validate_coordinates(
    latitude,
    longitude
):
    """Validate latitude and longitude."""

    if latitude is None or latitude == "":
        return (
            False,
            "Latitude is required."
        )

    if longitude is None or longitude == "":
        return (
            False,
            "Longitude is required."
        )

    if not is_valid_latitude(latitude):
        return (
            False,
            "Invalid latitude."
        )

    if not is_valid_longitude(longitude):
        return (
            False,
            "Invalid longitude."
        )

    return (
        True,
        None
    )


# ---------------------------------------------------------
# REPORT CATEGORIES
# ---------------------------------------------------------

VALID_CATEGORIES = {
    "Pothole",
    "Road Damage",
    "Street Light",
    "Traffic Signal",
    "Water Logging",
    "Garbage",
    "Broken Divider",
    "Illegal Parking",
    "Accident",
    "Other"
}


VALID_SEVERITIES = {
    "low",
    "medium",
    "high",
    "critical"
}


def validate_category(category):
    """Validate RoadSafe report category."""

    if not category:
        return "Category is required."

    category_clean = str(
        category
    ).strip()

    valid = any(
        category_clean.lower() == item.lower()
        for item in VALID_CATEGORIES
    )

    if not valid:
        return (
            "Please select a valid "
            "report category."
        )

    return None


def validate_severity(severity):
    """Validate report severity."""

    if not severity:
        return "Severity is required."

    severity_clean = str(
        severity
    ).strip().lower()

    if severity_clean not in VALID_SEVERITIES:
        return (
            "Please select a valid "
            "severity."
        )

    return None


# ---------------------------------------------------------
# DESCRIPTION
# ---------------------------------------------------------

def validate_description(
    description,
    min_length=10,
    max_length=1000
):
    """Validate report description."""

    if not description:
        return "Description is required."

    description = str(
        description
    ).strip()

    if len(description) < min_length:
        return (
            f"Description must contain "
            f"at least {min_length} characters."
        )

    if len(description) > max_length:
        return (
            f"Description cannot exceed "
            f"{max_length} characters."
        )

    return None


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

def validate_title(
    title,
    min_length=3,
    max_length=150
):
    """Validate report title."""

    if not title:
        return "Title is required."

    title = str(title).strip()

    if len(title) < min_length:
        return (
            f"Title must contain at least "
            f"{min_length} characters."
        )

    if len(title) > max_length:
        return (
            f"Title cannot exceed "
            f"{max_length} characters."
        )

    return None


# ---------------------------------------------------------
# COMPLETE REPORT VALIDATION
# ---------------------------------------------------------

def validate_report(data):
    """
    Validate complete RoadSafe report.

    Expected data:

    {
        "title": "...",
        "category": "...",
        "severity": "...",
        "description": "...",
        "latitude": "...",
        "longitude": "..."
    }

    Returns:

    {
        "valid": True/False,
        "errors": {}
    }
    """

    if data is None:
        data = {}

    errors = {}

    # Title
    title_error = validate_title(
        data.get("title")
    )

    if title_error:
        errors["title"] = title_error

    # Category
    category_error = validate_category(
        data.get("category")
    )

    if category_error:
        errors["category"] = category_error

    # Severity
    severity_error = validate_severity(
        data.get("severity")
    )

    if severity_error:
        errors["severity"] = severity_error

    # Description
    description_error = validate_description(
        data.get("description")
    )

    if description_error:
        errors["description"] = description_error

    # Coordinates
    coordinates_valid, coordinates_error = (
        validate_coordinates(
            data.get("latitude"),
            data.get("longitude")
        )
    )

    if not coordinates_valid:
        errors["location"] = coordinates_error

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }