import os

# Đường dẫn tuyệt đối tới thư mục project
basedir = os.path.abspath(os.path.dirname(__file__))

# Tạo thư mục database nếu chưa tồn tại
database_dir = os.path.join(basedir, 'database')
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_dir, 'hrms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
