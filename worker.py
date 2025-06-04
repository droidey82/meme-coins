import requests
import smtplib
import time
import os

DEXSCREENER_API_URL = os.getenv("DEXSCREENER_API_URL", "https://api.dexscreener.com/latest/dex/pairs")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "300"))
MAX_AGE_MINUTES = int(os.getenv("MAX_PAIR_AGE", "15"))
MIN_VOLUME = float(os.getenv("MIN_VOLUME", "15000"))
MIN_LIQUIDITY = float(os.getenv("MIN_LIQUIDITY", "10000"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ALERT_RECEIVER_EMAIL = os.getenv("ALERT_RECEIVER_EMAIL")

def send_email_alert(subject, body):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            message = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(EMAIL_USER, ALERT_RECEIVER_EMAIL, message)
            print(f"📧 Alert sent: {subject}")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def scan_dex():
    try:
        response = requests.get(DEXSCREENER_API_URL)
        response.raise_for_status()
        return response.json().get('pairs', [])
    except Exception as e:
        print(f"❌ Dexscreener API error: {e}")
        return []

def is_new_pair(pair):
    created_ts = pair.get("pairCreatedAt") or pair.get("createdAtTimestamp")
    if not created_ts:
        return False
    current_ts = int(time.time() * 1000)
    age_minutes = (current_ts - int(created_ts)) / 60000
    return age_minutes <= MAX_AGE_MINUTES

def filter_new_pairs(pairs):
    found = 0
    for pair in pairs:
        base = pair.get("baseToken", {})
        name = base.get("name", "")
        symbol = base.get("symbol", "")
        volume = float(pair.get("volume", {}).get("h24", 0))
        liquidity = float(pair.get("liquidity", {}).get("usd", 0))

        if is_new_pair(pair) and volume >= MIN_VOLUME and liquidity >= MIN_LIQUIDITY:
            subject = f"🚨 New Token: {symbol.upper()}"
            body = (
                f"Name: {name} ({symbol})\n"
                f"Price: ${pair.get('priceUsd')}\n"
                f"Volume (24h): ${volume}\n"
                f"Liquidity: ${liquidity}\n"
                f"DEX: {pair.get('dexId')}\n"
                f"URL: {pair.get('url')}\n"
                f"Created: {pair.get('pairCreatedAt') or pair.get('createdAtTimestamp')}"
            )
            send_email_alert(subject, body)
            found += 1
    print(f"🆕 New tokens found: {found}")

def main():
    print("🔍 New Coin Scanner Started")
    print(f"Scan Interval: {SCAN_INTERVAL}s | Max Age: {MAX_AGE_MINUTES}m | Min Vol: {MIN_VOLUME} | Min Liq: {MIN_LIQUIDITY}")

    while True:
        try:
            print("🔄 Scanning Dexscreener...")
            pairs = scan_dex()
            filter_new_pairs(pairs)
            print(f"💤 Sleeping for {SCAN_INTERVAL} seconds...\n")
            time.sleep(SCAN_INTERVAL)
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()