# =========================================================
# ROADSAFE - config.py
# =========================================================

import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:
    # -----------------------------------------------------
    # APP
    # -----------------------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ).lower() == "true"


    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///roadSafe.db"
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # -----------------------------------------------------
    # UPLOADS
    # -----------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "webp"
    }


    # -----------------------------------------------------
    # ROADSAVE
    # -----------------------------------------------------

    APP_NAME = os.getenv(
        "APP_NAME",
        "RoadSafe"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )


    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    MAP_DEFAULT_LAT = float(
        os.getenv(
            "MAP_DEFAULT_LAT",
            "22.3072"
        )
    )

    MAP_DEFAULT_LNG = float(
        os.getenv(
            "MAP_DEFAULT_LNG",
            "73.1812"
        )
    )

    MAP_DEFAULT_ZOOM = int(
        os.getenv(
            "MAP_DEFAULT_ZOOM",
            "13"
        )
    )


    # -----------------------------------------------------
    # OPTIONAL API KEYS
    # -----------------------------------------------------

    MAP_API_KEY = os.getenv(
        "MAP_API_KEY",
        ""
    )

    OPENWEATHER_API_KEY = os.getenv(
        "OPENWEATHER_API_KEY",
        ""
    )


# Default configuration
ConfigClass = Config