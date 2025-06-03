from flask import Flask, jsonify
from alert import send_email_alert
from scanner import run_signal_scan

app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({"status": "alive"})

@app.route('/status')
def status():
    return jsonify({"status": "running", "module": "memecoin-bot"})

@app.route('/test-alert')
def test_alert():
    send_email_alert("TESTCOIN", "ETH", "0.0000421", "0.0000542", "0.0000687", "0.0000385")
    return jsonify({"status": "Email sent to droideypop@gmail.com"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)