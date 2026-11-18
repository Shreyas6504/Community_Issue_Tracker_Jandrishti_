"""
JanDrishti (जन दृष्टि) - Community Issue & Civic Grievance Tracker
Author: Shreyas (https://github.com/Shreyas6504)
Description: A full-stack civic-tech platform enabling citizens to report, geotag, 
and track municipal issues while empowering local administrations with analytics 
and lifecycle management.
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "jandrishti.db")

def get_db():
    """Contextual database connection helper."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    """Initializes schema and seeds realistic baseline civic issues."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Schema definition
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                location_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Reported',
                officer_note TEXT DEFAULT '',
                upvotes INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Check if initial seed data is needed
        cursor.execute("SELECT COUNT(*) AS count FROM issues")
        if cursor.fetchone()["count"] == 0:
            seed_data = [
                (
                    "Hazardous Pothole near Main Market Junction",
                    "Deep crater causing traffic slowdowns and severe accident hazard for two-wheelers, especially in night hours.",
                    "Roads & Infrastructure",
                    "High",
                    "MG Road, Cross 4, Central Sector",
                    12.9716, 77.5946,
                    "In Progress",
                    "PWD contractor notified. Asphalt resurfacing scheduled for Thursday morning.",
                    24
                ),
                (
                    "Broken Water Pipeline Flooding Street",
                    "Continuous freshwater leakage for 36 hours. Road submergence and dropping pressure in neighboring homes.",
                    "Water & Sanitation",
                    "Critical",
                    "Sector 7, Near Community Center",
                    12.9815, 77.6000,
                    "Reported",
                    "Inspection team dispatched to locate pipeline valve.",
                    42
                ),
                (
                    "Streetlights Non-Functional on School Road",
                    "Row of 6 streetlights broken. Area completely dark after 7 PM, creating safety concern for evening commuters.",
                    "Electricity & Lighting",
                    "Medium",
                    "Vivekananda Marg, Block B",
                    12.9650, 77.5850,
                    "Resolved",
                    "Replaced burned-out LED fixtures and fixed junction box wiring.",
                    15
                ),
                (
                    "Overflowing Waste Dump & Blocked Drainage",
                    "Garbage bin uncollected for 5 days. Waste spilling into open storm drain causing stench and vector breeding.",
                    "Sanitation & Waste",
                    "High",
                    "Ward 12, Market Backgate",
                    12.9750, 77.6100,
                    "In Progress",
                    "Solid Waste Management assigned extra loader vehicle for clearance.",
                    31
                )
            ]
            cursor.executemany("""
                INSERT INTO issues (title, description, category, severity, location_name, latitude, longitude, status, officer_note, upvotes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, seed_data)
            db.commit()

# --- Web UI Routes ---

@app.route("/")
def index():
    return render_template("index.html")

# --- REST API Endpoints ---

@app.route("/api/issues", methods=["GET"])
def get_issues():
    """Retrieve filtered issues with optional category, status, and severity queries."""
    category = request.args.get("category")
    status = request.args.get("status")
    severity = request.args.get("severity")

    query = "SELECT * FROM issues WHERE 1=1"
    params = []

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    if status and status != "All":
        query += " AND status = ?"
        params.append(status)
    if severity and severity != "All":
        query += " AND severity = ?"
        params.append(severity)

    query += " ORDER BY upvotes DESC, created_at DESC"

    cursor = get_db().cursor()
    cursor.execute(query, params)
    issues = [dict(row) for row in cursor.fetchall()]
    return jsonify({"success": True, "data": issues})

@app.route("/api/issues", methods=["POST"])
def create_issue():
    """Report a new community issue."""
    data = request.get_json() or {}
    required = ["title", "description", "category", "severity", "location_name", "latitude", "longitude"]
    for field in required:
        if not data.get(field):
            return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO issues (title, description, category, severity, location_name, latitude, longitude, status, upvotes)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Reported', 1)
    """, (
        data["title"].strip(),
        data["description"].strip(),
        data["category"],
        data["severity"],
        data["location_name"].strip(),
        float(data["latitude"]),
        float(data["longitude"])
    ))
    db.commit()
    new_id = cursor.lastrowid
    return jsonify({"success": True, "message": "Issue registered successfully", "id": new_id}), 201

@app.route("/api/issues/<int:issue_id>/status", methods=["PATCH"])
def update_issue_status(issue_id):
    """Admin / Municipal Officer endpoint to update status and add progress notes."""
    data = request.get_json() or {}
    new_status = data.get("status")
    officer_note = data.get("officer_note", "").strip()

    valid_statuses = ["Reported", "Under Investigation", "In Progress", "Resolved"]
    if new_status not in valid_statuses:
        return jsonify({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE issues 
        SET status = ?, officer_note = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (new_status, officer_note, issue_id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"success": False, "error": "Issue not found"}), 404

    return jsonify({"success": True, "message": "Status updated successfully"})

@app.route("/api/issues/<int:issue_id>/upvote", methods=["POST"])
def upvote_issue(issue_id):
    """Citizen upvote endpoint to boost visibility for critical local grievances."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE issues SET upvotes = upvotes + 1 WHERE id = ?", (issue_id,))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"success": False, "error": "Issue not found"}), 404

    cursor.execute("SELECT upvotes FROM issues WHERE id = ?", (issue_id,))
    new_count = cursor.fetchone()["upvotes"]
    return jsonify({"success": True, "upvotes": new_count})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Analytics aggregate for dashboards."""
    cursor = get_db().cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) AS resolved,
            SUM(CASE WHEN severity = 'Critical' AND status != 'Resolved' THEN 1 ELSE 0 END) AS active_critical,
            SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress
        FROM issues
    """)
    stats = dict(cursor.fetchone())
    total = stats["total"] or 0
    resolved = stats["resolved"] or 0
    stats["resolution_rate"] = round((resolved / total * 100), 1) if total > 0 else 0
    return jsonify({"success": True, "stats": stats})

if __name__ == "__main__":
    init_db()
    print("✓ JanDrishti Engine Online: Running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
