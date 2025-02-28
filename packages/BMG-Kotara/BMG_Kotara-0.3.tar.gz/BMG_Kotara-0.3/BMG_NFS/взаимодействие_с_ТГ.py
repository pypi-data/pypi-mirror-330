# pip install pytz
# pip install python-dotenv
# pip install python-telegram-bot==13.7

import os
import time
from datetime import datetime
from pytz import UTC
from dotenv import load_dotenv
from telegram import Bot

RED = '\x1b[31m'
GREEN = '\x1b[32m'
YELLOW = '\x1b[33m'
RESET = '\x1b[39m'

load_dotenv()
ТОКЕН = os.getenv('токен')
if not ТОКЕН:
    raise KeyError('Не найден файл .env')
БОТ = Bot(ТОКЕН)
этот_файл = __file__
this_folder = os.path.dirname(этот_файл)

def отправить_сообщение(сообщение, айди, кнопки=None):
    if type(айди) is int:
        try:
            БОТ.send_message(chat_id=айди, text=сообщение, reply_markup=кнопки)
        except Exception as error:
            print(f"Возникла ошибка {RED}{error}{RESET}")
    else:
        print(сообщение)

def проверить_входящие(айди=None, максимальное_ожидание_ответа_в_секундах=None):
    def отмена_если_нет_ответа(now):
        if максимальное_ожидание_ответа_в_секундах and (datetime.now(UTC) - now).seconds > максимальное_ожидание_ответа_в_секундах:
            print(f"Не было ответа в течении {максимальное_ожидание_ответа_в_секундах} сек. Перестаём следить за этим юзером")
            return True

    def создать_last_msg(update_id):
        with open(f'{this_folder}\\last_msg', 'w', encoding='utf-8') as file:
            file.write(str(update_id))

    def считать_last_msg():
        with open(f'{this_folder}\\last_msg', 'r', encoding='utf-8') as file:
            return int(file.read())

    now = datetime.now(UTC)
    if not os.path.exists(f'{this_folder}\\last_msg'):
        while True:
            try:
                обновления = БОТ.get_updates()
                if отмена_если_нет_ответа(now):
                    return None
                if not обновления:
                    time.sleep(0.5)
                    continue
                break
            except:
                continue
        last_msg = обновления[-1]
        if last_msg.message.date < now:
            создать_last_msg(last_msg.update_id)
        else:
            создать_last_msg(last_msg.update_id - 1)

    while True:
        if отмена_если_нет_ответа(now):
            return None
        try:
            обновления = БОТ.get_updates(offset=считать_last_msg() + 1)
        except:
            time.sleep(1)
            continue
        if not обновления:
            continue

        обновления.reverse()
        print(len(обновления))
        for msg in обновления:
            if айди is None or msg.effective_user.id == айди:
                создать_last_msg(msg.update_id)
                print(msg.effective_message.text)
                return msg
        time.sleep(0.5)

if __name__ == "__main__":
    проверить_входящие(478735661)