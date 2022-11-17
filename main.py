import os
import telebot
import subprocess
import time

bot = telebot.TeleBot('5424104954:AAG8liH8DrKHKPHKpXCJ0uOYZuV01XmicR8')
bot_password = 'B^VR5cb6g53'


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, я - Парсинг Бот."
                                           " Я умею парсить данные об участниках групп Вконтакте: id пользователя, "
                                           "имя, фамилия, дату рождения, номер телефона, город, "
                                           "id группы, название группы."
                                           " Чтобы начать парсить отправьте, пожалуйста, документ в формате .txt, "
                                           "в котором содержатся ссылки на группы ВК (каждая с новой строки).")


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        src = os.getcwd() + f'//{file_name}'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Задача принята и обрабатывается 🤖 Это может занять какое-то время. "
                              "Как только парсинг завершится, я вышлю файл Excel.")
        subprocess.call('python parsing_body.py', shell=True)
        file_name_send = file_name.split('.')[0]
        doc = open(f'{file_name_send}.xlsx', 'rb')
        bot.send_document(message.chat.id, doc)
        doc.close()
        new_file.close()
        os.remove(f'{file_name_send}.xlsx')
        os.remove(f'{file_name}')
    except Exception as e:
        e = str(e)
        bot.reply_to(message, e)


if __name__ == '__main__':
    bot.infinity_polling()
