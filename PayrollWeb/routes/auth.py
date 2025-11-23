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
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('auth.index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validate
            if len(username) < 4:
                flash('Tên đăng nhập phải có ít nhất 4 ký tự!', 'danger')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Mật khẩu phải có ít nhất 6 ký tự!', 'danger')
                return render_template('register.html')
            
            if password != confirm_password:
                flash('Mật khẩu xác nhận không khớp!', 'danger')
                return render_template('register.html')
            
            # Kiểm tra username đã tồn tại
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Tên đăng nhập đã tồn tại!', 'danger')
                return render_template('register.html')
            
            # Tạo nhân viên mới
            employee = Employee(
                full_name=full_name,
                phone=phone,
                email=email,
                position='Nhân viên',
                daily_wage=300000,  # Lương mặc định
                start_date=datetime.now(),
                status='active'
            )
            db.session.add(employee)
            db.session.flush()
            
            # Tạo user mới
            user = User(username=username, role='user', employee_id=employee.id)
            user.set_password(password)
            db.session.add(user)
            
            db.session.commit()
            
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất!', 'info')
    return redirect(url_for('auth.login'))
