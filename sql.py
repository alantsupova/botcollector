import sqlite3
import re

def add_user_query(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    tel = message.text.split(" ")[0]
    name = message.text.split(" ")[1]
    surname = message.text.split(" ")[2]
    users_list = [message.chat.id, message.from_user.username, name,
                  surname, tel]
    cursor.execute("INSERT INTO users (user_id, username, first_name, second_name, tel) VALUES(?, ?, ?, ?, ?);",
                   (users_list[0], users_list[1], users_list[2], users_list[3], users_list[4]))
    connect.commit()
    connect.close()

def add_group_query(message, group_name):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO groups (group_name) VALUES('{group_name}');")
    connect.commit()

    query = f"SELECT id FROM users WHERE username='{message.from_user.username}' "
    cursor.execute(query)
    user_id = cursor.fetchall()[0][0]

    query = f"SELECT group_id FROM groups WHERE group_name='{group_name}' "
    cursor.execute(query)
    group_id = cursor.fetchall()[0][0]

    query = f"INSERT INTO group_users (user_id, group_id) VALUES ({user_id}, {group_id})"
    cursor.execute(query)
    connect.commit()

    connect.close()

def add_user_in_group_query(group_name, user):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{user}' "
    cursor.execute(query)
    user_id = cursor.fetchall()[0][0]
    query = f"SELECT group_id FROM groups WHERE group_name='{group_name}'"
    cursor.execute(query)
    group_id = cursor.fetchall()[0][0]

    cursor.execute("INSERT INTO group_users(user_id, group_id) VALUES(?, ?);",
                   (user_id, group_id))
    connect.commit()
    connect.close()

def delete_user_from_group_query(group, users):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{users}' "
    cursor.execute(query)
    user_id = cursor.fetchall()[0][0]
    query = f"SELECT group_id FROM groups WHERE group_name='{group}'"
    cursor.execute(query)
    group_id = cursor.fetchall()[0][0]

    cursor.execute(f"DELETE FROM group_users WHERE user_id={user_id} AND group_id={group_id};")
    connect.commit()
    connect.close()

def create_deal_query(creditor, debitor, credit, desc):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{creditor}' "
    cursor.execute(query)
    creditor_id = cursor.fetchall()[0][0]

    query = f"SELECT id FROM users WHERE username='{debitor}' "
    cursor.execute(query)
    debitor_id = cursor.fetchall()[0][0]

    cursor.execute(f"INSERT INTO deals(creditor_id, debtor_id, credit, description) VALUES({creditor_id}, {debitor_id}, {credit}, '{desc}');")
    connect.commit()
    connect.close()

def create_deal_group_query(creditor, debitor, credit, desc):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{creditor}' "
    cursor.execute(query)
    creditor_id = cursor.fetchall()[0][0]

    query = f"SELECT group_id FROM groups WHERE group_name='{debitor}' "
    cursor.execute(query)
    debitor_group_id = cursor.fetchall()[0][0]

    query = f"SELECT user_id FROM group_users WHERE group_id='{debitor_group_id}' "
    cursor.execute(query)
    ids = cursor.fetchall()
    debitor_ids = []
    for id in ids:
        debitor_ids.append(id[0])

    query = f"SELECT COUNT(user_id) FROM group_users WHERE group_id='{debitor_group_id}' "
    cursor.execute(query)
    count_debitors = cursor.fetchall()[0][0]

    for debitor_id in debitor_ids:
        if debitor_id != creditor_id:
            cursor.execute(f"INSERT INTO deals(creditor_id, debtor_id, credit, description) VALUES({creditor_id}, {debitor_id}, {credit/count_debitors}, '{desc}');")

    connect.commit()
    connect.close()

def debtors_list_query(creditor):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{creditor}' "
    cursor.execute(query)
    creditor_id = cursor.fetchall()[0][0]

    query = f"SELECT debtor_id, credit, description FROM deals WHERE creditor_id='{creditor_id}' "
    cursor.execute(query)
    info = cursor.fetchall()
    debitor_ids = []
    credits = []
    desc = []
    for id in info:
        debitor_ids.append(id[0])
        credits.append(id[1])
        desc.append(id[2])
    deb_names = []
    for id in debitor_ids:
        query = f'SELECT username, tel FROM users WHERE id={id}'
        cursor.execute(query)
        d = cursor.fetchall()[0]
        deb_names.append(d)
    inf = []
    for i in range(len(deb_names)):
        inf.append([deb_names[i], credits[i], desc[i]])
    connect.close()
    result = ["Список актуальных должников : \n"]
    for s in inf:
        result_str = '\n@' + s[0][0] + ' должен тебе ' + str(s[1]) + ' \n Причина: ' + s[2]
        if s[0][1] is not None:
            result_str += "\n Номер телефона: " + str(s[0][1])
        else:
            result_str += "\n Номер телефона не оставил/а"
        result.append(result_str)
    return "\n".join(result)

def creditors_list_query(debitor):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{debitor}' "
    cursor.execute(query)
    debtor_id = cursor.fetchall()[0][0]


    query = f"SELECT creditor_id, credit, description FROM deals WHERE debtor_id='{debtor_id}' "
    cursor.execute(query)
    info = cursor.fetchall()
    creditor_ids = []
    credits = []
    desc = []
    for id in info:
        creditor_ids.append(id[0])
        credits.append(id[1])
        desc.append(id[2])
    cre_names = []
    tels = []
    for id in creditor_ids:
        query = f'SELECT username, tel FROM users WHERE id={id}'
        cursor.execute(query)
        d = cursor.fetchall()[0]
        cre_names.append(d[0])
        tels.append(d[1])
    inf = []
    for i in range(len(cre_names)):
        inf.append([cre_names[i],tels[i], credits[i], desc[i]])
    connect.close()

    result = ["Список актуальных долгов : \n"]
    for s in inf:
        result_str = '\n@' + s[0]+ ' ты должен/жна ' + str(s[2]) + ' \n Причина: ' + s[3]
        if s[1] is not None:
            result_str += "\n Номер телефона: " + str(s[1])
        else:
            result_str += "\n Номер телефона не оставил/а"
        result.append(result_str)
    return "\n".join(result)

def name_creditors_list_query(debitor):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{debitor}' "
    cursor.execute(query)
    debtor_id = cursor.fetchall()[0][0]


    query = f"SELECT creditor_id, credit, description FROM deals WHERE debtor_id='{debtor_id}' "
    cursor.execute(query)
    info = cursor.fetchall()
    creditor_ids = []
    credits = []
    desc = []
    for id in info:
        creditor_ids.append(id[0])
        credits.append(id[1])
        desc.append(id[2])
    cre_names = []
    tels = []
    for id in creditor_ids:
        query = f'SELECT username, tel FROM users WHERE id={id}'
        cursor.execute(query)
        d = cursor.fetchall()[0]
        cre_names.append(d[0])
        tels.append(d[1])
    inf = []
    for i in range(len(cre_names)):
        inf.append([cre_names[i],tels[i], credits[i], desc[i]])
    connect.close()

    result = []
    for s in inf:
        result_str = 'Закрыть @' + s[0]+ ' долг ' + str(s[2]) + ' \n ,причина: ' + s[3] + '\n'
        result.append(result_str)
    return result

def users_query():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f'SELECT username FROM users'
    cursor.execute(query)
    data = cursor.fetchall()
    res = []
    for i in data:
        res.append(i[0])
    return res
    connect.close()

def users_not_in_group_query(group):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    query = f'SELECT group_id FROM GROUPS WHERE group_name = "{group}"'
    cursor.execute(query)
    group_id = cursor.fetchall()[0][0]

    query = f'SELECT username FROM users WHERE id NOT IN (SELECT user_id FROM group_users WHERE group_id = {group_id})'
    cursor.execute(query)
    data = cursor.fetchall()
    res = []
    for i in data:
        res.append(i[0])
    return res
    connect.close()

def users_in_group_query(group):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f'SELECT username FROM users WHERE id IN (SELECT user_id FROM group_users WHERE group_id = (SELECT group_id FROM GROUPS WHERE group_name = "{group}"))'
    cursor.execute(query)
    data = cursor.fetchall()
    res = []
    for i in data:
        res.append(i[0])
    return res
    connect.close()


def groups_with_user_query(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f'SELECT group_name FROM groups JOIN group_users using(group_id) WHERE user_id = (SELECT id from users WHERE username = "{message.from_user.username}")'
    cursor.execute(query)
    data = cursor.fetchall()
    res = []
    for i in data:
        res.append(i[0])
    return res
    connect.close()

def delete_deal_query(user, summa):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    query = f"SELECT id FROM users WHERE username='{user}' "
    cursor.execute(query)
    user_id = cursor.fetchall()[0][0]

    cursor.execute(f"DELETE FROM deals WHERE creditor_id={user_id} and credit={summa}")
    connect.commit()
    connect.close()