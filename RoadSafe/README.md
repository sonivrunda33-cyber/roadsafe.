# 🚦 RoadSafe

RoadSafe is a modern road-safety and civic issue reporting platform.

It allows people to report problems such as:

- 🕳️ Potholes
- 🚧 Road damage
- 💡 Broken street lights
- 🚦 Traffic signal problems
- 💧 Water logging
- 🗑️ Garbage
- 🧱 Broken dividers
- 🚗 Illegal parking
- ⚠️ Accidents
- 📍 Other road-related problems

The platform provides a visual dashboard and map-based reporting system.

---

## ✨ Features

### 🏠 Home

Modern landing page with:

- Premium animations
- Floating elements
- Smooth scrolling
- Road-safety statistics
- Call-to-action buttons
- Responsive design

---

### 📍 Report Issue

Users can report a road problem with:

- Issue title
- Category
- Description
- Severity
- Location
- Latitude
- Longitude
- Image

---

### 🗺️ Interactive Map

The map can display reported road problems.

Each report can contain:

- Location
- Issue type
- Severity
- Status
- Description

---

### 📊 Dashboard

Dashboard provides:

- Total reports
- Open reports
- Reports under review
- Reports in progress
- Resolved reports
- Critical issues
- Resolution rate

---

### 👤 Profile

Users can view:

- Name
- Email
- Profile information
- Submitted reports
- Report history

---

### 🔐 Authentication

RoadSafe supports:

- User registration
- Login
- Logout
- Password validation
- Session management

---

# 🛠️ Technology Stack

## Backend

- Python
- Flask
- Flask-SQLAlchemy

## Frontend

- HTML
- CSS
- JavaScript

## Database

- SQLite

## Environment

- python-dotenv

## Map

The map can be integrated with a map provider such as:

- OpenStreetMap
- Leaflet

---

# 📁 Project Structure

```text
RoadSafe/
│
├── app.py
├── config.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── validators.py
│
├── static/
│   │
│   ├── css/
│   │   ├── home.css
│   │   ├── map.css
│   │   ├── report.css
│   │   └── dashboard.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── map.js
│   │   ├── report.js
│   │   ├── dashboard.js
│   │   └── animations.js
│   │
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── map.html
│   ├── report.html
│   ├── profile.html
│   └── 404.html
│
└── uploads/