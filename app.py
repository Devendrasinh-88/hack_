import os
import logging
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
login_manager.login_view = 'login'

# Import routes after app initialization to avoid circular imports
from models import User, Project
from forms import LoginForm, RegistrationForm, ProjectForm
from utils import generate_project_id, check_duplicates

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html', form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        logger.debug(f"Login attempt for username: {form.username.data}")
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            logger.info(f"User {user.username} logged in successfully")
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        logger.warning(f"Failed login attempt for username: {form.username.data}")
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form, title='Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.all()
    stats = {
        'total': len(projects),
        'ongoing': len([p for p in projects if p.status == 'ongoing']),
        'completed': len([p for p in projects if p.status == 'completed'])
    }
    return render_template('dashboard.html', stats=stats, projects=projects[:5])

@app.route('/projects')
@login_required
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project_id = generate_project_id(form.village_code.data, form.project_type.data)
        
        # Check for duplicates
        duplicates = check_duplicates(
            form.village_code.data,
            form.project_type.data,
            form.location.data
        )
        
        if duplicates:
            flash('Warning: Similar projects detected in the area', 'warning')
        
        project = Project(
            project_id=project_id,
            name=form.name.data,
            project_type=form.project_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            cost=form.cost.data,
            location=form.location.data,
            contractor=form.contractor.data,
            village_code=form.village_code.data
        )
        
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully', 'success')
        return redirect(url_for('projects'))
    
    return render_template('new_project.html', form=form)

@app.route('/analytics')
@login_required
def analytics():
    projects = Project.query.all()
    data = {
        'project_types': {},
        'status_distribution': {},
        'monthly_costs': {}
    }
    
    for project in projects:
        # Project type distribution
        data['project_types'][project.project_type] = \
            data['project_types'].get(project.project_type, 0) + 1
        
        # Status distribution
        data['status_distribution'][project.status] = \
            data['status_distribution'].get(project.status, 0) + 1
        
        # Monthly cost distribution
        month = project.start_date.strftime('%Y-%m')
        data['monthly_costs'][month] = \
            data['monthly_costs'].get(month, 0) + project.cost
    
    return render_template('analytics.html', data=data)

# Initialize database
with app.app_context():
    db.create_all()

    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()