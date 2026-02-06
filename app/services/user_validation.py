from app.extensions import db
from flask import make_response,redirect
from flask_jwt_extended import create_access_token
from app.models.user import User
import re
import os
import csv
import hashlib
import smtplib
import requests
from email.mime.text import MIMEText

def fetch_joke():
    response = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"}
    )
    data = response.json()
    return data["joke"]



def encrypt_password(password):
    password=hashlib.md5(password.encode()).hexdigest()
    return password

def send_mail(data):
    # SMTP Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')  
    USERNAME = os.getenv('GMAIL')
    PASSWORD = os.getenv('PASSWORD')
    # Email Details
    receiver_email = data["email"]
    sender_email=os.getenv('GMAIL')
    subject = "User registered Successfully"
    body = "Your account has been created.\nThank you for registration\n\n\nUse your email and password to login"
    # Create the email
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure connection
        server.login(USERNAME, PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully!")

def csv_convert(data):
    path = 'app/user_hobby'
    name = data["email"]+ '.csv'
    csvFileName = os.path.join(path,name)

    with open(csvFileName, 'w') as csv_file:
        csvWriter = csv.writer(csv_file, delimiter = ',')
        csvWriter.writerow(data["hobbies"])
    file_path = os.path.join(csvFileName)
    return file_path

def insert_data(data):
    print(data)
    encrypted_pass=encrypt_password(data["password"])
    # hobby_string=",".join(data["hobbies"])
    hobby_csv=csv_convert(data)
    user= User(
        first_name = data["first_name"],
        last_name = data["last_name"],
        email = data["email"],
        password = encrypted_pass,
        address = data["address"],
        hobbies = hobby_csv,
        gender = data["gender"]
    )
    db.session.add(user)
    db.session.commit()
    send_mail(data)

class UserValidation:

    @staticmethod
    def register_validation(data):

        if not all([
            data["first_name"], data["last_name"], data["email"],
            data["password"], data["confirm"], data["address"],
            data["gender"], data["terms"]
        ]):
            return None, "All fields required", 400

        if User.query.filter_by(email=data["email"]).first():
            return None, "Email already exists", 400

        if len(data["first_name"]) > 30 or len(data["last_name"]) > 30:
            return None, "Name must be < 30 chars", 400

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, data["email"]):
            return None, "Invalid Email", 400

        if len(data["password"]) < 6 or len(data["password"]) > 12:
            return None, "Password must be 6-12 chars", 400

        if data["password"] != data["confirm"]:
            return None, "Passwords mismatch", 400

        if len(data["address"].split()) <= 15:
            return None, "Address must contain >15 words", 400

        if len(data["hobbies"]) == 0:
            return None, "Select at least one hobby", 400

        insert_data(data)

        return "User created", None, 201


    @staticmethod
    def login_validation(data):
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return None, "User not found", 404
        if user.password != encrypt_password(data["password"]):
            return None, "Wrong password", 400
        token = create_access_token(identity=str(user.registration_id))
        return {"access_token": token}, None, 200

# if __name__=="__main__":
