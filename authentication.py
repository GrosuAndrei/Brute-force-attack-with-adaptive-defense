from storage import get_user, hash_password, log_attempt
from defense import check_defense, apply_delay, apply_captcha, check_geoblock
from config import ALPHABET, BRUTEFORCE_MAX_LENGTH
import itertools

def handle_defense(ip, use_defense):
    if not use_defense:
        return True

    if check_geoblock(ip):
        print("Acces blocat (geoblocking)")
        return False

    status = check_defense(ip)

    if status == "BLOCKED":
        print("IP blocat!")
        return False

    elif status == "DELAY":
        apply_delay()

    elif status == "CAPTCHA":
        apply_captcha()

    return True


def login_classic(ip, use_defense):
    username = input("Username: ")
    user = get_user(username)

    if not user:
        print("User inexistent")
        return

    while True:
        if not handle_defense(ip, use_defense):
            return

        password = input("Password: ")
        hashed = hash_password(password)

        if hashed == user[2]:
            print("Login reusit!")
            log_attempt(ip, username, "success", password)
            return
        else:
            print("Parola gresita")
            log_attempt(ip, username, "fail", password)


def brute_force(ip, use_defense, username):
    user = get_user(username)
    if not user:
        print("User inexistent")
        return

    target_hash = user[2]

    for length in range(1, BRUTEFORCE_MAX_LENGTH + 1):
        for attempt in itertools.product(ALPHABET, repeat=length):
            
            if not handle_defense(ip, use_defense):
                return

            password = ''.join(attempt)
            hashed = hash_password(password)

            if hashed == target_hash:
                print(f"Parola gasita: {password}")
                log_attempt(ip, username, "success", password)
                return
            else:
                log_attempt(ip, username, "fail", password)


def wordlist_attack(ip, use_defense, username):
    user = get_user(username)
    if not user:
        print("User inexistent")
        return

    target_hash = user[2]

    with open("passwords.txt") as f:
        for line in f:
            
            if not handle_defense(ip, use_defense):
                return

            password = line.strip()
            hashed = hash_password(password)

            if hashed == target_hash:
                print(f"Parola gasita: {password}")
                log_attempt(ip, username, "success", password)
                return
            else:
                log_attempt(ip, username, "fail", password)