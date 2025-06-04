import time
from scanner import run_signal_scan

def run_loop():
    while True:
        print("Running Dexscreener scan...")
        run_signal_scan()
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    run_loop()