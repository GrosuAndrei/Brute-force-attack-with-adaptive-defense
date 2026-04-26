import time
import random
import string
from storage import get_attempts_after_last_success
from config import THRESHOLDS, IP_COUNTRY, BLOCKED_COUNTRIES

blocked_ips = {}

def check_geoblock(ip):
    country = IP_COUNTRY.get(ip, "UNKNOWN")
    if country in BLOCKED_COUNTRIES:
        return True
    return False

def reset_defense_state():
    blocked_ips.clear()

def check_defense(ip):
    now = time.time()

    if ip in blocked_ips:
        if now < blocked_ips[ip]:
            return "BLOCKED"
        else:
            del blocked_ips[ip]

    attempts = get_attempts_after_last_success(ip, THRESHOLDS["window_minutes"] * 60)
    fails = attempts.count("fail")

    if fails >= THRESHOLDS["block_after"]:
        blocked_ips[ip] = now + THRESHOLDS["block_duration"]
        return "BLOCKED"

    elif fails >= THRESHOLDS["captcha_after"]:
        return "CAPTCHA"

    elif fails >= THRESHOLDS["delay_after"]:
        return "DELAY"

    return "OK"

def apply_delay():
    print("Delay activ...")
    time.sleep(THRESHOLDS["delay_seconds"])

def apply_captcha():

    while True:
        captcha = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        print(f"\n CAPTCHA necesar: {captcha}")

        user_input = input("Introdu captcha: ").strip()

        if user_input == captcha:
            return True
        else:
            print("CAPTCHA gresit! Se genereaza unul nou.")
            
