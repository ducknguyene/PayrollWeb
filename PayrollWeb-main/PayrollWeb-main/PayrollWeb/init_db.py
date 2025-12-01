"""
Script to initiate database và seed data 
Run: python init_db.py
"""
from app import create_app
from models import db, User, Employee, Attendance
from datetime import datetime, timedelta

def init_database():
    app = create_app()
    
    with app.app_context():
        # Delete old data
        print("Deleting old data...")
        db.drop_all()
        
        # Recreate tables
        print("Recreating tables...")
        db.create_all()
        
        # Initiate admin
        print("Initiating admin...")
        admin_user = User(username='admin', role='admin')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # Initiate example employee
        print("Initiating employee...")
        
        # Employee 1: John Doe
        emp1 = Employee(
            full_name='John Doe',
            phone='0901234567',
            email='jdoe@example.com',
            position='Sales person',
            daily_wage=300000,
            start_date=datetime(2024, 1, 15),
            status='active'
        )
        db.session.add(emp1)
        db.session.flush()
        
        user1 = User(username='jdoe', role='user', employee_id=emp1.id)
        user1.set_password('123456')
        db.session.add(user1)
        
        # Employee 2: Jessica Mary
        emp2 = Employee(
            full_name='Jessica Mary',
            phone='0912345678',
            email='jmary@example.com',
            position='Accountant',
            daily_wage=350000,
            start_date=datetime(2024, 2, 1),
            status='active'
        )
        db.session.add(emp2)
        db.session.flush()
        
        user2 = User(username='jmary', role='user', employee_id=emp2.id)
        user2.set_password('123456')
        db.session.add(user2)
        
        # Employee 3: Jack Wong
        emp3 = Employee(
            full_name='Jack Wong',
            phone='0923456789',
            email='jwong@example.com',
            position='Technician',
            daily_wage=400000,
            start_date=datetime(2024, 3, 1),
            status='active'
        )
        db.session.add(emp3)
        db.session.flush()
        
        user3 = User(username='jwong', role='user', employee_id=emp3.id)
        user3.set_password('123456')
        db.session.add(user3)
        
        db.session.commit()
        
        # Initiate sample work hour data (current month)
        print("Initiating sample data...")
        today = datetime.now()
        
        # Work hour for employee 1 (20 days per month)
        for i in range(1, 21):
            try:
                work_date = datetime(today.year, today.month, i).date()
                attendance = Attendance(
                    employee_id=emp1.id,
                    work_date=work_date,
                    work_hours=1.0,
                    note='Sufficient work hour'
                )
                db.session.add(attendance)
            except:
                pass
        
        # Work hour for employee 2 (18 days per month)
        for i in range(1, 19):
            try:
                work_date = datetime(today.year, today.month, i).date()
                attendance = Attendance(
                    employee_id=emp2.id,
                    work_date=work_date,
                    work_hours=1.0,
                    note='Sufficient work hour'
                )
                db.session.add(attendance)
            except:
                pass
        
        # Work hour for employee 3 (22 days per month)
        for i in range(1, 23):
            try:
                work_date = datetime(today.year, today.month, i).date()
                attendance = Attendance(
                    employee_id=emp3.id,
                    work_date=work_date,
                    work_hours=1.0,
                    note='Sufficient work hour'
                )
                db.session.add(attendance)
            except:
                pass
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("Initiate database successfully!")
        print("="*50)
        print("\n ACCOUNT INFORMATION:")
        print("\n Admin:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n Employee:")
        print("   1. Username: jdoe | Password: 123456")
        print("   2. Username: jmary   | Password: 123456")
        print("   3. Username: jwong     | Password: 123456")
        print("\n" + "="*50)
        print("Run script: flask run")
        print("Access: http://127.0.0.1:5000")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_database()
