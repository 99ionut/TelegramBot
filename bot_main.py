import telebot


token = '1315794495:AAHz5CVPLTqUE3OoTFaXe54ZmrMHHZjL1Rk'

bot = telebot.TeleBot(token)
bot.delete_webhook()

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🖥 Visit sites', '💰 Balance')
    keyboard.add('🙌 Referrals', '⚙ Settings')
    keyboard.add('📊 My ads')
    bot.send_message(message.chat.id, '🔥 Welcome to *EARN DOGE Today* Bot! 🔥 \n\nThis bot lets you earn Dogecoin by completing simple tasks. \n\nPress 🖥 *Visit sites* to earn by clicking links Press \n\nYou can also create your own ads with /newad. Use the /help command for more info.',  parse_mode= 'Markdown', reply_markup=keyboard)


@bot.message_handler(commands=['test'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(
        text='Three', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(
        text='Four', callback_data=4))
    markup.add(telebot.types.InlineKeyboardButton(
        text='Five', callback_data=5))
    bot.send_message(
        message.chat.id, text="How much is 2 plus 2?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '🖥 Visit sites':
        bot.send_message(message.chat.id, '$_visit_sites')
    elif message.text.lower() == '💰 Balance':
        bot.send_message(message.chat.id, '$_balance')
    elif message.text.lower() == '🙌 Referrals':
        bot.send_message(message.chat.id, '$_referrals')
    elif message.text.lower() == '⚙ Settings':
        bot.send_message(message.chat.id, '$_settings')
    elif message.text.lower() == '📊 My Ads':
        bot.send_message(message.chat.id, '$_My_ads')
      


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(
        callback_query_id=call.id, text='Answer accepted!')
    answer = 'You made a mistake'
    if call.data == '4':
        answer = 'You answered correctly!'

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id)


bot.polling()
