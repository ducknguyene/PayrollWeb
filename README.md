# Web application used for managing employee's information and check-in/ check-out

## Technologies used

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **Template Engine**: Jinja2

## Project Structure

```
project/
│ app.py              # File to kickstart the app
│ config.py           # App configuration
│ requirements.txt    # Required libraries
│ init_db.py          # Script to initiate database
│
├── static/
│   └── css/
│       └── style.css 
│
├── templates/
│   ├── base.html     # Template 
│   ├── login.html    # Login page
│   ├── admin/        # Admin page
│   └── employee/     # Employee page
│
├── models/
│   └── __init__.py   # Database models (User, Employee, Attendance)
│
├── routes/
│   ├── auth.py       # Authentication routes
│   ├── admin.py      # Admin routes
│   └── employee.py   # Employee routes
│
└── database/
    └── hrms.db       # Database SQLite 
```

## Install and Run

### 1. Install libraries

```bash
pip install -r requirements.txt
```

### 2. Initiate database

```bash
python init_db.py
```

### 3. Run the app

```bash
flask run
```

or

```bash
python app.py
```

### 4. Access the web app

Open browser and type: `http://127.0.0.1:5000`

## Default account

### Admin
- **Username**: `admin`
- **Password**: `admin123`

### Employee
1. **Username**: `jdoe` | **Password**: `123456`
2. **Username**: `jmary` | **Password**: `123456`
3. **Username**: `jwong` | **Password**: `123456`

## Features

### Roles
- **Admin**: Full control of the system
- **Employee**: Only view his/her information

### Employee managing (Admin)
-  Add new employee
-  Modify employee's information
-  Delete employee
-  List employee
-  Employee search
-  Create new account

### Clock-in/ Clock-out managing (Admin)
-  Add clock-in/ clock-out
-  Modify clock-in/ clock-out
-  Delete clock-in/ clock-out
-  Sort by employee and date
-  Note for each clock-in/ clock-out

### Payroll (Admin)
-  Automatically calculated payroll monthly
-  Formula: **Salary = Total Work × Salary per work**
-  View all employees' salaries
-  Sort by month

### Emloyee features
-  View work by day and month
-  View total work of the month
-  View salary for the month
-  View previous works and salaries

## Interfaces

- Responsive design with Bootstrap 5
- Icons from Bootstrap Icons
- Modern, user-friendly interfaces

## Database Models

### User
- Log-in account
- Roles decentralization (admin/user)
- Employee linked

### Employee
- Personal information
- Work information
- Base salary

### Attendance
- Clock-in/ clock-out by date
- Work/ Work hour
- Notes

## Security

- Passwords are hashed by Werkzeug
- Session are managed by Flask
- Decentralization between admin and user
- Input data validation
