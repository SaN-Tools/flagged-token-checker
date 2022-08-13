import os
import time
import httpx
from colorama import Fore
import threading

_flagged = []
_unflagged = []
_invalid = []
_locked = []

counter = 0

flagged = 0
unflagged = 0
invalid = 0
locked = 0
errors = 0

def titleUpdater():
    os.system(f"title [ Unflagged: {unflagged} , Flagged: {flagged} , Invalid: {invalid} , Locked: {locked}, Errors: {errors} ]")

class Checker():
    def _init__(self, token):
        self.token = token

    def check(self):
        global _flagged
        global _unflagged
        global _invalid
        global _locked

        global flagged
        global unflagged
        global invalid
        global locked
        global errors
        headers = {
            "Authortization": self.token
        }

        req = httpx.get("https://discord.com/api/v9/users/@me", headers=headers)

        if req.status_code == 200:
            rj = req.json()
            username = rj["username"]
            flags = rj["flags"]
            publicFlags = rj["public_flags"]

            if flags == "1048576" or publicFlags == "1048576":
                flagged += 1
                _flagged.append(self.token)
                print(f"{Fore.MAGENTA}[FLAGGED] ({self.token}) - ({username}) is marked as spammer [{flagged}]{Fore.WHITE}")
                return
            else:
                unflagged += 1
                _unflagged.append(self.token)
                print(f"{Fore.GREEN}[UNFLAGGED] ({self.token}) - ({username}) is not marked as spammer [{unflagged}]{Fore.WHITE}")
                return
        elif req.status_code == 401:
            invalid += 1
            _invalid.append(self.token)
            print(f"{Fore.RED}[INVALID] ({self.token})  [{invalid}]{Fore.WHITE}")
            return
        elif req.status_code == 403:
            locked += 1
            _locked.append(self.token)
            print(f"{Fore.RED}[LOCKED] ({self.token})  [{locked}]{Fore.WHITE}")
            return
        else:
            print(f"{Fore.RED}[ERROR] ({self.token}) - [{errors}] - {Fore.WHITE}{req.text}")
            return
            
def main():
    try:
        threads = int(input("[>] How many threads to use (0 = maximum): "))
    except:
        print("[ERROR] Please enter a number\n Press enter to return...\n")
        input()
        main()

    tokens = []
    with open("data/tokens.txt") as f:
        for line in f:
            tokens.append(line.replace("\n",""))
    if threads == 0:
        threads = len(tokens)
    elif threads > (len(tokens)):
        threads = len(tokens)

    for token in tokens:
        while threading.active_count > threads:
            time.sleep(0.01)
        checker = Checker(token)
        t = threading.Thread(checker.check)
        t.start()

    while counter > len(tokens):
        time.sleep(0.1)
    
    c = input("[SUCCESS] Threads finished do you want to save tokens (y/n): ")
    if c == "y":
        with open("data/flagged.txt", "w") as f:
            for x in _flagged:
                f.write(f"{x}\n")

        with open("data/unflagged.txt", "w") as f:
            for x in _unflagged:
                f.write(f"{x}\n")

        with open("data/invalid.txt", "w") as f:
            for x in _invalid:
                f.write(f"{x}\n")
        
        with open("data/locked.txt", "w") as f:
            for x in _locked:
                f.write(f"{x}\n")
    else:
        pass

    print("Done.")
    time.sleep(2)
    input("Press enter to exit...\n")
main()
