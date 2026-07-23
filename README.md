# Feedback Management System

A clean, modern, full-stack **Feedback Management System** with a glassmorphism UI, blue-gradient theme, and a lightweight Flask + JSON backend.

---

## 📋 Project Description

This project allows users to submit feedback (name, email, star rating, and comments) through a responsive, professional web form. Submissions are validated on both the client and server, then stored persistently in a local `feedback.json` file — no database setup required.

**Key Features**
- Clean, modern white background with blue gradient accents
- Glassmorphism feedback card with smooth animations
- Five-star clickable rating system
- Real-time client-side validation with inline error messages
- Flask REST API (`POST /submit-feedback`) with server-side validation
- CORS enabled for local cross-origin development
- Fully responsive — works on desktop, tablet, and mobile
- Success confirmation screen with auto form reset

---

## 📁 Folder Structure

```
Feedback-System/
│
├── frontend/
│   ├── index.html          # Main feedback form page
│   ├── style.css           # Styling (Poppins font, gradients, glassmorphism)
│   ├── script.js           # Validation, star rating, Fetch API calls
│   └── assets/
│       └── logo.png        # Brand logo (optional)
│
├── backend/
│   ├── app.py               # Flask application & API routes
│   ├── feedback.json        # JSON "database" of submitted feedback
│   ├── requirements.txt     # Python dependencies
│   └── templates/
│       └── README.md        # Project documentation (this file)
```

---

## ⚙️ Tech Stack

| Layer      | Technology                  |
|------------|------------------------------|
| Frontend   | HTML5, CSS3, Vanilla JavaScript |
| Backend    | Python (Flask)               |
| Database   | JSON file (`feedback.json`)  |
| Font       | Google Fonts — Poppins       |

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

### 2. Install Backend Dependencies

Navigate to the `backend/` folder and install the required packages:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the Backend Server

```bash
python app.py
```

The Flask API will start at:

```
http://127.0.0.1:5000
```

You should see the server running in debug mode. Test it's alive by visiting `http://127.0.0.1:5000/` in your browser — it should return a small JSON status message.

### 4. Launch the Frontend

Open `frontend/index.html` directly in your browser (double-click it, or use a tool like VS Code's "Live Server" extension for the best experience):

```
frontend/index.html
```

> **Note:** Because the frontend calls the API at `http://127.0.0.1:5000/submit-feedback`, make sure the Flask backend (Step 3) is running **before** you submit the form.

---

## 🔌 API Reference

### `POST /submit-feedback`

Submits a new feedback entry.

**Request Body**
```json
{
  "name": "Priyanka",
  "email": "abc@gmail.com",
  "rating": 5,
  "feedback": "Excellent workshop!"
}
```

**Success Response** — `201 Created`
```json
{
  "status": "success",
  "message": "Feedback submitted successfully.",
  "data": {
    "name": "Priyanka",
    "email": "abc@gmail.com",
    "rating": 5,
    "feedback": "Excellent workshop!",
    "date": "2026-07-23 10:30"
  }
}
```

**Error Response** — `400 Bad Request`
```json
{
  "status": "error",
  "message": "Name must be at least 3 characters. A valid email address is required."
}
```

### `GET /feedback`
Returns all stored feedback entries as a JSON array (useful for admin/debugging purposes).

---

## ✅ Validation Rules

| Field     | Rule                                    |
|-----------|------------------------------------------|
| Name      | Required, minimum 3 characters           |
| Email     | Required, must be a valid email format   |
| Rating    | Required, must be between 1 and 5 stars  |
| Feedback  | Required, minimum 20 characters          |

---

## 🎨 Design Notes

- **Theme:** White background with a blue gradient (`#3b82f6` → `#1e40af`)
- **Card style:** Glassmorphism (frosted glass blur effect)
- **Typography:** Poppins (Google Fonts)
- **Animations:** Smooth fade-ins, hover scale effects, star hover/click transitions, toast notifications

---

## 📄 License

This project is provided as-is for educational and demonstration purposes.
