import os
import smtplib
from email.mime.text import MIMEText

def send_email_alert(token, chain, entry, tp1, tp2, sl):
    sender = os.getenv("EMAIL_USER")
    recipient = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASS")

    subject = f"🚀 MEMECOIN SIGNAL: ${token}"
    body = f'''
🔥 Entry Signal Detected for ${token}
Chain: {chain}
📍 Entry: {entry}
🎯 TP1: {tp1}
🎯 TP2: {tp2}
🛑 SL: {sl}

Signal triggered by volume spike + demand zone bounce.
    '''
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("Email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")