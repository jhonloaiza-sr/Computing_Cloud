import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-me')
    # RDS (MySQL)
    DB_HOST = os.getenv('DB_HOST', 'consultorio-medico-db.cqjmquca03y1.us-east-1.rds.amazonaws.com')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Elzancudo980407')
    DB_NAME = os.getenv('DB_NAME', 'consultorio_db')
    # AWS
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', 'TU_AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', 'TU_AWS_SECRET_KEY')
    SES_SENDER_EMAIL = os.getenv('SES_SENDER_EMAIL', 'stivelo131@gmail.com')