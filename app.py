from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
try:
    from flask_sqlalchemy import SQLAlchemy
except ImportError as e:
    raise ImportError("Missing dependency 'Flask-SQLAlchemy'. Run 'pip install -r requirements.txt' or activate the virtualenv.") from e
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv
import time

# google-generativeai is optional; if unavailable the chatbot will be disabled
try:
    import google.generativeai as genai
    _genai_available = True
except ImportError:
    _genai_available = False
from functools import wraps

load_dotenv()

# Initialize Gemini AI only if the library is present and key provided
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if _genai_available and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    CHATBOT_ENABLED = True
else:
    CHATBOT_ENABLED = False

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret')
db_path = os.path.join(os.path.dirname(__file__), 'ems.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'uploads'))
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'volunteer'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(200))
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    description = db.Column(db.Text)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    task_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending/completed
    est_start = db.Column(db.Time, nullable=True)
    est_end = db.Column(db.Time, nullable=True)
    event = db.relationship('Event', backref=db.backref('tasks', cascade='all,delete'))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('assignments', cascade='all,delete'))
    user = db.relationship('User', backref='assignments')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='absent')  # present/absent
    event = db.relationship('Event', backref=db.backref('attendances', cascade='all,delete'))
    user = db.relationship('User', backref='attendances')


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    comment = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending/approved/rejected
    task = db.relationship('Task', backref=db.backref('submissions', cascade='all,delete'))
    user = db.relationship('User', backref='submissions')


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    event = db.relationship('Event', backref=db.backref('queries', cascade='all,delete'))
    user = db.relationship('User', backref='queries')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Role check decorator
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role != role:
                flash('Access denied')
                return redirect(url_for('index'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Rate limiting for Gemini API (free tier has low limits)
api_request_times = {}
MAX_REQUESTS_PER_MINUTE = 3  # Conservative limit for free tier

def is_rate_limited(user_id):
    """Check if user has exceeded rate limit"""
    now = time.time()
    if user_id not in api_request_times:
        api_request_times[user_id] = []
    
    # Remove requests older than 1 minute
    api_request_times[user_id] = [t for t in api_request_times[user_id] if now - t < 60]
    
    if len(api_request_times[user_id]) >= MAX_REQUESTS_PER_MINUTE:
        return True
    
    api_request_times[user_id].append(now)
    return False

# Gemini AI Chat function
def get_ai_response(user_message, user_name, user_role, user_id=None):
    """Get response from Gemini AI with context"""
    if not CHATBOT_ENABLED:
        return "AI Assistant is not configured. Please set GEMINI_API_KEY in environment."
    
    # Check rate limit
    if user_id and is_rate_limited(user_id):
        return "⏱️ You're sending messages too quickly. Please wait a moment before sending another message. (Rate limit: 3 messages per minute)"
    
    try:
        # Build context for the AI
        context = f"""You are a helpful AI Assistant for the Event Management & Volunteer Allocation System.
        
User Information:
- Name: {user_name}
- Role: {user_role}
- Event System: Manages events, tasks, volunteer assignments, and submissions

Your responsibilities:
- Help users understand their tasks and roles
- Provide guidance on event management (for admins)
- Answer questions about volunteer assignments
- Assist with task submissions and attendance
- Provide general event management advice
- Be concise and professional

Remember to:
1. Keep responses brief and helpful
2. If user is a volunteer, focus on their assigned tasks
3. If user is an admin, provide event management guidance
4. Always maintain a supportive tone"""

        try:
            # Try latest model first
            model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception:
            # Fallback to older model if latest not available
            model = genai.GenerativeModel('gemini-pro')
        
        full_prompt = f"{context}\n\nUser ({user_role}): {user_message}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        error_str = str(e)
        # Handle rate limit errors
        if "429" in error_str or "quota" in error_str.lower():
            return "⚠️ API quota exceeded. The free tier Gemini API has reached its daily limit. Please try again tomorrow or upgrade your API plan at https://ai.google.dev/pricing"
        # Handle model not found errors
        elif "404" in error_str or "not found" in error_str.lower():
            return "⚠️ The AI model is temporarily unavailable. Please try again later."
        # Generic error
        else:
            return f"⚠️ Chatbot unavailable: {error_str[:100]}. Please try again later."

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('volunteer_dashboard'))
    events = Event.query.order_by(Event.date).all()
    return render_template('index.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        role = request.form.get('role', 'volunteer')
        if not name or not email or not password:
            flash('Please fill required fields')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        user = User(name=name, email=email, password=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registered. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

### Admin routes ###
@app.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    events = Event.query.order_by(Event.date.desc()).all()
    tasks = Task.query.all()
    # summary
    total_tasks = len(tasks)
    completed = len([t for t in tasks if t.status == 'completed'])
    pending = total_tasks - completed
    attendances = Attendance.query.all()
    present = len([a for a in attendances if a.status == 'present'])
    return render_template('admin/dashboard.html', events=events, total_tasks=total_tasks,
                           completed=completed, pending=pending, present=present)


@app.route('/admin/submissions')
@login_required
@role_required('admin')
def admin_submissions():
    subs = Submission.query.order_by(Submission.submitted_at.desc()).all()
    return render_template('admin/submissions.html', submissions=subs)


@app.route('/admin/submissions/<int:sub_id>/approve', methods=['POST'])
@login_required
@role_required('admin')
def approve_submission(sub_id):
    sub = Submission.query.get_or_404(sub_id)
    sub.status = request.form.get('status', 'approved')
    db.session.commit()
    flash('Submission updated')
    return redirect(url_for('admin_submissions'))


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin/events')
@login_required
@role_required('admin')
def admin_events():
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('admin/events.html', events=events)

@app.route('/admin/events/new', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def new_event():
    if request.method == 'POST':
        title = request.form['title']
        date_str = request.form['date']
        location = request.form['location']
        description = request.form['description']
        if not title or not date_str:
            flash('Title and date required')
            return redirect(url_for('new_event'))
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        st = datetime.strptime(start_time, '%H:%M').time() if start_time else None
        et = datetime.strptime(end_time, '%H:%M').time() if end_time else None
        ev = Event(title=title, date=datetime.strptime(date_str, '%Y-%m-%d').date(), venue=location, start_time=st, end_time=et, description=description)
        db.session.add(ev)
        db.session.commit()
        flash('Event created')
        return redirect(url_for('admin_events'))
    return render_template('admin/event_form.html', event=None)

@app.route('/admin/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.venue = request.form['location']
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        event.start_time = datetime.strptime(start_time, '%H:%M').time() if start_time else None
        event.end_time = datetime.strptime(end_time, '%H:%M').time() if end_time else None
        event.description = request.form['description']
        db.session.commit()
        flash('Event updated')
        return redirect(url_for('admin_events'))
    return render_template('admin/event_form.html', event=event)

@app.route('/admin/events/<int:event_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted')
    return redirect(url_for('admin_events'))

@app.route('/admin/tasks')
@login_required
@role_required('admin')
def admin_tasks():
    tasks = Task.query.order_by(Task.id.desc()).all()
    events = Event.query.order_by(Event.date).all()
    volunteers = User.query.filter_by(role='volunteer').all()
    return render_template('admin/tasks.html', tasks=tasks, events=events, volunteers=volunteers)

@app.route('/admin/tasks/new', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def new_task():
    if request.method == 'POST':
        event_id = request.form['event_id']
        task_name = request.form['task_name']
        est_start = request.form.get('est_start')
        est_end = request.form.get('est_end')
        est_s = datetime.strptime(est_start, '%H:%M').time() if est_start else None
        est_e = datetime.strptime(est_end, '%H:%M').time() if est_end else None
        if not event_id or not task_name:
            flash('Event and task name required')
            return redirect(url_for('new_task'))
        t = Task(event_id=event_id, task_name=task_name, est_start=est_s, est_end=est_e)
        db.session.add(t)
        db.session.commit()
        flash('Task created')
        return redirect(url_for('admin_tasks'))
    events = Event.query.order_by(Event.date).all()
    return render_template('admin/task_form.html', events=events, task=None)

@app.route('/admin/tasks/<int:task_id>/assign', methods=['POST'])
@login_required
@role_required('admin')
def assign_task(task_id):
    user_id = request.form.get('user_id')
    task = Task.query.get_or_404(task_id)
    if not user_id:
        flash('Select a volunteer')
        return redirect(url_for('admin_tasks'))
    # avoid duplicate
    if Assignment.query.filter_by(task_id=task.id, user_id=user_id).first():
        flash('Volunteer already assigned')
        return redirect(url_for('admin_tasks'))
    a = Assignment(task_id=task.id, user_id=user_id)
    db.session.add(a)
    db.session.commit()
    flash('Assigned')
    return redirect(url_for('admin_tasks'))

@app.route('/admin/tasks/<int:task_id>/status', methods=['POST'])
@login_required
@role_required('admin')
def change_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    new = request.form.get('status')
    if new in ('pending', 'completed'):
        task.status = new
        db.session.commit()
    return redirect(url_for('admin_tasks'))

@app.route('/admin/attendance/<int:event_id>/mark', methods=['POST'])
@login_required
@role_required('admin')
def mark_attendance(event_id):
    user_id = request.form.get('user_id')
    status = request.form.get('status')
    if not user_id or status not in ('present', 'absent'):
        flash('Invalid')
        return redirect(url_for('admin_dashboard'))
    att = Attendance.query.filter_by(event_id=event_id, user_id=user_id).first()
    if not att:
        att = Attendance(event_id=event_id, user_id=user_id, status=status)
        db.session.add(att)
    else:
        att.status = status
    db.session.commit()
    flash('Attendance updated')
    return redirect(url_for('admin_dashboard'))

### Volunteer routes ###
@app.route('/volunteer')
@login_required
@role_required('volunteer')
def volunteer_dashboard():
    # assigned tasks
    assignments = Assignment.query.filter_by(user_id=current_user.id).all()
    tasks = [a.task for a in assignments]
    events = {t.event for t in tasks}
    return render_template('volunteer/dashboard.html', tasks=tasks, events=events)

@app.route('/volunteer/task/<int:task_id>/complete', methods=['POST'])
@login_required
@role_required('volunteer')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    # ensure assigned
    if not Assignment.query.filter_by(task_id=task.id, user_id=current_user.id).first():
        flash('Not assigned to this task')
        return redirect(url_for('volunteer_dashboard'))
    task.status = 'completed'
    db.session.commit()
    flash('Task marked complete')
    return redirect(url_for('volunteer_dashboard'))

@app.route('/volunteer/task/<int:task_id>/submit', methods=['POST'])
@login_required
@role_required('volunteer')
def submit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not Assignment.query.filter_by(task_id=task.id, user_id=current_user.id).first():
        flash('Not assigned')
        return redirect(url_for('volunteer_dashboard'))
    if 'file' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('volunteer_dashboard'))
    file = request.files['file']
    comment = request.form.get('comment')
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('volunteer_dashboard'))
    filename = secure_filename(f"{current_user.id}_{int(datetime.utcnow().timestamp())}_{file.filename}")
    dest = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(dest)
    sub = Submission(task_id=task.id, user_id=current_user.id, filename=filename, comment=comment)
    db.session.add(sub)
    db.session.commit()
    flash('Submission uploaded')
    return redirect(url_for('volunteer_dashboard'))

@app.route('/volunteer/query/<int:event_id>', methods=['POST'])
@login_required
@role_required('volunteer')
def volunteer_query(event_id):
    message = request.form.get('message')
    if not message:
        flash('Message required')
        return redirect(url_for('volunteer_dashboard'))
    q = Query(event_id=event_id, user_id=current_user.id, message=message)
    db.session.add(q)
    db.session.commit()
    flash('Question submitted')
    return redirect(url_for('volunteer_dashboard'))

@app.route('/volunteer/attendance/<int:event_id>/mark', methods=['POST'])
@login_required
@role_required('volunteer')
def volunteer_attendance(event_id):
    status = request.form.get('status')
    if status not in ('present', 'absent'):
        flash('Invalid')
        return redirect(url_for('volunteer_dashboard'))
    att = Attendance.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if not att:
        att = Attendance(event_id=event_id, user_id=current_user.id, status=status)
        db.session.add(att)
    else:
        att.status = status
    db.session.commit()
    flash('Attendance saved')
    return redirect(url_for('volunteer_dashboard'))

@app.route('/admin/query/<int:query_id>/reply', methods=['POST'])
@login_required
@role_required('admin')
def admin_reply(query_id):
    q = Query.query.get_or_404(query_id)
    q.response = request.form.get('response')
    db.session.commit()
    flash('Reply saved')
    return redirect(url_for('admin_dashboard'))

### AI Chatbot Routes ###
@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """API endpoint for AI chatbot"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    if not CHATBOT_ENABLED:
        return jsonify({'error': 'AI Assistant not configured'}), 503
    
    # Get AI response
    ai_response = get_ai_response(
        user_message, 
        current_user.name, 
        current_user.role,
        current_user.id
    )
    
    return jsonify({'response': ai_response})

@app.route('/chatbot')
@login_required
def chatbot_page():
    """Chatbot page for users"""
    return render_template('chatbot.html', chatbot_enabled=CHATBOT_ENABLED)

### Helpers and seed ###
def seed_data():
    if User.query.first():
        return
    admin = User(name='Admin Organizer', email='admin@example.com', password=generate_password_hash('adminpass'), role='admin')
    v1 = User(name='Alice Volunteer', email='alice@example.com', password=generate_password_hash('alicepass'), role='volunteer')
    v2 = User(name='Bob Volunteer', email='bob@example.com', password=generate_password_hash('bobpass'), role='volunteer')
    e1 = Event(title='Community Clean-up', date=date.today(), venue='Town Park', description='Cleanup event')
    e2 = Event(title='Food Drive', date=date.today(), venue='Community Center', description='Collect food donations')
    db.session.add_all([admin, v1, v2, e1, e2])
    db.session.commit()
    t1 = Task(event_id=e1.id, task_name='Pick up trash', status='pending')
    t2 = Task(event_id=e1.id, task_name='Sort recyclables', status='pending')
    t3 = Task(event_id=e2.id, task_name='Accept donations', status='pending')
    db.session.add_all([t1, t2, t3])
    db.session.commit()
    a1 = Assignment(task_id=t1.id, user_id=v1.id)
    a2 = Assignment(task_id=t3.id, user_id=v2.id)
    db.session.add_all([a1, a2])
    db.session.commit()

if __name__ == '__main__':
    # Ensure DB tables exist and seed sample data if needed
    with app.app_context():
        db.create_all()
        seed_data()
    debug_mode = os.environ.get('FLASK_DEBUG', '1')
    app.run(debug=bool(int(debug_mode)))
