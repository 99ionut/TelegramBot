import telebot
from block_io import BlockIo
import string
import random
import dbConnector

# DB CONNECTOR SINGLETON
connector = dbConnector.connect()

# Crypto API token
version = 2
block_io = BlockIo('b239-c199-7b18-9ee9', 'telegrambot', version)
# Bot's token
token = '1315794495:AAHz5CVPLTqUE3OoTFaXe54ZmrMHHZjL1Rk'

# Create the bot
bot = telebot.TeleBot(token)


# onStart
@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.text.replace('/start ',''))
    chatId = message.chat.id
    if checkUserId(chatId) == 1: #if user id is new insert...
        print("user inserted")
        userAddress = block_io.get_new_address(label=chatId)
        print(userAddress["data"]["address"])
        insertUser(chatId, userAddress["data"]["address"])
        createReferralCode(message)
    else:
        print("user not inserted")
        pass
    startMenu(message)


#@bot.message_handler(commands=['test'])
#def start_message(message):
#    markup = telebot.types.InlineKeyboardMarkup()
#    markup.add(telebot.types.InlineKeyboardButton(
#        text='Three', callback_data=3))
#    markup.add(telebot.types.InlineKeyboardButton(
#        text='Four', callback_data=4))
#    markup.add(telebot.types.InlineKeyboardButton(
#        text='Five', callback_data=5))
#    bot.send_message(
#        message.chat.id, text="How much is 2 plus 2?", reply_markup=markup)




#@bot.callback_query_handler(func=lambda call: True)
#def query_handler(call):
#    bot.answer_callback_query(
#        callback_query_id=call.id, text='Answer accepted!')
#    answer = 'You made a mistake'
#    if call.data == '4':
#        answer = 'You answered correctly!'

#    bot.send_message(call.message.chat.id, answer)
#    bot.edit_message_reply_markup(
#        call.message.chat.id, call.message.message_id)




# onTextReceived/ButtonPressedFromTheKeyboard
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == '🖥 visit sites':
        visitSitesMenu(message)
    elif message.text.lower() == '💰 balance':
        balanceMenu(message)
    elif message.text.lower() == '🙌🏻 referrals':
        referralMenu(message)
    elif message.text.lower() == '⚙ settings':
        settingsMenu(message)
    elif message.text.lower() == '📊 my ads':
        adsMenu(message)
    elif message.text.lower() == '🏠 menu':
        startMenu(message)
    elif message.text.lower() == '💵 withdraw':
        withdrawMenu(message)
    elif message.text.lower() == '➕ deposit':
        depositMenu(message)
    elif message.text.lower() == '🕑 history':
        historyMenu(message)
    elif message.text.lower() == '❌ cancel':
        cancelWithdrawMenu(message)
    elif message.text.lower() == '➕ new ad':
        createAdCampagin(message)




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
    keyboard.add('🙌🏻 Referrals', '⚙ Settings')
    keyboard.add('📊 My ads')
    bot.send_message(message.chat.id,
                     '🔥 Welcome to *EARN DOGE Today* Bot! 🔥 \n\nThis bot lets you earn Dogecoin by completing simple tasks. \n\nPress 🖥 *Visit sites* to earn by clicking links Press \n\nYou can also create your own ads with /newad. Use the /help command for more info.',
                     parse_mode='Markdown', reply_markup=keyboard)

def createReferralCode(message):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(8))

    mycursor = connector.cursor()
    print('UPDATE user SET referral = \"'+ result_str +'\"  WHERE userId = '+ str(message.chat.id))
    mycursor.execute('UPDATE user SET referral = \"'+ result_str +'\"  WHERE userId = '+ str(message.chat.id))
    connector.commit()

    print("referral code inserted = "+ result_str)

def referralMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🖥 Visit sites', '💰 Balance')
    keyboard.add('🙌🏻 Referrals', '⚙ Settings')
    keyboard.add('📊 My ads')

    bot.send_message(message.chat.id,
                    'You have *0* referrals, and earned *0* DOGE. \nTo refer people, send them to: \n\n'+getReferralCode(message.chat.id)+' \n\nYou will earn *15%* of each user\'s earnings from tasks, and *1%* of DOGE they spend on ads.',
                    parse_mode='Markdown', reply_markup=keyboard)

def adsMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ New ad', '📊 My ads')
    keyboard.add('🏠 Menu')

    if checkUserAds(message.chat.id) == 0:
        print("no campaign")
        bot.send_message(message.chat.id, "You don't have any ad campaigns yet.", parse_mode='Markdown',
                     reply_markup=keyboard)
    else:
        print("yes campaign")
        print(getUserAds(message.chat.id))
        bot.send_message(message.chat.id, "You currently have *" +str(checkUserAds(message.chat.id))+"* Ads", parse_mode='Markdown',
                         reply_markup=keyboard)
        ads = getUserAds(message.chat.id)
        nrAds = checkUserAds(message.chat.id)
        adsString = ""
        print("ads are: "+ str(ads))
        for i in range(int(nrAds)):
                adsString = "Title: "+str(ads[i][1])+"\nDescription: "+str(ads[i][2])+\
                            "\nNSFW: "+str(ads[i][3])+"\nClick: "+str(ads[i][4])+\
                            "\nCPC: "+str(ads[i][5])+"\nDaily Budget: "+str(ads[i][6])+\
                            "\nStatus: "+str(ads[i][7])+"\nURL: "+str(ads[i][8])
                bot.send_message(message.chat.id, adsString,parse_mode='Markdown',reply_markup=keyboard)
                adsString = ""

def createAdCampaign(message):
    mycursor = connector.cursor()
    mycursor.execute('INSERT INTO adcampaign VALUES('','','','','','')')
    connector.commit()

    campaignID | userID | title | description | budget

    12(A I)           33112     ''        ''           ''

    GET ultimo campaignID where userid == 

    12          33214         

    12          33214     dfsdf        sdfsdfs         10



    mycursor = connector.cursor()
    mycursor.execute('UPDATE adcampaign SET userId = '+ message.chat.id +' WHERE campaignId = ' + str(message.chat.id))
    connector.commit()

def newAdUrlMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌ Cancel')
    print(message)
    url = bot.send_message(message.chat.id, "Enter the URL to send traffic to: \n\nIt should begin with https:// or http://", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=url, callback=addUrl)

   
def newAdTitleMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Skip','❌ Cancel')
    title = bot.send_message(message.chat.id, "Enter a title for your ad: \n\nIt must be between *5* and *80* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=title, callback=addTitle)

def newAdDescriptionMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Skip','❌ Cancel')
    title = bot.send_message(message.chat.id, "Enter a description for your ad:\n\nIt must be between *10* and *180* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=title, callback=addTitle)


def addUrl(message):
    # if the url is with http:// or https://
    if(message.text[0:6] == "http://" or message.text[0:7] == "https://"):
        # Query for adding the url to the db
        mycursor = connector.cursor()

        

        mycursor.execute('UPDATE adcampaign SET url = '+ +' WHERE userId = ' + str(message.chat.id))
        connector.commit()

        newAdTitleMenu()

    # else return to current section for a wrong url submitted
    else:
        newAdUrlMenu()
        
        

def addTitle(message):
    if(message.text == "Skip"):
        
    pass


def balanceMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "Available balance: *"+str(getUserBalance(message.chat.id))+" DOGE*", parse_mode='Markdown',
                     reply_markup=keyboard)

def depositMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "To deposit funds, send at least *1 DOGE* to the following address:\n\n *" + str(getUserAddress(message.chat.id)) + "* \n\n Deposits are not subject to a fee.",
                     parse_mode='Markdown',
                     reply_markup=keyboard)

def withdrawMenu2(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌ Cancel')
    bot.send_message(message.chat.id, "Your balance: *" + str(getUserBalance(message.chat.id)) + " DOGE*\n\nTo withdraw, enter your Dogecoin address:",
                     parse_mode='Markdown',
                     reply_markup=keyboard)

def withdrawMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')

    if(float(getUserBalance(message.chat.id)) < 4):
        bot.send_message(message.chat.id, "Your balance is too small to withdraw.\n\n Available balance: *" + str(getUserBalance(message.chat.id)) + " DOGE* \n\n Minimum withdrawal: *4 DOGE*",
                     parse_mode='Markdown',
                     reply_markup=keyboard)
    else:
        withdrawMenu2(message)

def cancelWithdrawMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "Your withdrawal has been canceled.",
                     parse_mode='Markdown',
                     reply_markup=keyboard)

def historyMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "*Click the link below to see your transaction history* \n\n" +str(getUserHistory(message.chat.id))+"", parse_mode='Markdown',
                     reply_markup=keyboard)

