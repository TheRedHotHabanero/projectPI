import hashlib
import json

passwords = {"MIPT":"mfti4321"}

for login, password in passwords.items():
    passwords[login] = hashlib.sha3_256(passwords[login].encode()).hexdigest()

with open("passwords.json","w+") as file:
    json.dump(passwords, file)