# JanDrishti (जन दृष्टि) — Civic Issue & Grievance Tracker

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Framework-Flask%203.0-lightgrey?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Database-SQLite%20%2F%20PostgreSQL-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="Database" />
  <img src="https://img.shields.io/badge/Architecture-REST%20API-005571?style=for-the-badge&logo=postman&logoColor=white" alt="REST API" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

> **JanDrishti** (meaning *People's Vision*) is an open-source civic-technology platform designed to bridge the communication gap between citizens and local municipal authorities. It empowers community members to report, geotag, and upvote civic hazards (e.g., potholes, pipeline leaks, broken streetlights) while providing municipal engineers with real-time lifecycle tracking, analytics, and resolution auditing.

---

## 🌟 Key Highlights & Features

- 📍 **Interactive Geospatial Mapping:** Live OpenStreetMap / Leaflet interface displaying civic incidents with real-time GPS coordinate markers and severity color coding.
- 🚦 **Issue Lifecycle Management:** Tracks grievances through 4 stages: `Reported` ➔ `Under Investigation` ➔ `In Progress` ➔ `Resolved`.
- 🗳️ **Democratic Citizen Upvoting:** Crowdsourced prioritization ensures critical community emergencies rise to the top of administrative queues.
- 🛡️ **Municipal Officer Workspace:** Dedicated administrative toggle allowing field engineers to update ticket status and append verified official action notes.
- 📊 **Real-time Analytics Engine:** Aggregate metrics on total grievance volume, active critical hazards, and resolution percentage rates.
- ⚡ **Zero-Dependency Lightweight Core:** Built with clean Python standards, SQLite database persistence, and native RESTful JSON endpoints.

---

## 🏗️ Architecture & Workflow

```text
  [ Citizen / User ]
         │
         ▼
  [ Web Frontend (Leaflet Map + Responsive UI) ]
         │
         ├── POST /api/issues  (Submit Grievance + Geotag)
         ├── GET  /api/issues  (Filter by Category, Status, Severity)
         ├── POST /api/issues/:id/upvote (Community Upvoting)
         │
         ▼
  [ Flask Application Server & REST Controllers ]
         │
         ▼
  [ SQLite / Relational Persistence Layer ]
         │
         ▼
  [ Municipal Officer Dashboard ] ── PATCH /api/issues/:id/status ──> [ Resolved ]
```

---

## 🔌 REST API Documentation

### 1. Fetch Issues
`GET /api/issues`
- **Query Parameters:** `category`, `status`, `severity` (Optional)
- **Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Hazardous Pothole near Main Market Junction",
      "category": "Roads & Infrastructure",
      "severity": "High",
      "status": "In Progress",
      "location_name": "MG Road, Cross 4",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "officer_note": "Asphalt resurfacing scheduled for Thursday morning.",
      "upvotes": 24,
      "created_at": "2026-03-28 10:00:00"
    }
  ]
}
```

### 2. Report New Issue
`POST /api/issues`
- **Payload:**
```json
{
  "title": "Broken Streetlight on 5th Main",
  "description": "Entire street is dark; safety concern for commuters.",
  "category": "Electricity & Lighting",
  "severity": "Medium",
  "location_name": "5th Main Road, Indiranagar",
  "latitude": 12.9750,
  "longitude": 77.6100
}
```

### 3. Update Status (Officer Mode)
`PATCH /api/issues/<id>/status`
- **Payload:**
```json
{
  "status": "Resolved",
  "officer_note": "Replaced bulb fixture and restored power circuit."
}
```

### 4. Community Upvote
`POST /api/issues/<id>/upvote`

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.9+
- Git

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shreyas6504/Community_Issue_Tracker_Jandrishti_.git
   cd Community_Issue_Tracker_Jandrishti_
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access in browser:**
   Open [http://localhost:5000](http://localhost:5000)

---

## 📈 Roadmap & Future Enhancements

- [ ] **AI-Powered Image Triage:** Integration with Vision models to automatically assess pothole or waste severity from uploaded photos.
- [ ] **WhatsApp / SMS Bot:** Enable citizen reporting directly via Twilio WhatsApp API.
- [ ] **GeoJSON Ward Heatmaps:** Density visualizations of unresolved civic problems across municipal wards.

---

## 👤 Author

**Shreyas**
- GitHub: [@Shreyas6504](https://github.com/Shreyas6504)
- LinkedIn: [Contact via Email](mailto:jshreyasshetty@gmail.com)

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
