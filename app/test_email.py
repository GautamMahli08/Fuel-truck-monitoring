from app.alerts import send_email_alert

if __name__ == "__main__":
    subject = "🚨 Test Alert"
    body = "This is a test email from your IoT fuel truck monitoring system."

    try:
        send_email_alert(subject, body)
        print("✅ Test email sent! Check your inbox.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
