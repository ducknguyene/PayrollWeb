from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    
    employee = db.relationship('Employee', back_populates='user', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'


class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    position = db.Column(db.String(100))
    daily_wage = db.Column(db.Float, nullable=False)  # Salary of 1 day or 1 hour
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='active')  # 'active' or 'inactive'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='employee', uselist=False)
    attendances = db.relationship('Attendance', back_populates='employee', cascade='all, delete-orphan')
    
    def get_total_work_days(self, year, month):
        """Calculate total work hour in a month"""
        total = 0
        for attendance in self.attendances:
            if attendance.work_date.year == year and attendance.work_date.month == month:
                total += attendance.work_hours
        return total
    
    def calculate_salary(self, year, month):
        """Calculate salary"""
        total_work = self.get_total_work_days(year, month)
        return total_work * self.daily_wage


class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    work_date = db.Column(db.Date, nullable=False)
    work_hours = db.Column(db.Float, nullable=False)  # Work hour / hour
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', back_populates='attendances')
    
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'work_date', name='unique_employee_date'),
    )
