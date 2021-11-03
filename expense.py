from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
from user import load_users
import regex
import csv
import json


class IntergerValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[\d]+$', document.text)
        if not ok:
            raise ValidationError(message = 'Please enter a valid number', cursor_position = len(document.text))



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
        'validate': IntergerValidator

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
    {
        "type":"list",
        "name":"main_options",
        "message":"Expense Tracker v0.1",
        "choices": ["Split Expenses Properly", "Main menu"]
    }
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

    if (infos['main_options']) == "Split Expenses Properly":
        split_expenses(infos)

    print("Expense Added !")
    append_to_json(infos, 'expense_report.csv')

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
    return owned






def split_expenses(expenses):
    split_questions = []
    for i in expenses['allspenders']:
        split_questions.append({
        "type":"input",
        "name":i,
        "message":"Splitting - Pourcentage for {}: (pourcentage left : 100%)".format(i),
        'validate': IntergerValidator
    })
    
    infos = prompt(split_questions)
    
    newPrices = {}
    for userO in expenses['allspenders']:
        newPrices[userO] = (int(infos[userO]) * int(expenses['amount'])) / 100

    expenses['allspenders'] = newPrices
    print (newPrices)
    return expenses
