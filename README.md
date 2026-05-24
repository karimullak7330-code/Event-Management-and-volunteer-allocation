# Event Management & Volunteer Allocation System

**B.Tech 3rd Year Mini Project**  
*Department of Artificial Intelligence & Data Science*  
**Dhanalakshmi Srinivasan University, Trichy - 621112**

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Tech Stack](#tech-stack)
3. [System Architecture](#system-architecture)
4. [Features](#features)
5. [Installation & Setup](#installation--setup)
6. [Configuration](#configuration)
7. [Usage Guide](#usage-guide)
8. [Database Schema](#database-schema)
9. [API Endpoints](#api-endpoints)
10. [Security & Deployment](#security--deployment)
11. [Team & Credits](#team--credits)

---

## 🎯 System Overview

The **Event Management & Volunteer Allocation System** is a comprehensive web application designed to streamline event organization and volunteer coordination. It provides a robust platform for event organizers (admins) to manage events, create tasks, assign volunteers, and monitor submissions, while enabling volunteers to track their assignments, submit work, and communicate with organizers.

### Key Objectives
- ✅ Centralized event management and task allocation
- ✅ Real-time volunteer assignment tracking
- ✅ Automated file submission and approval workflow
- ✅ AI-powered intelligent assistant for user guidance
- ✅ Secure role-based access control
- ✅ Comprehensive reporting and analytics

---

## 🛠️ Tech Stack

### **Frontend**
- **HTML5** - Semantic markup structure
- **CSS3** - Modern styling with gradients and animations
- **Bootstrap 5.3** - Responsive UI framework
- **JavaScript (Vanilla)** - Interactive chatbot and dynamic UI

### **Backend**
- **Python 3.9+** - Core programming language
- **Flask 2.2.5** - Lightweight web framework
- **Flask-SQLAlchemy 3.0.3** - ORM for database management
- **Flask-Login 0.6.2** - User authentication & session management
- **Werkzeug 2.2.3** - Security utilities (password hashing)

### **Database**
- **SQLite 3** - Default lightweight database
- **SQL** - Relational data modeling

### **AI/ML Integration**
- **Google Gemini AI** - Advanced language model for chatbot
- **google-generativeai 0.3.0** - Python SDK for Gemini API

### **Security & Utilities**
- **python-dotenv** - Environment variable management
- **itsdangerous** - Secure data serialization

### **Deployment**
- **Windows/Linux/Mac** - Cross-platform support
- **Flask Development Server** - Built-in for development
- *Recommended for Production: Gunicorn + Nginx*

---

## 🏗️ System Architecture

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│         (Web Browser - Chrome, Firefox, Safari, Edge)           │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  (HTML Templates, CSS Styles, JavaScript, Bootstrap)           │
│  - base.html, index.html, login.html, register.html            │
│  - admin/dashboard.html, events.html, tasks.html, etc.         │
│  - volunteer/dashboard.html                                     │
│  - chatbot.html (AI Assistant UI)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│                    (Flask Routes & Logic)                       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Authentication Routes (Login, Register, Logout)         │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Admin Routes                                            │   │
│  │ - Event Management (/admin/events)                      │   │
│  │ - Task Management (/admin/tasks)                        │   │
│  │ - Submission Review (/admin/submissions)                │   │
│  │ - Attendance Tracking (/admin/attendance)               │   │
│  │ - Query Responses (/admin/query)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Volunteer Routes                                        │   │
│  │ - Dashboard (/volunteer)                                │   │
│  │ - Task Submission (/volunteer/task/submit)              │   │
│  │ - Attendance Marking (/volunteer/attendance)            │   │
│  │ - Query Submission (/volunteer/query)                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ AI Chatbot Routes                                       │   │
│  │ - Chat API (/api/chat) - JSON responses                │   │
│  │ - Chatbot Page (/chatbot) - Interactive interface       │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Utility Routes                                          │   │
│  │ - File Upload/Download (/uploads)                       │   │
│  │ - Index & Home (/index, /)                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Role-Based Access Control (RBAC) Decorator                   │
│  @role_required('admin') / @role_required('volunteer')        │
│  @login_required - Ensures authentication                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                            │
│                  (SQLAlchemy ORM)                              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ User Model   │  │ Event Model   │  │ Task Model   │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ id (PK)      │  │ id (PK)      │  │ id (PK)      │         │
│  │ name         │  │ title        │  │ event_id (FK)│         │
│  │ email        │  │ date         │  │ task_name    │         │
│  │ password     │  │ venue        │  │ status       │         │
│  │ role         │  │ description  │  │ est_start    │         │
│  │              │  │ start_time   │  │ est_end      │         │
│  │              │  │ end_time     │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Assignment   │  │ Submission   │  │ Attendance   │         │
│  │ Model        │  │ Model        │  │ Model        │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ id (PK)      │  │ id (PK)      │  │ id (PK)      │         │
│  │ task_id (FK) │  │ task_id (FK) │  │ event_id (FK)│         │
│  │ user_id (FK) │  │ user_id (FK) │  │ user_id (FK) │         │
│  │              │  │ filename     │  │ status       │         │
│  │              │  │ comment      │  │              │         │
│  │              │  │ submitted_at │  │              │         │
│  │              │  │ status       │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐                                              │
│  │ Query Model  │                                              │
│  ├──────────────┤                                              │
│  │ id (PK)      │                                              │
│  │ event_id (FK)│                                              │
│  │ user_id (FK) │                                              │
│  │ message      │                                              │
│  │ response     │                                              │
│  │ created_at   │                                              │
│  └──────────────┘                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERSISTENCE LAYER                            │
│                    (SQLite Database)                            │
│                                                                 │
│  ems.db (Single file, portable, no server required)           │
│  - SQL tables for all models                                   │
│  - Relationships & Constraints enforced                        │
│  - Indexes on frequently queried columns                       │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Google Gemini AI API                                     │  │
│  │ - Endpoint: https://generativelanguage.googleapis.com    │  │
│  │ - Model: gemini-pro                                      │  │
│  │ - Function: AI-powered chatbot responses                 │  │
│  │ - Auth: API Key (stored in .env, not in repo)           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### **Data Flow Diagram**

```
User Action (e.g., Login)
        │
        ▼
Browser sends HTTP Request
        │
        ▼
Flask Route Handler (@app.route)
        │
        ▼
Role Check Decorator (@role_required, @login_required)
        │
    ┌───┴───┐
    │       │
  YES      NO
    │       │
    ▼       ▼
Process   Redirect to
Request   Login/Error
    │
    ▼
Database Query/Update (SQLAlchemy ORM)
    │
    ▼
SQLite Database
    │
    ▼
Response (Template or JSON)
    │
    ▼
Browser Renders/Updates UI
```

### **User Interaction Flow**

```
ADMIN WORKFLOW:
┌─────────────────┐
│   Login Page    │
└────────┬────────┘
         │ (admin@example.com / password)
         ▼
┌──────────────────────────┐
│  Admin Dashboard         │
│  - View Events/Tasks     │
│  - View Submissions      │
└────────┬─────────────────┘
         │
    ┌────┴────┬─────────────┬──────────────┐
    ▼         ▼             ▼              ▼
┌────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
│Create  │ │Assign    │ │Approve  │ │View      │
│Events  │ │Tasks to  │ │Submit   │ │Queries & │
│        │ │Volunteers│ │tions    │ │Respond   │
└────────┘ └──────────┘ └─────────┘ └──────────┘
    │         │            │             │
    └─────────┴────────────┴─────────────┘
              │
              ▼
        ┌──────────────┐
        │ AI Assistant │
        │ (Ask for     │
        │  guidance)   │
        └──────────────┘

VOLUNTEER WORKFLOW:
┌─────────────────┐
│   Login Page    │
└────────┬────────┘
         │ (alice@example.com / password)
         ▼
┌──────────────────────────────┐
│  Volunteer Dashboard         │
│  - View Assigned Tasks       │
│  - View Events               │
└────────┬─────────────────────┘
         │
    ┌────┴────┬─────────────┬────────────┐
    ▼         ▼             ▼            ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│Mark    │ │Submit    │ │Mark      │ │Ask Query │
│Task    │ │Task Work │ │Attendance│ │to Admin  │
│Compl.  │ │(Files)   │ └──────────┘ └──────────┘
└────────┘ └──────────┘
    │         │
    └─────────┘
         │
         ▼
  ┌──────────────┐
  │ AI Assistant │
  │ (Ask for     │
  │  task help)  │
  └──────────────┘
```

---

## ✨ Features

### **Admin Features (Event Organizers)**
- ✅ **Event Management**
  - Create new events with title, date, venue, time, description
  - Edit event details
  - Delete events
  - View all events with filtering
  
- ✅ **Task Management**
  - Create tasks linked to events
  - Set estimated start/end times
  - Assign tasks to volunteers
  - Update task status (pending/completed)
  - Remove task assignments
  
- ✅ **Submission Review**
  - View all volunteer submissions
  - Download submitted files
  - Approve/Reject submissions
  - Track submission timeline
  
- ✅ **Attendance Tracking**
  - Mark volunteer attendance (present/absent)
  - View attendance statistics
  - Generate attendance reports
  
- ✅ **Query Management**
  - View volunteer questions
  - Respond to queries in real-time
  - Track query resolution
  
- ✅ **Dashboard Analytics**
  - Total tasks count
  - Completed vs pending tasks
  - Attendance summary
  - Quick event overview

### **Volunteer Features**
- ✅ **Task Dashboard**
  - View all assigned tasks
  - See task details and estimated time
  - Filter tasks by event
  - Track task status
  
- ✅ **Task Submission**
  - Upload work files (documents, images, etc.)
  - Add comments/notes
  - Track submission status (pending/approved/rejected)
  - Download submission history
  
- ✅ **Attendance Management**
  - Mark attendance for events
  - View personal attendance record
  
- ✅ **Communication**
  - Submit questions/queries to admins
  - Receive responses from organizers
  - Track query resolution status

### **AI Chatbot (Gemini-Powered)**
- ✅ **Intelligent Assistance**
  - Context-aware responses based on user role
  - Event and task guidance
  - Submission help
  - General FAQs
  
- ✅ **Real-time Chat Interface**
  - Typing indicators
  - Auto-scrolling conversation
  - Error handling and retry logic
  
- ✅ **Role-Specific Assistance**
  - Admin-specific event management guidance
  - Volunteer-specific task assistance

### **Security & Access Control**
- ✅ **Authentication**
  - Secure login/logout
  - Password hashing (Werkzeug)
  - Session management (Flask-Login)
  
- ✅ **Authorization**
  - Role-based access control (Admin/Volunteer)
  - Route protection with decorators
  - Unauthorized access prevention
  
- ✅ **File Security**
  - Secure filename generation
  - Upload folder isolation
  - File type validation

---

## 📦 Installation & Setup

### **Prerequisites**
- Python 3.9 or higher
- Windows/Mac/Linux
- pip package manager
- Virtual environment (recommended)
- Google Gemini API Key (free from [AI Studio](https://aistudio.google.com/app/apikeys))

### **Step 1: Clone/Download Project**

```bash
cd path/to/Event\ Management
```

### **Step 2: Create Virtual Environment**

**Windows:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 4: Configure Environment Variables**

Copy `.env.example` to `.env`:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` file:

```env
SECRET_KEY=your-secure-random-key-here
FLASK_ENV=development
FLASK_DEBUG=1
GEMINI_API_KEY=your-gemini-api-key-here
```

### **Step 5: Get Gemini API Key (FREE)**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Click **"Create API Key"**
3. Copy the key to your `.env` file
4. No billing required for free tier!

### **Step 6: Run Application**

```bash
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### **Step 7: Access Application**

Open browser: **http://localhost:5000**

---

## ⚙️ Configuration

### **Environment Variables (.env)**

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session encryption key | `super-secret-key-123` |
| `FLASK_ENV` | Environment mode | `development` or `production` |
| `FLASK_DEBUG` | Debug mode (0/1) | `1` for dev, `0` for prod |
| `DATABASE_URL` | Database connection string | `sqlite:///ems.db` |
| `UPLOAD_FOLDER` | Directory for file uploads | `uploads/` |
| `GEMINI_API_KEY` | Google Gemini AI API key | `AIza...` |

### **Database Configuration**

**Default (SQLite):**
```
No configuration needed. File auto-created as `ems.db`
```

**PostgreSQL (Optional):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ems_db
```

### **Application Configuration (app.py)**

```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///ems.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
```

---

## 🚀 Usage Guide

### **Initial Setup**

First run creates sample data:

**Seeded Accounts:**
```
Admin User:
  Email: admin@example.com
  Password: adminpass
  Role: admin

Volunteer 1:
  Email: alice@example.com
  Password: alicepass
  Role: volunteer

Volunteer 2:
  Email: bob@example.com
  Password: bobpass
  Role: volunteer

Sample Events:
  - Community Clean-up (Park)
  - Food Drive (Community Center)

Sample Tasks:
  - Pick up trash
  - Sort recyclables
  - Accept donations
```

### **Admin Workflow**

**1. Login:**
- Go to login page
- Email: `admin@example.com`
- Password: `adminpass`

**2. Create Event:**
- Click "Manage Events"
- Click "New Event"
- Fill: Title, Date, Venue, Time, Description
- Save

**3. Create Task:**
- Click "Manage Tasks"
- Click "New Task"
- Select Event
- Enter Task Name, Times
- Save

**4. Assign Volunteers:**
- In Tasks list
- Click "Assign"
- Select volunteer
- Confirm

**5. Review Submissions:**
- Click "View Submissions"
- Review volunteer work
- Approve/Reject

**6. Use AI Assistant:**
- Click "🤖 AI Assistant"
- Ask: "How do I manage multiple events?"
- Get instant guidance!

### **Volunteer Workflow**

**1. Login:**
- Email: `alice@example.com`
- Password: `alicepass`

**2. View Tasks:**
- Check "My Tasks" dashboard
- See assigned tasks with details

**3. Submit Work:**
- Click "Submit" on task
- Upload file (document/image)
- Add comment
- Click "Submit"

**4. Mark Attendance:**
- Click "Mark Attendance"
- Select present/absent
- Confirm

**5. Ask Question:**
- Click "Ask Admin"
- Type question
- Admin responds

**6. Get Help:**
- Click "🤖 AI Assistant"
- Ask: "How do I submit my task?"
- Get step-by-step guidance!

---

## 💾 Database Schema

### **Users Table**
```sql
CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password VARCHAR(200) NOT NULL,
  role VARCHAR(20) NOT NULL  -- 'admin' or 'volunteer'
);
```

### **Events Table**
```sql
CREATE TABLE event (
  id INTEGER PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  date DATE NOT NULL,
  venue VARCHAR(200),
  start_time TIME,
  end_time TIME,
  description TEXT
);
```

### **Tasks Table**
```sql
CREATE TABLE task (
  id INTEGER PRIMARY KEY,
  event_id INTEGER FOREIGN KEY,
  task_name VARCHAR(200) NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',  -- 'pending' or 'completed'
  est_start TIME,
  est_end TIME
);
```

### **Assignments Table (Task-Volunteer Junction)**
```sql
CREATE TABLE assignment (
  id INTEGER PRIMARY KEY,
  task_id INTEGER FOREIGN KEY,
  user_id INTEGER FOREIGN KEY,
  UNIQUE(task_id, user_id)  -- Prevent duplicate assignments
);
```

### **Submissions Table**
```sql
CREATE TABLE submission (
  id INTEGER PRIMARY KEY,
  task_id INTEGER FOREIGN KEY,
  user_id INTEGER FOREIGN KEY,
  filename VARCHAR(300) NOT NULL,
  comment TEXT,
  submitted_at DATETIME DEFAULT NOW(),
  status VARCHAR(20) DEFAULT 'pending'  -- 'pending', 'approved', 'rejected'
);
```

### **Attendance Table**
```sql
CREATE TABLE attendance (
  id INTEGER PRIMARY KEY,
  event_id INTEGER FOREIGN KEY,
  user_id INTEGER FOREIGN KEY,
  status VARCHAR(20) DEFAULT 'absent',  -- 'present' or 'absent'
  UNIQUE(event_id, user_id)
);
```

### **Queries Table**
```sql
CREATE TABLE query (
  id INTEGER PRIMARY KEY,
  event_id INTEGER FOREIGN KEY,
  user_id INTEGER FOREIGN KEY,
  message TEXT NOT NULL,
  response TEXT,
  created_at DATETIME DEFAULT NOW()
);
```

### **Entity Relationship Diagram**

```
┌──────────┐                ┌────────┐
│   User   │                │ Event  │
├──────────┤                ├────────┤
│ id (PK)  │                │ id (PK)│
│ name     │                │ title  │
│ email    │                │ date   │
│ password │                │ venue  │
│ role     │                │ desc   │
└──────────┘                └────────┘
      │                           │
      │ 1:N                       │ 1:N
      │                           │
      ▼                           ▼
┌──────────────┐           ┌──────────┐
│  Assignment  │           │  Task    │
├──────────────┤           ├──────────┤
│ id (PK)      │           │ id (PK)  │
│ task_id (FK) │◄──────────┤ event_id │
│ user_id (FK) │──────┐    │ name     │
└──────────────┘      │    │ status   │
                      │    └──────────┘
                      │        │ 1:N
                      │        │
                      │        ▼
                      │   ┌──────────────┐
                      │   │ Submission   │
                      │   ├──────────────┤
                      │   │ id (PK)      │
                      │   │ task_id (FK) │
                      │   │ user_id (FK) │
                      │   │ filename     │
                      │   │ status       │
                      └───┤ submitted_at │
                          └──────────────┘

User ──1:N──► Attendance ◄──N:1── Event
User ──1:N──► Query ◄──N:1── Event
```

---

## 🔌 API Endpoints

### **Authentication Routes**
```
GET  /               → Home page (redirects to dashboard if logged in)
GET  /register       → Registration form
POST /register       → Process registration
GET  /login          → Login form
POST /login          → Process login
GET  /logout         → Logout (redirects to home)
```

### **Admin Routes**
```
GET  /admin                                    → Dashboard (analytics)
GET  /admin/events                             → List all events
GET  /admin/events/new                         → New event form
POST /admin/events/new                         → Create event
GET  /admin/events/<id>/edit                   → Edit event form
POST /admin/events/<id>/edit                   → Update event
POST /admin/events/<id>/delete                 → Delete event

GET  /admin/tasks                              → List all tasks
GET  /admin/tasks/new                          → New task form
POST /admin/tasks/new                          → Create task
POST /admin/tasks/<id>/assign                  → Assign task to volunteer
POST /admin/tasks/<id>/status                  → Update task status

GET  /admin/submissions                        → View all submissions
POST /admin/submissions/<id>/approve           → Approve/Reject submission

GET  /admin/attendance/<event_id>/mark         → Mark attendance form
POST /admin/attendance/<event_id>/mark         → Save attendance

GET  /admin/query/<id>/reply                   → Reply form
POST /admin/query/<id>/reply                   → Submit reply
```

### **Volunteer Routes**
```
GET  /volunteer                                 → Dashboard (my tasks)

POST /volunteer/task/<id>/complete             → Mark task complete
POST /volunteer/task/<id>/submit               → Submit task work

POST /volunteer/query/<event_id>               → Submit query to admin

POST /volunteer/attendance/<event_id>/mark     → Mark own attendance
```

### **Chatbot Routes**
```
GET  /chatbot                                   → AI Assistant page
POST /api/chat                                  → Chat API (JSON)
     Request:  { "message": "user text" }
     Response: { "response": "ai text" }
```

### **Utility Routes**
```
GET  /uploads/<filename>                        → Download uploaded file
```

---

## 🔐 Security & Deployment

### **Security Best Practices**

**1. API Key Protection:**
```env
# .env file (DO NOT COMMIT)
GEMINI_API_KEY=your-secret-key

# .gitignore
.env
.env.local
```

**2. Password Hashing:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Create: hashed = generate_password_hash(password)
# Verify: check_password_hash(hashed, password)
```

**3. Session Security:**
```python
app.config['SECRET_KEY'] = 'change-this-to-random-key-in-production'
```

**4. CSRF Protection (if needed):**
```
# Add Flask-WTF for CSRF tokens in forms
pip install Flask-WTF
```

### **Deployment Checklist**

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=0`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure secure `GEMINI_API_KEY` in hosting environment
- [ ] Use HTTPS only
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable logging and monitoring
- [ ] Regular database backups
- [ ] Rate limiting on API endpoints

### **Production Setup (Example with Gunicorn + Nginx)**

**1. Install Gunicorn:**
```bash
pip install gunicorn
```

**2. Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**3. Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Environment-Specific Configuration**

**Development:**
```
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///ems.db
```

**Production:**
```
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=postgresql://user:pass@host/dbname
```

---

## 👥 Team & Credits

### **Developed by (B.Tech 3rd Year Mini Project)**

**Team Members:**
- 👨‍💻 **Karimulla**
- 👨‍💻 **Prasad**
- 👨‍💻 **Fawaz**

**Institution:**
- **Department:** Artificial Intelligence & Data Science
- **University:** Dhanalakshmi Srinivasan University
- **Location:** Trichy - 621112, India
- **Year:** 3rd Year (2025-2026)

### **Technology Credits**

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Bootstrap** - UI framework
- **Google Gemini** - AI Chatbot
- **SQLite** - Database
- **Werkzeug** - Security utilities

### **Project Duration**

- **Started:** January 2026
- **Completed:** February 2026
- **Version:** 1.0.0

---

## 📞 Support & Troubleshooting

### **Common Issues**

**1. "Module not found" error:**
```bash
# Solution: Activate virtual environment
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

**2. Database locked:**
```bash
# Solution: Delete ems.db and restart
rm ems.db
python app.py
```

**3. Gemini API not working:**
- Verify API key in `.env`
- Check internet connection
- Ensure quota not exceeded at [AI Studio Dashboard](https://aistudio.google.com/app/apikeys)

**4. Port already in use:**
```python
# In app.py, change port:
app.run(port=5001)
```

### **Useful Commands**

```bash
# Run app
python app.py

# Install packages
pip install -r requirements.txt

# Activate venv (Windows)
venv\Scripts\Activate.ps1

# Deactivate venv
deactivate

# Check Python version
python --version
```

---

## 📄 License

This project is developed as an academic mini project for educational purposes.

---

## 🙏 Acknowledgments

- Prof. for guidance and support
- DSU for infrastructure and resources
- Open-source community for amazing frameworks
- Google for free Gemini API tier

---

**Last Updated:** February 2026  
**Status:** ✅ Production Ready  
**Version:** 1.0.0

For questions or support, contact the development team at the Department of AI & Data Science, DSU.

---

**Made with ❤️ by Karimulla, Prasad, and Fawaz**

