"""
Script để khởi tạo database và seed data mẫu
Chạy: python init_db.py
"""
from app import create_app
from models import db, User, Employee, Attendance
from datetime import datetime, timedelta

def init_database():
    app = create_app()
    
    with app.app_context():
        # Xóa tất cả dữ liệu cũ
        print("Đang xóa dữ liệu cũ...")
        db.drop_all()
        
        # Tạo lại các bảng
        print("Đang tạo các bảng...")
        db.create_all()
        
        # Tạo admin
        print("Đang tạo admin...")
        admin_user = User(username='admin', role='admin')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # Tạo nhân viên mẫu
        print("Đang tạo nhân viên mẫu...")
        
        # Nhân viên 1: Nguyễn Văn A
        emp1 = Employee(
            full_name='Nguyễn Văn A',
            phone='0901234567',
            email='nguyenvana@example.com',
            position='Nhân viên kinh doanh',
            daily_wage=300000,
            start_date=datetime(2024, 1, 15),
            status='active'
        )
        db.session.add(emp1)
        db.session.flush()
        
        user1 = User(username='nguyenvana', role='user', employee_id=emp1.id)
        user1.set_password('123456')
        db.session.add(user1)
        
        # Nhân viên 2: Trần Thị B
        emp2 = Employee(
            full_name='Trần Thị B',
            phone='0912345678',
            email='tranthib@example.com',
            position='Nhân viên kế toán',
            daily_wage=350000,
            start_date=datetime(2024, 2, 1),
            status='active'
        )
        db.session.add(emp2)
        db.session.flush()
        
        user2 = User(username='tranthib', role='user', employee_id=emp2.id)
        user2.set_password('123456')
        db.session.add(user2)
        
        # Nhân viên 3: Lê Văn C
        emp3 = Employee(
            full_name='Lê Văn C',
            phone='0923456789',
            email='levanc@example.com',
            position='Nhân viên kỹ thuật',
            daily_wage=400000,
            start_date=datetime(2024, 3, 1),
            status='active'
        )
        db.session.add(emp3)
        db.session.flush()
        
        user3 = User(username='levanc', role='user', employee_id=emp3.id)
        user3.set_password('123456')
        db.session.add(user3)
        
        db.session.commit()
        
        # Tạo dữ liệu chấm công mẫu (tháng hiện tại)
        print("Đang tạo dữ liệu chấm công mẫu...")
        today = datetime.now()
        
        # Chấm công cho nhân viên 1 (20 ngày trong tháng)
        for i in range(1, 21):
            try:
                work_date = datetime(today.year, today.month, i).date()
                attendance = Attendance(
                    employee_id=emp1.id,
                    work_date=work_date,
                    work_hours=1.0,
                    note='Đi làm đầy đủ'
                )
                db.session.add(attendance)
            except:
                pass
        
        # Chấm công cho nhân viên 2 (18 ngày trong tháng)
        for i in range(1, 19):
            try:
                work_date = datetime(today.year, today.month, i).date()
                attendance = Attendance(
                    employee_id=emp2.id,
                    work_date=work_date,
                    work_hours=1.0,
                    note='Đi làm đầy đủ'
                )
                db.session.add(attendance)
            except:
                pass
        
        # Chấm công cho nhân viên 3 (22 ngày trong tháng)
        for i in range(1, 23):
            try:
                work_date = datetime(today.year, today.month, i).date()
                attendance = Attendance(
                    employee_id=emp3.id,
                    work_date=work_date,
                    work_hours=1.0,
                    note='Đi làm đầy đủ'
                )
                db.session.add(attendance)
            except:
                pass
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ Khởi tạo database thành công!")
        print("="*50)
        print("\n📋 THÔNG TIN TÀI KHOẢN:")
        print("\n👨‍💼 Admin:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n👥 Nhân viên:")
        print("   1. Username: nguyenvana | Password: 123456")
        print("   2. Username: tranthib   | Password: 123456")
        print("   3. Username: levanc     | Password: 123456")
        print("\n" + "="*50)
        print("🚀 Chạy lệnh: flask run")
        print("🌐 Truy cập: http://127.0.0.1:5000")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_database()
