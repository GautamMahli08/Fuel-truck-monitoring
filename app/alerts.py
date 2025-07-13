# app/alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")   # e.g., smtp.gmail.com
SMTP_PORT = int(os.getenv("SMTP_PORT"))  # e.g., 587
SMTP_USER = os.getenv("SMTP_USER")       # Your Gmail address
SMTP_PASS = os.getenv("SMTP_PASS")       # Gmail App Password
ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT")  # Who gets alerts

def send_email_alert(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_RECIPIENT
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
