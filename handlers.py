from sql import *
from main import *
from telebot import types
from keyboards import *




def add_user(message):
    add_user_query(message)
    msg = bot.send_message(message.chat.id, 'Кайф, теперь можем начинать', reply_markup=main_keyboard())
    bot.register_next_step_handler(msg, func)


def help():
    return ('У меня есть 4 функции \n  \n Обновить группу \n эта функция'
            'позволит добавить или удалить пользователя из существующую группы или '
            'создать новую группу \n \n '
            'Распределить деньги\n' 'эта функция поможет распределить деньги '
            'поровну между всеми членами группы, или ты можешь назначить выплату'
            'определенным людям\n \n '
            'Долги\n'
            'Получишь список с долгами и контактами тех, кому должен\n \n '
            'Должники\n'
            'Получишь список должников и их контактов')


def create_group(message):
    if message.text == 'Вернуться к главному меню':
        msg = bot.send_message(message.chat.id, "Оке, возвращаемся, группа не создана", reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)
    else:
        group_name = message.text
        add_group_query(message, group_name)
        msg = bot.send_message(message.chat.id, 'Группа создана', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)


def insert_into_group(message):
    if message.text == 'Вернуться к главному меню':
        msg = bot.send_message(message.chat.id, "Оке, возвращаемся, группа не изменена", reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)
    else:
        usernames = message.text.split(" ")[1]
        group = " ".join(message.text.split(" ")[3:])
        add_user_in_group_query(group, usernames)
        msg = bot.send_message(message.chat.id, 'Пользователь добавлен', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)

def delete_from_group(message):
    if message.text == 'Вернуться к главному меню':
        msg = bot.send_message(message.chat.id, "Оке, возвращаемся, группа не изменена", reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)
    else:
        group = " ".join(message.text.split(' ')[3:])
        username = message.text.split(' ')[1]
        delete_user_from_group_query(group, username)
        msg = bot.send_message(message.chat.id, 'Пользователь удален', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)

def create_user_deal(message, user):
    if message.text == 'Вернуться к главному меню':
        msg = bot.send_message(message.chat.id, "Оке, возвращаемся без должников", reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)
    else:
        credit = int(message.text.split(' ')[0])
        desc = " ".join(message.text.split(' ')[1:])
        create_deal_query(message.from_user.username, user, credit, desc)
        msg = bot.send_message(message.chat.id, 'Птичка в клетке', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)


def create_group_deal(message, group):
    if message.text == 'Вернуться к главному меню':
        msg = bot.send_message(message.chat.id, "Оке, возвращаемся без должников", reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)
    else:
        summa = int(message.text.split(" ")[0])
        desc = message.text.split(" ")[1:]
        create_deal_group_query(message.from_user.username, " ".join(group), summa, " ".join(desc))
        msg = bot.send_message(message.chat.id, 'Кайф, Должники назначены', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)









