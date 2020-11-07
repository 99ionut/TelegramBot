import telebot

#ROBA UTILE         
# bot.send_message(message.chat.id, '$_My_ads')

### DOCUMENTATION
###
###
###
###

#Bot's token
token = '1315794495:AAHz5CVPLTqUE3OoTFaXe54ZmrMHHZjL1Rk'

#Create the bot
bot = telebot.TeleBot(token)

soldi = 0

#onStart
@bot.message_handler(commands=['start'])
def start_message(message):
    #Show the keyboard buttons
    startMenu(message)

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


#onTextReceived/ButtonPressedFromTheKeyboard
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '🖥 visit sites':
        visitSitesMenu(message)
    elif message.text.lower() == '💰 balance':
        balanceMenu(message)
    elif message.text.lower() == '🙌 referrals':
        pass
    elif message.text.lower() == '⚙ settings':
        soldi += 1
        pass
    elif message.text.lower() == '📊 my ads':
        bot.send_message(message.chat.id, soldi)
        pass
    elif message.text.lower() == '🏠 menu':
        startMenu(message)
    elif message.text.lower() == '💵 withdraw':
        soldi -= 1
        bot.send_message(message.chat.id, 'TOLTO')
        


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





#Menus
def visitSitesMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('dffsdisit sites', 'sdsdsdf')
    keyboard.add('🙌 Refsdferrals', '⚙sdsdttings')
    keyboard.add('📊 Mysdf ads')
    bot.send_message(message.chat.id,'ciao ssssimone',parse_mode='Markdown', reply_markup=keyboard)

def startMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🖥 Visit sites', '💰 Balance')
    keyboard.add('🙌 Referrals', '⚙ Settings')
    keyboard.add('📊 My ads')
    bot.send_message(message.chat.id, '🔥 Welcome to *EARN DOGE Today* Bot! 🔥 \n\nThis bot lets you earn Dogecoin by completing simple tasks. \n\nPress 🖥 *Visit sites* to earn by clicking links Press \n\nYou can also create your own ads with /newad. Use the /help command for more info.',  parse_mode= 'Markdown', reply_markup=keyboard)

def balanceMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id,'Avabile balance: balance dell user',parse_mode='Markdown', reply_markup=keyboard)


#waitForUserInteraction
bot.polling()
