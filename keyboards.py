from telebot import types
from sql import *
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Помощь")
    btn2 = types.KeyboardButton("Обновить группу")
    btn3 = types.KeyboardButton("Распределить деньги")
    btn4 = types.KeyboardButton("Долги")
    btn5 = types.KeyboardButton("Должники")
    btn6 = types.KeyboardButton("Выплатить долг")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def return_to_main_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1)
    return markup

def update_group_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать группу")
    btn2 = types.KeyboardButton("Добавить чела в группу")
    btn3 = types.KeyboardButton("Удалить чела из группы")
    btn4 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def create_deal_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Между группой")
    btn2 = types.KeyboardButton("Назначить пользователю")
    btn3 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1, btn2, btn3)
    return markup

def user_list_kb(word):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users = users_query()
    for user in users:
            btn = types.KeyboardButton(word+str(user))
            markup.add(btn)
    btn1 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1)
    return markup

def group_list_or_not_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Список групп")
    btn2 = types.KeyboardButton("Знаю название группы")
    btn3 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1, btn2, btn3)
    return markup

def group_list_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вернуться к главному меню")
    btn2 = types.KeyboardButton("Назначить долг группе")
    markup.add(btn1, btn2)
    return markup

def groups_kb(message, word):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    groups = groups_with_user_query(message)
    for group in groups:
        btn = types.KeyboardButton(word+str(group))
        markup.add(btn)
    btn1 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1)
    return markup

def add_user_to_group_kb(message, word, word2):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users = users_not_in_group_query(" ".join(word2.split(" ")[2:]))
    for user in users:
            btn = types.KeyboardButton(word+str(user)+word2)
            markup.add(btn)
    btn1 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1)
    return markup

def delete_user_from_group_kb(message, word, word2):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users = users_in_group_query(" ".join(word2.split(" ")[2:]))
    for user in users:
            btn = types.KeyboardButton(word+str(user)+word2)
            markup.add(btn)
    btn1 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1)
    return markup

def deals_kb(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    deals= name_creditors_list_query(message.from_user.username)
    for deal in deals:
        btn = types.KeyboardButton(deal)
        markup.add(btn)
    btn1 = types.KeyboardButton("Вернуться к главному меню")
    markup.add(btn1)
    return markup