def settingsMenu(message):
        print("settings")
        nsfw = getNsfw(message.chat.id)
        markup = telebot.types.InlineKeyboardMarkup()

        if nsfw == 1:
            markup.add(telebot.types.InlineKeyboardButton(
            text='❌ Disable NSFW', callback_data=1))
            markup.add(telebot.types.InlineKeyboardButton(
            text='⬅ Back', callback_data=3))
        else:
            markup.add(telebot.types.InlineKeyboardButton(
            text='✅ Enable NSFW', callback_data=2))
            markup.add(telebot.types.InlineKeyboardButton(
            text='⬅ Back', callback_data=3))

        if nsfw == 1:
            bot.send_message(
            message.chat.id, text="NSFW/pornographic ads are currently ✅ *Enabled* .", reply_markup=markup, parse_mode='Markdown')
        else:
            bot.send_message(
            message.chat.id, text="NSFW/pornographic ads are currently ❌ *Disabled* .", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
        bot.answer_callback_query(
            callback_query_id=call.id, text='Settings Saved!')
        if call.data == '1':
            answer = 'NSFW Ads have been Disabled!'
            disableNsfw(call.message.chat.id)
        elif call.data == '2':
            answer = 'NSFW Ads have Enabled!'
            enableNsfw(call.message.chat.id)
        elif call.data == '3':
            answer = '⬅ Back to main menu'

        bot.send_message(call.message.chat.id, answer)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)

#inserts new user in the DB
def insertUser(chatId,userAddress):

    mycursor = connector.cursor()

    sql = "INSERT INTO user (userId, referral, address, taskAlert, seeNsfw) VALUES (%s, %s, %s, %s, %s)"
    val = (chatId, chatId, userAddress, 1, 1)
    mycursor.execute(sql, val)
    connector.commit()
    print(mycursor.rowcount, "record inserted.")

#check if user is already inserted in the DB
def checkUserId(chatId):
    print("check user id")

    mycursor = connector.cursor()
    mycursor.execute("SELECT * FROM user WHERE userId = " + str(chatId))
    myresult = mycursor.fetchall()

    if  myresult:
        print("user exists")
        return 0
    else:
        print("user is new")
        return 1

def checkUserAddress(chatId):
    print("check user Address")

    mycursor = connector.cursor()
    mycursor.execute("SELECT address FROM user WHERE userId = " + str(chatId))
    myresult = mycursor.fetchall()

    if myresult:
        print("address exists")
        return myresult[0][0]
    else:
        print("address doesnt exist")
        return 0

#returns the number of ads of a user
def checkUserAds(chatId):
        print("check user Ads")

        print("chat id ads " + str(chatId))
        mycursor = connector.cursor()
        print("SELECT COUNT(userId) FROM adcampaign WHERE userId = " + str(chatId) + " GROUP BY userId")
        mycursor.execute("SELECT COUNT(userId) FROM adcampaign WHERE userId = " + str(chatId)+" GROUP BY userId")

        myresult = mycursor.fetchall()

        if myresult:
            print("ads exists")
            print(myresult)
            return myresult[0][0]
        else:
            print("ads doesnt exist")
            return 0

def getReferralCode(chatId):

        mycursor = connector.cursor()
        mycursor.execute('SELECT referral FROM user WHERE userId = ' + str(chatId))
        

        myresult = mycursor.fetchall()

        if myresult:
            fullReferral = "https://t.me/EarnDogeTodayBot?start="+str(myresult[0][0])
            print(fullReferral)
            return fullReferral
        else:
            print("ERROR")
            return 0

def getUserBalance(chatId):
    print("check user balance")
    balance = block_io.get_address_by(label=chatId)["data"]["available_balance"]
    print(balance)
    return str(float(balance))

def getUserAddress(chatId):
    print("check user address")
    address = checkUserAddress(chatId)
    print(address)
    return address

def getUserHistory(chatId):
    print("check user history")
    address = getUserAddress(chatId)
    history = "https://sochain.com/address/DOGETEST/"+address
    print(history)
    return history



def getNsfw(chatId):
    print("check user Nsfw settings")

    mycursor = connector.cursor()
    mycursor.execute("SELECT seeNsfw FROM user WHERE userId = " + str(chatId))
    myresult = mycursor.fetchall()

    print("risultato check nsfw = " + str(myresult[0][0]))
    if myresult:
        print("seeNsfw exists")
        return myresult[0][0]
    else:
        print("seeNsfw doesnt exist")
        return 0

#returns all data of all ads of a user
def getUserAds(chatId):
        print("get all user Ads")

        mycursor = connector.cursor()
        print("SELECT * FROM adcampaign WHERE userId = " + str(chatId))
        mycursor.execute("SELECT * FROM adcampaign WHERE userId = " + str(chatId))

        myresult = mycursor.fetchall()
        return myresult

def disableNsfw(chatId):
    print("disable user Nsfw settings")

    mycursor = connector.cursor()
    mycursor.execute("UPDATE user SET seeNsfw = 0 WHERE userId = " + str(chatId))
    connector.commit()

def enableNsfw(chatId):
    print("enable user Nsfw settings")
    print(chatId)

    mycursor = connector.cursor()
    mycursor.execute("UPDATE user SET seeNsfw = 1 WHERE userId = " + str(chatId))
    connector.commit()

# waitForUserInteraction
bot.polling()
