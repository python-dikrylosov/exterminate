# -*- coding: utf-8 -*-
import time
import os
import pandas as pd
import sqlite3
import password
#Подключение биткоин и других кошельков
from block_io import BlockIo
api_key_block_btc = password.api_key_block_btc
api_key_block_ltc = password.api_key_block_ltc
api_key_block_doge = password.api_key_block_doge
SECRET_PIN = password.SECRET_PIN #kry2011gm
API_VERSION = 2
block_io_btc = BlockIo(api_key_block_btc, SECRET_PIN, API_VERSION)
block_io_ltc = BlockIo(api_key_block_ltc, SECRET_PIN, API_VERSION)
block_io_doge = BlockIo(api_key_block_doge, SECRET_PIN, API_VERSION)
#Коды и модуль для телеграмма
# user_id = message.from_user.id
# user_first_name = message.from_user.first_name
# user_last_name = message.from_user.last_name
# user_username = message.from_user.username
TOKEN = password.TOKEN
import telebot
from telebot import types
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=["start"])
def start(m, res=False):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id INTEGER)""")

    connect.commit()

    people_id = m.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        user_id = [m.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_person = types.KeyboardButton("🌐 О пользователе 🌐")
        markup.add(item_person)
        bot.send_message(m.chat.id, "Такой пользователь существует", reply_markup=markup)
        bot.send_message(810299040, "Такой пользователь существует " + str(m.from_user.id))

    answer = 'Принимая данное соглашение вы согласны с соблюдением всех возможных законов'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_Accept_user_agreement = types.KeyboardButton("✅ Принять пользовательское соглашение ✅")
    item_Accept_user_agreement_all = types.KeyboardButton("📚 Полный текст соглашения 📚")
    item_Refuse = types.KeyboardButton("❌ Отказаться ❌")
    markup.add(item_Accept_user_agreement)
    markup.add(item_Accept_user_agreement_all)
    markup.add(item_Refuse)
    bot.send_message(m.chat.id,answer , reply_markup=markup)
    bot.send_message(810299040, "Соглашение принято " + str(m.from_user.id))

@bot.message_handler(commands=["delete"])
def delete(m, res=False):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = m.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == '✅ Принять пользовательское соглашение ✅':
        print(str(time.strftime("%Y-%m-%d ")) + str(message.chat.id) + " " + message.from_user.first_name + " " + str(message.text))

        # проверка наличия пользователя в базе
        if os.path.isfile(str(message.from_user.id) + "_log.txt") == False:
            import pandas as pd
            import numpy as np
            btc_address = block_io_btc.get_address_balance(labels=str(message.from_user.id))
            data_btc = btc_address
            data_data_btc = data_btc["data"]
            balance_btc = data_data_btc["balances"]
            data_address_btc = pd.DataFrame(balance_btc)
            address_btc = data_address_btc['address']
            on_address_btc = address_btc[0]
            print(on_address_btc)
            ltc_address = block_io_ltc.get_address_balance(labels=str(message.from_user.id))
            doge_address = block_io_doge.get_address_balance(labels=str(message.from_user.id))

            data_person = pd.DataFrame([["id", "Fname", "BTC", "DOGE", "LTC"],
                                        [str(message.from_user.id), str(message.from_user.first_name),
                                         str(on_address_btc)]])
            data_person.to_csv(str(message.from_user.id) + "_log.txt")

            print(str(time.strftime("%Y-%m-%d ")) + "пользователь в базе: " + str(message.from_user.id))
            print("Пользовательский id : " + str(message.from_user.id))
            print(btc_address)
            print(ltc_address)
            print(doge_address)
            print(str(time.strftime("%Y-%m-%d ")) + "Новый пользователь зарегистрирован в базе: " + str(
                message.from_user.id))

            bot.send_message(810299040, str(time.strftime("%Y-%m-%d ")) + "пользователь в базе: " + str(message.from_user.id))
        elif os.path.isfile(str(message.from_user.id) + "_log.txt") == True:
            import pandas as pd
            import numpy as np
            btc_address = block_io_btc.get_address_balance(labels=str(message.from_user.id))
            data_btc = btc_address
            data_data_btc = data_btc["data"]
            balance_btc = data_data_btc["balances"]
            data_address_btc = pd.DataFrame(balance_btc)
            address_btc = data_address_btc['address']
            on_address_btc = address_btc[0]
            print(on_address_btc)
            ltc_address = block_io_ltc.get_address_balance(labels=str(message.from_user.id))
            data_ltc = ltc_address
            data_data_ltc = data_ltc["data"]
            balance_ltc = data_data_ltc["balances"]
            data_address_ltc = pd.DataFrame(balance_ltc)
            address_ltc = data_address_ltc['address']
            on_address_ltc = address_ltc[0]
            print(on_address_ltc)
            doge_address = block_io_doge.get_address_balance(labels=str(message.from_user.id))

            data_person = pd.DataFrame([["id", "Fname", "BTC", "DOGE", "LTC"],
                                        [str(message.from_user.id), str(message.from_user.first_name),
                                         str(on_address_btc), str(on_address_ltc)]])
            data_person.to_csv(str(message.from_user.id) + "_log.txt")

            print(str(time.strftime("%Y-%m-%d ")) + "пользователь в базе: " + str(message.from_user.id))
            print("Пользовательский id : " + str(message.from_user.id))
            print(btc_address)
            print(ltc_address)
            print(doge_address)


        answer = "Спасибо за доверие " + str(message.from_user.first_name) + "\n" \
                 + " : " + str(message.from_user.id) + "\n" \
                 + " : " + "\n" + str(on_address_btc)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_volue_btc = types.KeyboardButton("📒 BTC кошелек")
        item_volue_doge = types.KeyboardButton("📙 DOGE кошелек")
        item_volue_ltc = types.KeyboardButton("📗LTC кошелек")

        item_volue = types.KeyboardButton("💼 Обмен на рубли")
        item_volue_remote = types.KeyboardButton("🚧 Разработка, обновления и новости")
        item_person = types.KeyboardButton("🌐 О пользователе 🌐")
        markup.add(item_volue)
        markup.add(item_volue_btc, item_volue_ltc, item_volue_doge)
        markup.add(item_volue_remote, item_person)

        bot.send_message(message.chat.id, answer, reply_markup=markup)
        bot.send_message(810299040, answer)
    elif message.text.strip() == '🌐 О пользователе 🌐':
        import pandas as pd
        btc_address = block_io_btc.get_address_balance(labels=str(message.from_user.id))
        data_btc = btc_address
        data_data_btc = data_btc["data"]
        balance_btc = data_data_btc["balances"]
        data_address_btc = pd.DataFrame(balance_btc)
        address_btc = data_address_btc['address']
        on_address_btc = address_btc[0]
        print(on_address_btc)
        ltc_address = block_io_ltc.get_address_balance(labels=str(message.from_user.id))
        data_ltc = ltc_address
        data_data_ltc = data_ltc["data"]
        balance_ltc = data_data_ltc["balances"]
        data_address_ltc = pd.DataFrame(balance_ltc)
        address_ltc = data_address_ltc['address']
        on_address_ltc = address_ltc[0]
        print(on_address_ltc)
        answer = "Спасибо за доверие " + str(message.from_user.first_name) + "\n" \
                 + " : " + str(message.from_user.id) + "\n" \
                 + " : " + "\n" + str(on_address_btc)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_volue_btc = types.KeyboardButton("📒 BTC кошелек")
        item_volue_doge = types.KeyboardButton("📙 DOGE кошелек")
        item_volue_ltc = types.KeyboardButton("📗LTC кошелек")

        item_volue = types.KeyboardButton("💼 Обмен на рубли")
        item_volue_remote = types.KeyboardButton("🚧 Разработка, обновления и новости")
        item_person = types.KeyboardButton("🌐 О пользователе 🌐")
        markup.add(item_volue)
        markup.add( item_volue_btc, item_volue_ltc, item_volue_doge)
        markup.add(item_volue_remote, item_person)

        bot.send_message(message.chat.id, answer, reply_markup=markup)
        bot.send_message(810299040, answer)

    elif message.text.strip() == 'создание Российско-китайского центра экономического сотрудничества':
        bot.send_message(message.chat.id, "建立俄中经济合作中心 我假设有一个好的数据分析师" + str("\nhttps://vk.com/python_dikrylosov") + "\n" + "https://t.me/python8pro2023bot")
        bot.send_message(810299040, message.text.strip())
        bot.send_message(message.chat.id, "Этот ответ заложен заранее")
    elif message.text.strip() == 'сотрудничество по организации выращивания лечебных трав для поставок в КНР':
        bot.send_message(message.chat.id, "сотрудничество по организации выращивания лечебных трав для поставок в КНР")
        bot.send_message(810299040, message.text.strip())
        bot.send_message(message.chat.id, "сотрудничество по организации выращивания лечебных трав для поставок в КНР")

    else:
        print(type(message.text.strip()))
        for i in range(10000):
            print([i,message.text.strip()])
        import numpy as np
        from PIL import ImageGrab
        screen = np.array(ImageGrab.grab(bbox=(0, 0, 1280, 1024)))
        #print(screen)
        bot.send_message(message.chat.id, str(type(message.text.strip())))
        bot.send_message(810299040, message.text.strip())
        bot.send_message(message.chat.id, "Не похожа на все " + message.text.strip())
print("Запускаем бота")
bot.polling(none_stop=True, interval=0)
