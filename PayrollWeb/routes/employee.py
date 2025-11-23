from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Attendance
from datetime import datetime

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return render_template('employee/dashboard.html')
    
    if not current_user.employee:
        return "Tài khoản chưa được liên kết với nhân viên!"
    
    # Lấy tháng hiện tại
    now = datetime.now()
    total_work = current_user.employee.get_total_work_days(now.year, now.month)
    
    return render_template('employee/dashboard.html', 
                         employee=current_user.employee,
                         total_work=total_work)

@employee_bp.route('/attendance')
@login_required
def attendance():
    if not current_user.employee:
        return "Tài khoản chưa được liên kết với nhân viên!"
    
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    year, mon = map(int, month.split('-'))
    
    attendances = Attendance.query.filter(
        Attendance.employee_id == current_user.employee.id,
        db.extract('year', Attendance.work_date) == year,
        db.extract('month', Attendance.work_date) == mon
    ).order_by(Attendance.work_date.desc()).all()
    
    total_work = sum(a.work_hours for a in attendances)
    
    return render_template('employee/attendance.html', 
                         attendances=attendances,
                         selected_month=month,
                         total_work=total_work)

@employee_bp.route('/salary')
@login_required
def salary():
    if not current_user.employee:
        return "Tài khoản chưa được liên kết với nhân viên!"
    
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    year, mon = map(int, month.split('-'))
    
    employee = current_user.employee
    total_work = employee.get_total_work_days(year, mon)
    total_salary = employee.calculate_salary(year, mon)
    
    return render_template('employee/salary.html',
                         employee=employee,
                         selected_month=month,
                         total_work=total_work,
                         total_salary=total_salary)
