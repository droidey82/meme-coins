from flask import Flask, jsonify
from alert import send_email_alert

app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({"status": "alive"})

@app.route('/test-alert')
def test_alert():
    send_email_alert("TESTCOIN", "ETH", "0.0000421", "0.0000542", "0.0000687", "0.0000385")
    return jsonify({"status": "Email sent to droideypop@gmail.com"})