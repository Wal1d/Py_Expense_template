from PyInquirer import prompt
import csv

from user import load_users

def get_user_options(answers):
    options = load_users()
    return options

def get_users_choices(answers):
    tmp = get_user_options(answers)
    options = [{ 'name' : x} for x in tmp]
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
        'name': 'All spenders',
        "choices": get_users_choices,
    },

]



def new_expense(*args):
    infos = prompt(expense_questions)
    # Writing the informations on external file might be a good idea ¯\_(ツ)_/¯
    print("Expense Added !")
    with open('expense_report.csv', 'a') as f:
        w = csv.DictWriter(f, infos.keys())
        w.writerow(infos)
    return True