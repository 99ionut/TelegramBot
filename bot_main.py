#!/usr/bin/python 
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

slowest = 0.035
faster = 0.038
fastest = 0.789

# onStart
@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    print(message.text.replace('/start ', ''))
    chatId = message.chat.id
    if checkUserId(chatId) == 1:  # if user id is new insert
        print("user inserted")
        userAddress = block_io.get_new_address(label=chatId)
        print(userAddress["data"]["address"])
        insertUser(chatId, userAddress["data"]["address"])
        createReferralCode(message)
    else:
        print("user not inserted")
        pass
    startMenu(message)


# @bot.message_handler(commands=['test'])
# def start_message(message):
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
        createAdCampaign(message)




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

    print("referral code inserted = " + result_str)

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
    #SELECT MAX(campaignId), clicks, cpc, dailyBudget, description, nsfw, status, title, url, userId
    #FROM adcampaign
    #WHERE userId = 626602519   
     
    print('created new campaign')

    mycursor = connector.cursor()
    mycursor.execute('INSERT INTO adcampaign(userId) VALUES('+str(message.chat.id)+')')
    connector.commit()

    mycursor = connector.cursor()
    mycursor.execute("SELECT MAX(campaignId) FROM adcampaign WHERE userId = " + str(message.chat.id))
    myresult = mycursor.fetchall()
    maxid = myresult[0][0]

    print('max campaign id = ' + str(maxid))
    newAdUrlMenu(message,maxid)

def newAdUrlMenu(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌ Cancel')
    url = bot.send_message(message.chat.id, "Enter the URL to send traffic to: \n\nIt should begin with https:// or http://", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=url,maxid=maxid, callback=addUrl)

def addUrl(message,maxid):
    # if the url is with http:// or https://
    if(message.text[0:7] == "http://" or message.text[0:8] == "https://"):

        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET url = \'' + str(message.text) + '\' WHERE campaignId = ' + str(maxid))
        connector.commit()
        newAdTitleMenu(message,maxid)
    else:
        newAdUrlMenu(message,maxid)
   
def newAdTitleMenu(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⏭️ Skip','❌ Cancel')
    title = bot.send_message(message.chat.id, "Enter a title for your ad: \n\nIt must be between *5* and *80* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=title, maxid=maxid, callback=addTitle)

def addTitle(message,maxid):
    # if the title is between 5 and 80 characters
    if(len(str(message.text))>=5 and len(str(message.text))<=80):

        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET title = \'' + str(message.text) + '\' WHERE campaignId = ' + str(maxid))
        connector.commit()
        newAdDescriptionMenu(message,maxid)
    else:
        newAdTitleMenu(message,maxid)

def newAdDescriptionMenu(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⏭️ Skip','❌ Cancel')
    title = bot.send_message(message.chat.id, "Enter a description for your ad:\n\nIt must be between *10* and *180* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=title,maxid=maxid, callback=addDescription)

def addDescription(message,maxid):
    # if the description is between 10 and 180 characters
    if(len(str(message.text))>=10 and len(str(message.text))<=180):

        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET description = \'' + str(message.text) + '\' WHERE campaignId = ' + str(maxid))
        connector.commit()
        newAdNsfwMenu(message,maxid)
    else:
        newAdDescriptionMenu(message,maxid)

def newAdNsfwMenu(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('✔️ Yes','🚫 No')
    keyboard.row('❌ Cancel')
    title = bot.send_message(message.chat.id, "Does your advertisement contain *pornographic / NSFW* content?", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=title,maxid=maxid, callback=addNsfw)

def addNsfw(message,maxid):
    # if the description is between 10 and 180 characters
    if(message.text == '✔️ Yes'):
        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET nsfw = 1 WHERE campaignId = ' + str(maxid))
        connector.commit()
        newAdCpcMenu(message,maxid)
    elif(message.text == '🚫 No'):
        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET nsfw = 0 WHERE campaignId = ' + str(maxid))
        connector.commit()
        newAdCpcMenu(message,maxid)      
    else:
        addNsfw(message,maxid)

def newAdGeotargetingMenu(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('✔️ Yes','🚫 No')
    keyboard.row('❌ Cancel')
    title = bot.send_message(message.chat.id, "Do you want to use Geotargeting? 🌍\n\n If enabled, only users from certain countries will see your ad." , parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=title,maxid=maxid, callback=addNsfw)

def addGeotargeting(message,maxid):
    # if the description is between 10 and 180 characters
    if(message.text == '✔️ Yes'):
        newAdGeotargetingMenuAccept(message,maxid)
    elif(message.text == '🚫 No'):
        newAdCpcMenu(message,maxid)      
    else:
        addNsfw(message,maxid)

def newAdGeotargetingMenuAccept(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌ Cancel')   
    title = bot.send_message(message.chat.id, "Enter the two character country code(s) you want to target your ad to, separated by commas: \n\nExample: US, DE, GB, FR \n\nFor a list of countries click here (https://dogeclick.com/countries)." , parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=title,maxid=maxid, callback= addAcceptGeotargeting )

def addAcceptGeotargeting(message,maxid):
    
    #insert into db
    newAdCpcMenu(message,maxid)
    pass
    

def newAdCpcMenu(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    #usare qualche variabile globale cosi se cambi quella cambia pure qui
    keyboard.row(str(slowest)+'DOGE(slowest)',str(faster)+'DOGE(faster)',str(fastest)+'DOGE(fastest)')
    keyboard.row('❌ Cancel')
    title = bot.send_message(message.chat.id, "What is the most you want to pay *per click?* \n\nThe higher your cost per click, the faster people will see your ad. \n\nThe minimum amount is *0.035 DOGE*.\n\nEnter a value in DOGE:", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=title,maxid=maxid, callback=addCpc)

def addCpc(message,maxid):
    # if the description is between 10 and 180 characters
    if(str(message.text) == str(slowest)+'DOGE(slowest)'):
        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET cpc = \'' + str(slowest) + '\' WHERE campaignId = ' + str(maxid))
        connector.commit()
        newDailyBudgetMenu(message,maxid)
    elif(str(message.text) == str(faster)+'DOGE(faster)'):
        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET cpc = \'' + str(faster) + '\' WHERE campaignId = ' + str(maxid))
        connector.commit()
        newDailyBudgetMenu(message,maxid)
    elif(str(message.text) == str(fastest)+'DOGE(fastest)'):
        mycursor = connector.cursor()  
        mycursor.execute('UPDATE adcampaign SET cpc = \'' + str(fastest) + '\' WHERE campaignId = ' + str(maxid))
        connector.commit()
        newDailyBudgetMenu(message,maxid)
    else:
        newAdCpcMenu(message,maxid)

def newDailyBudgetMenu(message,maxid):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    #usare qualche variabile globale cosi se cambi quella cambia pure qui
    keyboard.row('29 DOGE($0.10)','74 DOGE($0.25)')
    keyboard.row('❌ Cancel')
    #usare qualche variabile globale per min amount
    title = bot.send_message(message.chat.id, "How much do you want to spend per day?\n\nThe minimum amount is 0.59 DOGE.\n\nEnter a value in DOGE:", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=title,maxid=maxid, callback=addDailyBudget)

def addDailyBudget(message,maxid):
    showInsertedAd(message,maxid)
    #inserisci nel db
    pass

def showInsertedAd(message,maxid):
    #matita edit, checkmark enabled

    #edit title, edit descript
    #edit url, edit geotag
    #...
    #back, delete
    #new ad, my ads, home

    #after earch press it brings you to the "new+ +Menu"
    #then it says Your ad has been updated.

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

