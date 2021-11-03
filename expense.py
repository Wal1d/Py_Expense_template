from PyInquirer import prompt
import csv
import json

from user import load_users

def get_user_options(answers):
    options = load_users()
    return options

def get_users_choices(answers):
    tmp = get_user_options(answers)
    print(answers)
    options = [{ 'name' : x, 'checked': True} if x == answers['spender'] else { 'name' : x} for x in tmp]
    return options


expense_questions = [
    {
        "type":"input",
        "name":"amount",
        "message":"New Expense - Amount: ",
    },
    {
        "type":"input",
        "name":"label",
        "message":"New Expense - Label: ",
    },
    {
        "type":"list",
        "name":"spender",
        "message":"New Expense - Spender: ",
        "choices": get_user_options,
    },
    {
        'type': 'confirm',
        'message': 'Do you want to split amount amoung all spenders?',
        'name': 'Split',
        'default': False,
    },
    {
        'type': 'checkbox',
        'qmark': '💸',
        'message': 'Select all the spenders',
        'name': 'allspenders',
        "choices": get_users_choices,
    },

]


def append_to_json(_dict, path): 
    with open(path, 'ab+') as f:
        f.seek(0,2)                                 
        if f.tell() == 0 :                        
            f.write(json.dumps([_dict]).encode()) 
        else :
            f.seek(-1,2)           
            f.truncate()                          
            f.write(' , '.encode())               
            f.write(json.dumps(_dict).encode())   
            f.write(']'.encode())                  


def new_expense(*args):
    infos = prompt(expense_questions)
    # Writing the informations on external file might be a good idea ¯\_(ツ)_/¯
    print(infos['allspenders'])
    amountOwned = [{}]
    print("Expense Added !")
    append_to_json(infos, 'expense_report.csv')
    # with open('expense_report.csv', 'a') as f:
    #     # w = csv.DictWriter(f, infos.keys())
    #     # w.writerow(infos)
    #     # feeds = json.load(f)
    #     # json.dump(infos, feeds)
    #     f.write(json.dumps(infos))
    #     f.write(",")
    #     f.close()


    return True

def showStatus(*args):
    with open('expense_report.csv') as f:
        status = json.load(f)
        users = load_users()
        # owned = dict.fromkeys(users, {}) # Created mutable objects 
        owned = {key: {} for key in users}
        # print(owned)

        for elem in status:
            dst = elem['spender']
            amount = int(elem['amount']) / (len(elem['allspenders']) - 1)
            usersOwed = elem['allspenders']
            for userO in usersOwed:
                if userO != dst:
                    owned[userO][dst] = amount + (owned[userO][dst] if dst in owned[userO] else 0)
           
        for src, dsts in owned.items():
            print(src, ' owes ', end=' ')
            for dst, amount in dsts.items():
                print (amount, ' to ', dst, end=', ')
            if not dsts.keys():
                print('nothing', end=' ')
            print()
    return True