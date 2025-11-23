# Hệ thống Quản lý Nhân sự - Chấm công - Tính lương

Ứng dụng web quản lý nhân sự với các tính năng đầy đủ: quản lý nhân viên, chấm công và tính lương tự động.

## 🚀 Công nghệ sử dụng

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **Template Engine**: Jinja2

## 📁 Cấu trúc project

```
project/
│ app.py              # File chính khởi động ứng dụng
│ config.py           # Cấu hình ứng dụng
│ requirements.txt    # Các thư viện cần thiết
│ init_db.py          # Script khởi tạo database
│
├── static/
│   └── css/
│       └── style.css # CSS tùy chỉnh
│
├── templates/
│   ├── base.html     # Template gốc
│   ├── login.html    # Trang đăng nhập
│   ├── admin/        # Templates cho admin
│   └── employee/     # Templates cho nhân viên
│
├── models/
│   └── __init__.py   # Database models (User, Employee, Attendance)
│
├── routes/
│   ├── auth.py       # Routes xác thực
│   ├── admin.py      # Routes cho admin
│   └── employee.py   # Routes cho nhân viên
│
└── database/
    └── hrms.db       # Database SQLite (tự động tạo)
```

## ⚙️ Cài đặt và chạy

### 1. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 2. Khởi tạo database và dữ liệu mẫu

```bash
python init_db.py
```

### 3. Chạy ứng dụng

```bash
flask run
```

hoặc

```bash
python app.py
```

### 4. Truy cập ứng dụng

Mở trình duyệt và truy cập: `http://127.0.0.1:5000`

## 👤 Tài khoản mặc định

### Admin
- **Username**: `admin`
- **Password**: `admin123`

### Nhân viên
1. **Username**: `nguyenvana` | **Password**: `123456`
2. **Username**: `tranthib` | **Password**: `123456`
3. **Username**: `levanc` | **Password**: `123456`

## 📋 Chức năng

### 🔐 Phân quyền
- **Admin**: Toàn quyền quản lý hệ thống
- **User (Nhân viên)**: Chỉ xem dữ liệu của mình

### 👨‍💼 Quản lý Nhân viên (Admin)
- ✅ Thêm nhân viên mới
- ✅ Sửa thông tin nhân viên
- ✅ Xóa nhân viên
- ✅ Danh sách nhân viên
- ✅ Tìm kiếm nhân viên (theo tên, SĐT, email)
- ✅ Tạo tài khoản đăng nhập cho nhân viên

### ⏰ Quản lý Chấm công (Admin)
- ✅ Thêm chấm công theo ngày
- ✅ Sửa chấm công
- ✅ Xóa chấm công
- ✅ Lọc theo nhân viên và tháng
- ✅ Ghi chú cho từng lần chấm công

### 💰 Tính lương (Admin)
- ✅ Tự động tính lương theo tháng
- ✅ Công thức: **Tổng lương = Tổng công × Lương 1 công**
- ✅ Xem bảng lương toàn bộ nhân viên
- ✅ Lọc theo tháng

### 👥 Chức năng Nhân viên
- ✅ Xem công theo ngày và tháng
- ✅ Xem tổng công trong tháng
- ✅ Xem lương tự động theo tháng
- ✅ Xem lại công và lương các tháng trước

## 🎨 Giao diện

- Responsive design với Bootstrap 5
- Icons từ Bootstrap Icons
- Giao diện hiện đại, dễ sử dụng
- Màu sắc chuyên nghiệp

## 📊 Database Models

### User
- Tài khoản đăng nhập
- Phân quyền (admin/user)
- Liên kết với nhân viên

### Employee
- Thông tin cá nhân
- Thông tin công việc
- Lương cơ bản

### Attendance
- Chấm công theo ngày
- Số công/giờ làm
- Ghi chú

## 🔒 Bảo mật

- Mật khẩu được hash bằng Werkzeug
- Flask-Login để quản lý session
- Phân quyền rõ ràng giữa admin và user
- Validation dữ liệu đầu vào

## 📝 Lưu ý

- Database SQLite được tạo tự động trong thư mục `database/`
- Để reset database, chạy lại `python init_db.py`
- Trong môi trường production, nên đổi `SECRET_KEY` trong `config.py`
- Có thể dễ dàng chuyển sang PostgreSQL/MySQL bằng cách đổi `SQLALCHEMY_DATABASE_URI`

## 🛠️ Phát triển thêm

Có thể mở rộng với các tính năng:
- Export bảng lương ra Excel/PDF
- Gửi email thông báo lương
- Quản lý phép nghỉ
- Báo cáo thống kê chi tiết
- Upload ảnh nhân viên
- Chấm công bằng QR code

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
1. Đã cài đặt đủ thư viện trong `requirements.txt`
2. Đã chạy `init_db.py` để tạo database
3. Port 5000 không bị chiếm bởi ứng dụng khác

---

**Made with ❤️ using Flask**
