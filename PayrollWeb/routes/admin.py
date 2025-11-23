from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Employee, User, Attendance
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Bạn không có quyền truy cập!', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_employees = Employee.query.count()
    active_employees = Employee.query.filter_by(status='active').count()
    return render_template('admin/dashboard.html', 
                         total_employees=total_employees,
                         active_employees=active_employees)

# ==================== QUẢN LÝ NHÂN VIÊN ====================

@admin_bp.route('/employees')
@login_required
@admin_required
def employees():
    search = request.args.get('search', '')
    if search:
        employees = Employee.query.filter(
            db.or_(
                Employee.full_name.contains(search),
                Employee.phone.contains(search),
                Employee.email.contains(search)
            )
        ).all()
    else:
        employees = Employee.query.all()
    return render_template('admin/employees.html', employees=employees, search=search)

@admin_bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_employee():
    if request.method == 'POST':
        try:
            # Tạo nhân viên mới
            employee = Employee(
                full_name=request.form.get('full_name'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                position=request.form.get('position'),
                daily_wage=float(request.form.get('daily_wage')),
                start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d'),
                status=request.form.get('status', 'active')
            )
            db.session.add(employee)
            db.session.flush()  # Để lấy employee.id
            
            # Tạo tài khoản đăng nhập
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username and password:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    flash('Tên đăng nhập đã tồn tại!', 'danger')
                    db.session.rollback()
                    return render_template('admin/add_employee.html')
                
                user = User(username=username, role='user', employee_id=employee.id)
                user.set_password(password)
                db.session.add(user)
            
            db.session.commit()
            flash('Thêm nhân viên thành công!', 'success')
            return redirect(url_for('admin.employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    return render_template('admin/add_employee.html')

@admin_bp.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            employee.full_name = request.form.get('full_name')
            employee.phone = request.form.get('phone')
            employee.email = request.form.get('email')
            employee.position = request.form.get('position')
            employee.daily_wage = float(request.form.get('daily_wage'))
            employee.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
            employee.status = request.form.get('status')
            
            # Cập nhật tài khoản nếu có
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username:
                if employee.user:
                    # Kiểm tra username trùng (ngoại trừ user hiện tại)
                    existing = User.query.filter(User.username == username, User.id != employee.user.id).first()
                    if existing:
                        flash('Tên đăng nhập đã tồn tại!', 'danger')
                        return render_template('admin/edit_employee.html', employee=employee)
                    
                    employee.user.username = username
                    if password:
                        employee.user.set_password(password)
                else:
                    # Tạo user mới
                    existing = User.query.filter_by(username=username).first()
                    if existing:
                        flash('Tên đăng nhập đã tồn tại!', 'danger')
                        return render_template('admin/edit_employee.html', employee=employee)
                    
                    user = User(username=username, role='user', employee_id=employee.id)
                    if password:
                        user.set_password(password)
                    else:
                        user.set_password('123456')  # Mật khẩu mặc định
                    db.session.add(user)
            
            db.session.commit()
            flash('Cập nhật nhân viên thành công!', 'success')
            return redirect(url_for('admin.employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    return render_template('admin/edit_employee.html', employee=employee)

@admin_bp.route('/employees/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    try:
        # Xóa user liên quan
        if employee.user:
            db.session.delete(employee.user)
        # Xóa nhân viên (cascade sẽ xóa attendance)
        db.session.delete(employee)
        db.session.commit()
        flash('Xóa nhân viên thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi: {str(e)}', 'danger')
    return redirect(url_for('admin.employees'))

# ==================== QUẢN LÝ CHẤM CÔNG ====================

@admin_bp.route('/attendance')
@login_required
@admin_required
def attendance():
    employee_id = request.args.get('employee_id', type=int)
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    query = Attendance.query
    
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    
    if month:
        year, mon = map(int, month.split('-'))
        query = query.filter(
            db.extract('year', Attendance.work_date) == year,
            db.extract('month', Attendance.work_date) == mon
        )
    
    attendances = query.order_by(Attendance.work_date.desc()).all()
    employees = Employee.query.filter_by(status='active').all()
    
    return render_template('admin/attendance.html', 
                         attendances=attendances, 
                         employees=employees,
                         selected_employee=employee_id,
                         selected_month=month)

@admin_bp.route('/attendance/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_attendance():
    if request.method == 'POST':
        try:
            employee_id = int(request.form.get('employee_id'))
            work_date = datetime.strptime(request.form.get('work_date'), '%Y-%m-%d')
            work_hours = float(request.form.get('work_hours'))
            note = request.form.get('note', '')
            
            # Kiểm tra trùng lặp
            existing = Attendance.query.filter_by(
                employee_id=employee_id,
                work_date=work_date
            ).first()
            
            if existing:
                flash('Đã có chấm công cho nhân viên này trong ngày này!', 'danger')
                return redirect(url_for('admin.add_attendance'))
            
            attendance = Attendance(
                employee_id=employee_id,
                work_date=work_date,
                work_hours=work_hours,
                note=note
            )
            db.session.add(attendance)
            db.session.commit()
            flash('Thêm chấm công thành công!', 'success')
            return redirect(url_for('admin.attendance'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    employees = Employee.query.filter_by(status='active').all()
    return render_template('admin/add_attendance.html', employees=employees)

@admin_bp.route('/attendance/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_attendance(id):
    attendance = Attendance.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            employee_id = int(request.form.get('employee_id'))
            work_date = datetime.strptime(request.form.get('work_date'), '%Y-%m-%d')
            work_hours = float(request.form.get('work_hours'))
            note = request.form.get('note', '')
            
            # Kiểm tra trùng lặp (ngoại trừ bản ghi hiện tại)
            existing = Attendance.query.filter(
                Attendance.employee_id == employee_id,
                Attendance.work_date == work_date,
                Attendance.id != id
            ).first()
            
            if existing:
                flash('Đã có chấm công cho nhân viên này trong ngày này!', 'danger')
                return render_template('admin/edit_attendance.html', 
                                     attendance=attendance,
                                     employees=Employee.query.filter_by(status='active').all())
            
            attendance.employee_id = employee_id
            attendance.work_date = work_date
            attendance.work_hours = work_hours
            attendance.note = note
            
            db.session.commit()
            flash('Cập nhật chấm công thành công!', 'success')
            return redirect(url_for('admin.attendance'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi: {str(e)}', 'danger')
    
    employees = Employee.query.filter_by(status='active').all()
    return render_template('admin/edit_attendance.html', 
                         attendance=attendance, 
                         employees=employees)

@admin_bp.route('/attendance/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_attendance(id):
    attendance = Attendance.query.get_or_404(id)
    try:
        db.session.delete(attendance)
        db.session.commit()
        flash('Xóa chấm công thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi: {str(e)}', 'danger')
    return redirect(url_for('admin.attendance'))

# ==================== TÍNH LƯƠNG ====================

@admin_bp.route('/salary')
@login_required
@admin_required
def salary():
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    year, mon = map(int, month.split('-'))
    
    employees = Employee.query.filter_by(status='active').all()
    
    salary_data = []
    for emp in employees:
        total_work = emp.get_total_work_days(year, mon)
        total_salary = emp.calculate_salary(year, mon)
        salary_data.append({
            'employee': emp,
            'total_work': total_work,
            'daily_wage': emp.daily_wage,
            'total_salary': total_salary
        })
    
    return render_template('admin/salary.html', 
                         salary_data=salary_data, 
                         selected_month=month)
