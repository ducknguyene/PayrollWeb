from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Employee
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('employee.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successfully!', 'success')
            return redirect(url_for('auth.index'))
        else:
            flash('Incorrect username or password!', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        try:
            # Retrieve date from form
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validate
            if len(username) < 4:
                flash('Username must have at least 4 characters!', 'danger')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Password must have at least 6 characters!', 'danger')
                return render_template('register.html')
            
            if password != confirm_password:
                flash('Password does not match!', 'danger')
                return render_template('register.html')
            
            # Check for existed username
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username is already in use!', 'danger')
                return render_template('register.html')
            
            # Add new employee
            employee = Employee(
                full_name=full_name,
                phone=phone,
                email=email,
                position='Employee',
                daily_wage=300000,  # Base salary
                start_date=datetime.now(),
                status='active'
            )
            db.session.add(employee)
            db.session.flush()
            
            # Create new user
            user = User(username=username, role='user', employee_id=employee.id)
            user.set_password(password)
            db.session.add(user)
            
            db.session.commit()
            
            flash('Sign-up successfully! Please log-in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged-out!', 'info')
    return redirect(url_for('auth.login'))
