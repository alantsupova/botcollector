import sqlite3
import telebot
from telebot import types
from config import BOT_TOKEN
from sql import *
from handlers import *
from keyboards import deals_kb

token = BOT_TOKEN
bot = telebot.TeleBot(token)

'''def create_group_deal(message):
    if message.text == 'Вернуться к главному меню':
        msg = bot.send_message(message.chat.id, "Оке, возвращаемся без должников", reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)
    else:
        #user = GroupDeal.get_user(message.from_user.id)
        group = "Прятки"
        credit = int(message.text.split(' ')[0])
        desc = " ".join(message.text.split(' ')[1:])
        #create_deal_group_query(message.from_user.username, group, credit, desc)
        #user.delete_user(message.from_user.id)
        msg = bot.send_message(message.chat.id, 'Птичка в клетке', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, func)'''

@bot.message_handler(commands=["start"])
def start_message(message):
    msg = bot.send_message(message.chat.id, text='Привет, я - бот, который поможет выбивать долги из друзей)) '
                                           'Напиши, пожалуйста, номер , по которому твои друзься смогут переводить бабки, потом твои имя и фамилию, например:'
                                                 '89291137013 Александра Анцупова', reply_markup=main_keyboard())
    bot.register_next_step_handler(msg, add_user)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Вернуться к главному меню":
        bot.send_message(message.chat.id, text="вы в главном меню", reply_markup=main_keyboard())
    elif message.text == 'Помощь':
        bot.send_message(message.chat.id, text=help(), reply_markup=return_to_main_kb())
    elif message.text == "Обновить группу":
        bot.send_message(message.chat.id, text="Выбери действие", reply_markup=update_group_kb())
    elif message.text == 'Создать группу':
        msg = bot.send_message(message.chat.id, 'Напиши название новой группы одним сообщением', reply_markup=return_to_main_kb())
        bot.register_next_step_handler(msg, create_group)
    elif message.text == "Добавить чела в группу":
        bot.send_message(message.chat.id, text="Выбери группу",
                         reply_markup=groups_kb(message, "Добавить в группу "))
    elif message.text.startswith("Добавить в группу "):
        msg = bot.send_message(message.chat.id,
                               "Кайф, теперь выбери человечка для добавления",
                               reply_markup=add_user_to_group_kb(message, "Добавить ", " в "+" ".join(message.text.split(" ")[3:])))
        bot.register_next_step_handler(msg, insert_into_group)
    elif message.text == "Удалить чела из группы":
        bot.send_message(message.chat.id, text="Выбери группу",
                         reply_markup=groups_kb(message, "Удалить из группы "))
    elif message.text.startswith("Удалить из группы "):
        msg = bot.send_message(message.chat.id,
                               "Кайф, теперь выбери человечка для удаления",
                               reply_markup=delete_user_from_group_kb(message, "Удалить ", " из "+" ".join(message.text.split(" ")[3:])))
        bot.register_next_step_handler(msg, delete_from_group)
    elif message.text == 'Распределить деньги':
        bot.send_message(message.chat.id, text="Выбери действие", reply_markup=create_deal_kb())
    elif message.text == "Назначить пользователю":
        bot.send_message(message.chat.id, text="Выбери действие", reply_markup=user_list_kb("Назначить "))
    elif message.text.startswith("Назначить "):
        msg = bot.send_message(message.chat.id,
                               "Кайф, теперь черкани : сколько_тебе_должны описание. Например: 50 за пиво",
                               reply_markup=return_to_main_kb())
        bot.register_next_step_handler(msg, create_user_deal, message.text.split(" ")[1])
    elif message.text == "Между группой":
        bot.send_message(message.chat.id, text="Выбери группу",
                         reply_markup=groups_kb(message, "Группа "))
    elif message.text.startswith("Группа"):
        msg = bot.send_message(message.chat.id,
                               "Кайф, теперь черкани : сколько_потратил описание. Например: 1250 за репетицию",
                               reply_markup=return_to_main_kb())
        bot.register_next_step_handler(msg, create_group_deal, message.text.split(" ")[1:])
    elif message.text == "Должники":
        bot.send_message(message.chat.id, text=debtors_list_query(message.from_user.username), reply_markup=return_to_main_kb())
    elif message.text == "Долги":
        bot.send_message(message.chat.id, text=creditors_list_query(message.from_user.username), reply_markup=return_to_main_kb())
    elif message.text == "Выплатить долг":
        bot.send_message(message.chat.id, text="Выбери долг",
                         reply_markup=deals_kb(message))
    elif message.text.startswith("Закрыть "):
        if message.text == 'Вернуться к главному меню':
            msg = bot.send_message(message.chat.id, "Оке, возвращаемся, обойдется сегодня без денег",
                                   reply_markup=main_keyboard())
            bot.register_next_step_handler(msg, func)
        else:
            username = message.text.split(' ')[1]
            credit = int(message.text.split(' ')[3])
            delete_deal_query(username[1:], credit)
            msg = bot.send_message(message.chat.id, 'Кайф, ты больше не шмырь позорный', reply_markup=main_keyboard())
            bot.register_next_step_handler(msg, func)







if __name__ == '__main__':
    bot.infinity_polling()
