from storage import init_db
from authentication import login_classic, brute_force, wordlist_attack
from config import DEFAULT_ATTACKER_IP

def main():
    init_db()

    while True:
        print("\n**** MENIU ****")
        print("1. Login (cu aparare)")
        print("2. Login (fara aparare)")
        print("3. Brute force (cu aparare)")
        print("4. Brute force (fara aparare)")
        print("5. Wordlist (cu aparare)")
        print("6. Wordlist (fara aparare)")
        print("7. Reset logs")
        print("0. Exit")

        choice = input("Alege: ")

        ip = DEFAULT_ATTACKER_IP

        if choice == "1":
            login_classic(ip, True)

        elif choice == "2":
            login_classic(ip, False)

        elif choice == "3":
            user = input("Username target: ")
            brute_force(ip, True, user)

        elif choice == "4":
            user = input("Username target: ")
            brute_force(ip, False, user)

        elif choice == "5":
            user = input("Username target: ")
            wordlist_attack(ip, True, user)

        elif choice == "6":
            user = input("Username target: ")
            wordlist_attack(ip, False, user)

        elif choice == "7":
            from storage import clear_logs
            from defense import reset_defense_state
            clear_logs()
            reset_defense_state()
            print("Logs resetate!")
            
        elif choice == "0":
            break

if __name__ == "__main__":
    main()