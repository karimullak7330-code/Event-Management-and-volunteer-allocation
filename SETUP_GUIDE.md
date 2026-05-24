# ⚡ QUICK SETUP GUIDE
## Event Management & Volunteer Allocation System

**👥 Team:** Karimulla, Prasad, Fawaz  
**🏫 Institution:** Dhanalakshmi Srinivasan University  
**📚 Department:** Artificial Intelligence & Data Science  
**📦 Version:** 1.0.0 (Production Ready)

---

## 🚀 5-Minute Setup

### 1️⃣ Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2️⃣ Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3️⃣ Get Free Gemini API Key
1. Go to: https://aistudio.google.com/app/apikeys
2. Click **"Create API Key"**
3. Copy the key

### 4️⃣ Configure Environment
```powershell
copy .env.example .env
```

Edit `.env`:
```env
SECRET_KEY=any-random-string-here
GEMINI_API_KEY=paste-your-key-here
```

### 5️⃣ Run Application
```powershell
python app.py
```

✅ Open: **http://localhost:5000**

---

## 🔐 Test Accounts (Auto-Created)

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | adminpass |
| Volunteer | alice@example.com | alicepass |
| Volunteer | bob@example.com | bobpass |

---

## 🎨 Features at a Glance

### 👑 Admin Dashboard
- ✅ Create & manage events
- ✅ Assign tasks to volunteers
- ✅ Review & approve submissions
- ✅ Track attendance
- ✅ Respond to volunteer questions
- ✅ Get AI-powered guidance

### 👤 Volunteer Dashboard
- ✅ View assigned tasks
- ✅ Submit work (upload files)
- ✅ Mark attendance
- ✅ Ask questions to admin
- ✅ Get AI assistance

### 🤖 AI Assistant (Gemini)
- ✅ Available to both admin & volunteers
- ✅ Context-aware responses
- ✅ Role-specific guidance
- ✅ Real-time chat interface

---

## 📁 Project Structure

```
Event Management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (CREATE THIS)
├── .env.example          # Template for .env
├── .gitignore            # Git ignore rules
├── ems.db                # SQLite database (auto-created)
├── README.md             # Comprehensive documentation
├── static/
│   └── style.css         # Styling with footer
├── templates/
│   ├── base.html         # Base template with footer & nav
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── chatbot.html      # NEW: AI Assistant page
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── events.html
│   │   ├── event_form.html
│   │   ├── tasks.html
│   │   ├── task_form.html
│   │   ├── submissions.html
│   │   └── queries.html
│   └── volunteer/
│       └── dashboard.html
└── uploads/              # User-uploaded files
```

---

## 🔑 Key Technologies

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, JavaScript |
| **Backend** | Python 3.9+, Flask 2.2.5 |
| **Database** | SQLite (Default), PostgreSQL (Optional) |
| **ORM** | SQLAlchemy 3.0.3 |
| **Auth** | Flask-Login 0.6.2 |
| **Security** | Werkzeug 2.2.3 |
| **AI** | Google Gemini API |
| **Env Management** | python-dotenv 1.0.0 |

---

## ✨ What's New (Gemini AI Integration)

✅ **AI Chatbot** - Click "🤖 AI Assistant" from navbar
✅ **Context-Aware** - Different responses for admin vs volunteer
✅ **Real-Time** - Instant responses with typing indicators
✅ **Secure API Key** - Stored in .env (not in GitHub)
✅ **Free Tier** - No billing required
✅ **Footer** - Team credit at bottom of every page

---

## 🔒 Security Setup

### .gitignore (Already Created)
Protects:
- `.env` - API keys & secrets
- `ems.db` - Database
- `venv/` - Virtual environment
- `__pycache__/` - Python cache

### Password Security
- All passwords hashed using Werkzeug
- Session management via Flask-Login
- CSRF protection ready (needs Flask-WTF if needed)

---

## 🐛 Troubleshooting

### "Module not found"
```powershell
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Port already in use"
```python
# In app.py, change:
app.run(port=5001)
```

### "Gemini API error"
- Check `.env` has API key
- Visit: https://aistudio.google.com/app/apikeys
- Ensure internet connection

### "Database error"
```powershell
# Delete & recreate:
rm ems.db
python app.py
```

---

## 📊 Database Models

7 Core Models:
1. **User** - Admin/Volunteer accounts
2. **Event** - Event information
3. **Task** - Event tasks
4. **Assignment** - Task-Volunteer mapping
5. **Submission** - Work submissions
6. **Attendance** - Event attendance
7. **Query** - Admin-Volunteer communication

---

## 🌐 API Endpoints (Key Routes)

```
Authentication:
  POST /register → Create account
  POST /login → Login
  GET  /logout → Logout

Admin:
  GET  /admin → Dashboard
  GET  /admin/events → Events CRUD
  GET  /admin/tasks → Tasks & assignments
  GET  /admin/submissions → Review work

Volunteer:
  GET  /volunteer → Dashboard
  POST /volunteer/task/<id>/submit → Upload work
  POST /volunteer/attendance/<id>/mark → Attendance

Chatbot:
  GET  /chatbot → Chat interface
  POST /api/chat → Chat API (JSON)
```

---

## 📝 Usage Example

### Admin: Create Event
1. Login with admin credentials
2. Click "Manage Events"
3. Click "New Event"
4. Fill: Title, Date, Venue, Description
5. Save & assign tasks

### Volunteer: Submit Task
1. Login with volunteer credentials
2. View "My Tasks"
3. Click "Submit"
4. Upload file + add comment
5. Admin reviews & approves

### Both: Use AI Assistant
1. Click "🤖 AI Assistant" (navbar)
2. Ask question: "How do I create an event?" (admin) or "How do I submit work?" (volunteer)
3. Get instant, context-aware guidance

---

## 🚀 Deployment Notes

### Development (Local)
```env
FLASK_ENV=development
FLASK_DEBUG=1
```

### Production (Online)
```env
FLASK_ENV=production
FLASK_DEBUG=0
```

### Recommended Production Stack
- **Server:** Gunicorn
- **Proxy:** Nginx
- **DB:** PostgreSQL
- **Hosting:** Heroku, DigitalOcean, AWS, Azure

---

## 📞 Quick Help

**Something not working?**
1. Check `.env` file has `GEMINI_API_KEY`
2. Ensure `pip install -r requirements.txt` completed
3. Verify virtual environment is activated
4. Check firewall allows port 5000
5. Delete `ems.db` and restart if database locked

**Want to customize?**
- Colors: Edit `static/style.css`
- Layout: Edit `templates/base.html`
- Database: Edit models in `app.py`
- Chatbot behavior: Edit `get_ai_response()` in `app.py`

---

## 📚 Documentation Links

- **Full README:** See [README.md](README.md) for complete documentation
- **Gemini API:** https://ai.google.dev/
- **Flask Docs:** https://flask.palletsprojects.com/
- **SQLAlchemy:** https://www.sqlalchemy.org/
- **Bootstrap:** https://getbootstrap.com/

---

## 👥 Credits

**Developed by (B.Tech 3rd Year Mini Project):**
- 👨‍💻 Karimulla
- 👨‍💻 Prasad
- 👨‍💻 Fawaz

**Department:** Artificial Intelligence & Data Science  
**University:** Dhanalakshmi Srinivasan University, Trichy  
**Year:** 2025-2026  
**Status:** ✅ Production Ready

---

**Happy Volunteering! 🎉**

*For PowerPoint presentation, use the comprehensive README.md with all architecture diagrams, tech stack, and features.*
