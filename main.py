import telebot
from telebot import types
bot = telebot.TeleBot(key)
size = ''
pay_metod = ''
@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == '/start':
        bot.register_next_step_handler(message, go_get_pay_metod);
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2 = types.KeyboardButton("Большую")
        item1 = types.KeyboardButton('Маленькую')
        markup.add(item1, item2)
        bot.send_message(message.from_user.id, text="Какую вы хотите пиццу? Большую или маленькую?", reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start');

@bot.message_handler(content_types=["text"])
def go_get_pay_metod(message):
    bot.register_next_step_handler(message, go_confirm);
    if message.chat.type == 'private':
        global size;
        size = message.text.lower()
        if size in ('большую', 'маленькую'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item2 = types.KeyboardButton("Наличкой")
            item1 = types.KeyboardButton('Картой')
            markup.add(item1, item2)
            bot.send_message(message.from_user.id, text="Как вы будете платить?", reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, 'Простите, я вас не понял. Напишите /start',reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=["text"])
def go_confirm(message):
    bot.register_next_step_handler(message, go_end);
    if message.chat.type == 'private':
        global pay_metod;
        pay_metod = message.text.lower()
        if pay_metod in ('наличкой','картой'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item2 = types.KeyboardButton("Да")
            item1 = types.KeyboardButton('Нет')
            markup.add(item1, item2)
            bot.send_message(message.from_user.id, 'Вы хотите '+size+' пиццу, оплата - '+pay_metod+'?', reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, 'Простите, я вас не понял. Напишите /start',reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=["text"])
def go_end(message):
    if message.chat.type == 'private':
        if message.text == 'Да':
            bot.send_message(message.from_user.id, 'Спасибо за заказ!',reply_markup=types.ReplyKeyboardRemove())
        elif message.text == 'Нет':
            bot.send_message(message.from_user.id, 'Для повторения заказа напишите /start',reply_markup=types.ReplyKeyboardRemove())

bot.polling()