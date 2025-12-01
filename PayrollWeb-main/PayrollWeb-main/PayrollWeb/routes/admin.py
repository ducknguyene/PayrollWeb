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
            flash('You do not have access!', 'danger')
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

# ==================== Employee Management ====================

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
            # Initiate new employee
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
            db.session.flush()  # Retrieve employee.id
            
            # Create log-in account
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username and password:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    flash('Username existed!', 'danger')
                    db.session.rollback()
                    return render_template('admin/add_employee.html')
                
                user = User(username=username, role='user', employee_id=employee.id)
                user.set_password(password)
                db.session.add(user)
            
            db.session.commit()
            flash('Employee added successfully!', 'success')
            return redirect(url_for('admin.employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
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
            
            # Update account if needded
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username:
                if employee.user:
                    # Check for duplicated username (except current user)
                    existing = User.query.filter(User.username == username, User.id != employee.user.id).first()
                    if existing:
                        flash('Username existed!', 'danger')
                        return render_template('admin/edit_employee.html', employee=employee)
                    
                    employee.user.username = username
                    if password:
                        employee.user.set_password(password)
                else:
                    # Create new user
                    existing = User.query.filter_by(username=username).first()
                    if existing:
                        flash('Username exisited!', 'danger')
                        return render_template('admin/edit_employee.html', employee=employee)
                    
                    user = User(username=username, role='user', employee_id=employee.id)
                    if password:
                        user.set_password(password)
                    else:
                        user.set_password('123456')  # Default password
                    db.session.add(user)
            
            db.session.commit()
            flash('Update successfully!', 'success')
            return redirect(url_for('admin.employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('admin/edit_employee.html', employee=employee)

@admin_bp.route('/employees/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    try:
        # Delete related user
        if employee.user:
            db.session.delete(employee.user)
        # Delete employee (cascade will delete attendance)
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin.employees'))

# ==================== Work hour management ====================

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
            
            # Duplication check
            existing = Attendance.query.filter_by(
                employee_id=employee_id,
                work_date=work_date
            ).first()
            
            if existing:
                flash('There is already check-in for this day!', 'danger')
                return redirect(url_for('admin.add_attendance'))
            
            attendance = Attendance(
                employee_id=employee_id,
                work_date=work_date,
                work_hours=work_hours,
                note=note
            )
            db.session.add(attendance)
            db.session.commit()
            flash('Check-in added successfully!', 'success')
            return redirect(url_for('admin.attendance'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
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
            
            # Duplication check (except for current attendance)
            existing = Attendance.query.filter(
                Attendance.employee_id == employee_id,
                Attendance.work_date == work_date,
                Attendance.id != id
            ).first()
            
            if existing:
                flash('Attendace already existed for this day!', 'danger')
                return render_template('admin/edit_attendance.html', 
                                     attendance=attendance,
                                     employees=Employee.query.filter_by(status='active').all())
            
            attendance.employee_id = employee_id
            attendance.work_date = work_date
            attendance.work_hours = work_hours
            attendance.note = note
            
            db.session.commit()
            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('admin.attendance'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
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
        flash('Attendance deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin.attendance'))

# ==================== SALARY ====================

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
