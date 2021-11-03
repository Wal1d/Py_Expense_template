from PyInquirer import prompt
import csv

user_questions = [
    {
        "type":"input",
        "name":"name",
        "message":"New User - User's name:",
    },
]

def add_user():
    infos = prompt(user_questions)

    with open('users.csv', 'a') as f:
        w = csv.DictWriter(f, infos.keys())
        w.writerow(infos)
    print("New user Added !")
    print(load_users())
    return True

USERS = None
def load_users():
    global USERS
    if USERS is not None:
        return USERS
    with open('users.csv') as csvfile:
        uload = csv.reader(csvfile)
        USERS = [row[0] for row in uload]
        return USERS
