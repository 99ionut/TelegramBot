import telebot
import mysql.connector

# ROBA UTILE
# bot.send_message(message.chat.id, '$_My_ads')

### DOCUMENTATION
###
###
###
###

# Bot's token
token = '1315794495:AAHz5CVPLTqUE3OoTFaXe54ZmrMHHZjL1Rk'

# Create the bot
bot = telebot.TeleBot(token)

soldi = 0
#user chat id
chatId = 0


# onStart
@bot.message_handler(commands=['start'])
def start_message(message):
    # Show the keyboard buttons
    chatId = message.chat.id
    if checkUserId(chatId) == 1: #if user id is already inserted...
        print("user inserted")
        insertUser(chatId)
    else:
        print("user not inserted")
        pass

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


# onTextReceived/ButtonPressedFromTheKeyboard
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '🖥 visit sites':
        visitSitesMenu(message)
    elif message.text.lower() == '💰 balance':
        balanceMenu(message)
    elif message.text.lower() == '🙌 referrals':
        pass
    elif message.text.lower() == '⚙ settings':
        pass
    elif message.text.lower() == '📊 my ads':
        pass
    elif message.text.lower() == '🏠 menu':
        startMenu(message)
    elif message.text.lower() == '💵 withdraw':
        bot.send_message(message.chat.id, chatId)


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


# Menus
def visitSitesMenu(message):
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton(
        text='🔎 Go to website', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(
        text='🛑 Report', callback_data=4), telebot.types.InlineKeyboardButton(
        text='⏭ Skip', callback_data=5))
    bot.send_message(
        message.chat.id, text="How much is 2 plus 2?", reply_markup=markup)

def startMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🖥 Visit sites', '💰 Balance')
    keyboard.add('🙌 Referrals', '⚙ Settings')
    keyboard.add('📊 My ads')
    bot.send_message(message.chat.id,
                     '🔥 Welcome to *EARN DOGE Today* Bot! 🔥 \n\nThis bot lets you earn Dogecoin by completing simple tasks. \n\nPress 🖥 *Visit sites* to earn by clicking links Press \n\nYou can also create your own ads with /newad. Use the /help command for more info.',
                     parse_mode='Markdown', reply_markup=keyboard)


def balanceMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, 'Avabile balance: balance dell user', parse_mode='Markdown',
                     reply_markup=keyboard)

#inserts new user in the DB
def insertUser(chatId):
    mydb = mysql.connector.connect(
        host="localhost",
        user="telegrambot",
        password="telegrambot",
        database="telegrambot"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO user (userId, referral, address, taskAlert, seeNsfw) VALUES (%s, %s, %s, %s, %s)"
    val = (chatId, chatId, 111, 1, 1)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

#check if user is already inserted in the DB
def checkUserId(chatId):
    print("chech user id")
    mydb = mysql.connector.connect(
        host="localhost",
        user="telegrambot",
        password="telegrambot",
        database="telegrambot"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user WHERE userId = " + str(chatId))
    myresult = mycursor.fetchall()

    if  myresult:
        print("user exists")
        return 0
    else:
        print("user is new")
        return 1



# waitForUserInteraction
bot.polling()
