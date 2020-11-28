#!/usr/bin/python 
import telebot
from block_io import BlockIo
import string
import random
import dbConnector
import validators
from pycoingecko import CoinGeckoAPI

# DB CONNECTOR SINGLETON
connector = dbConnector.connect()

#BLOCK.IO TOKEN
version = 2
block_io = BlockIo('60dc-be33-0b2d-4c44', 'telegrambot', version)

#BOT TOKEN
token = '1315794495:AAHz5CVPLTqUE3OoTFaXe54ZmrMHHZjL1Rk'

def getDogePrice():
    price = CoinGeckoAPI().get_price(ids='dogecoin', vs_currencies='usd')['dogecoin']['usd']
    return price

###CPC
#minimum cpc amount
slowest = 0.0001/getDogePrice()
faster = 0.0005/getDogePrice()
fastest = 0.0015/getDogePrice()
#maximum cpc amount, must be lower or equal to the dayly budgets minimum amount
maxamount = 0.09/getDogePrice() 

###DAILY BUDGET (the number on the left doesn't have to be equal to the number on the right, ONLY CHANGE THE NUMBER ON THE RIGHT!)
#minimum daily budget amount
cents10 = 0.11/getDogePrice()
cents25 = 0.25/getDogePrice()
cents100 = 1/getDogePrice()
cents200 = 2/getDogePrice()
cents500 = 5/getDogePrice()
cents1000 = 10/getDogePrice()
#maximum daily budget amount
cents500000 = 500/getDogePrice()

###COUNTRIES
countries = ["en","it","id","sg","ru","ng","de","vn","nl","ph","in","ve","gb","br","au","fi","fr","jp","no","my","tr","co","ch","ca","mx","ar","ua","es","md","eg","bd","mn","cu","th","it","ir"]

# Create the bot
bot = telebot.TeleBot(token)



# onStart
@bot.message_handler(commands=['start'])
def start_message(message):

    print(message.text.replace('/start ', ''))
    chatId = message.chat.id
    if checkUserId(message.chat.username) == 1:  # if user id is new insert
        print("user inserted")
        userAddress = block_io.get_new_address(label=message.chat.username)
        print(userAddress["data"]["address"])
        insertUser(chatId, userAddress["data"]["address"],message.from_user.language_code, message.chat.username)
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
    elif message.text.lower() == '❌cancel':
        cancelAdMenu(message)
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
    mycursor.execute('UPDATE user SET referral = \"'+ result_str +'\"  WHERE username = \''+ str(message.chat.username)+'\'')
    connector.commit()

def referralMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🖥 Visit sites', '💰 Balance')
    keyboard.add('🙌🏻 Referrals', '⚙ Settings')
    keyboard.add('📊 My ads')

    bot.send_message(message.chat.id,
                    'You have *0* referrals, and earned *0* DOGE. \nTo refer people, send them to: \n\n'+getReferralCode(message.chat.username)+' \n\nYou will earn *15%* of each user\'s earnings from tasks, and *1%* of DOGE they spend on ads.',
                    parse_mode='Markdown', reply_markup=keyboard)

def adsMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ New ad', '📊 My ads')
    keyboard.add('🏠 Menu')

    if checkUserAds(message.chat.username) == 0:
        bot.send_message(message.chat.id, "You don't have any ad campaigns yet.", parse_mode='Markdown',
                     reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "You currently have *" +str(checkUserAds(message.chat.username))+"* Ads", parse_mode='Markdown',
                         reply_markup=keyboard)
        ads = getUserAds(message.chat.username)
        nrAds = checkUserAds(message.chat.username)
        adsString = ""
        print("ads="+str(ads))
        for i in range(int(nrAds)):
                adsString = "*Campaign#"+ str(i) +"* \n\nTitle: *"+str(ads[i][1])+"*\nDescription: "+str(ads[i][2])+\
                "\nURL: "+str(ads[i][8])+"\nStatus: "+str(ads[i][7])+\
                "\nCPC: *"+str(ads[i][5])+" DOGE*\nDaily Budget: *"+str(ads[i][6])+" DOGE*"+\
                "\nClicks: *"+str(ads[i][11])+"* total/ *"+str(ads[i][4])+"* today"
                bot.send_message(message.chat.id, adsString,parse_mode='Markdown',reply_markup=keyboard)
                adsString = ""

def cancelAdMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ New ad', '📊 My ads')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "Your ad has been canceled.", parse_mode='Markdown',reply_markup=keyboard)

def createAdCampaign(message):
    print('created new campaign')
    newAdUrlMenu(message)

def newAdUrlMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')
    url = bot.send_message(message.chat.id, "Enter the URL to send traffic to: \n\nIt should begin with https:// or http://", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, callback=addUrl)

def addUrl(message):
    valid=validators.url(str(message.text))
    if(valid==True):
        newAdTitleMenu(message, str(message.text))
    else:
        newAdUrlMenu(message)
   
def newAdTitleMenu(message,url):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⏭️ Skip','❌Cancel')
    title = bot.send_message(message.chat.id, "Enter a title for your ad: \n\nIt must be between *5* and *80* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url , callback=addTitle)

def addTitle(message,url):
    if(len(str(message.text))>=5 and len(str(message.text))<=80):
        newAdDescriptionMenu(message,url,str(message.text))
    else:
        newAdTitleMenu(message,url)

def newAdDescriptionMenu(message,url,adtitle):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⏭️ Skip','❌Cancel')
    title = bot.send_message(message.chat.id, "Enter a description for your ad:\n\nIt must be between *10* and *180* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, callback=addDescription)

def addDescription(message,url,adtitle):
    if(len(str(message.text))>=10 and len(str(message.text))<=180):
        newAdNsfwMenu(message,url,adtitle,str(message.text))
    else:
        newAdDescriptionMenu(message,url,adtitle)

def newAdNsfwMenu(message,url,adtitle,description):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('✅ Yes','🚫 No')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "Does your advertisement contain *pornographic / NSFW* content?", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, callback=addNsfw)

def addNsfw(message,url,adtitle,description):
    if(message.text == '✅ Yes'):
        newAdGeotargetingMenu(message,url,adtitle,description, 1)
    elif(message.text == '🚫 No'):
        newAdGeotargetingMenu(message,url,adtitle,description, 0)      
    else:
        addNsfw(message,url,adtitle,description)

def newAdGeotargetingMenu(message,url,adtitle,description,nsfw):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('✅ Yes','🚫 No')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "Do you want to use Geotargeting? 🌍\n\n If enabled, only users from certain countries will see your ad." , parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, callback=addGeotargeting)

def addGeotargeting(message,url,adtitle,description,nsfw):
    if(message.text == '✅ Yes'):
        newAdGeotargetingMenuAccept(message,url,adtitle,description,nsfw)
    elif(message.text == '🚫 No'):
        newAdCpcMenu(message,url,adtitle,description,nsfw,'xx')      
    else:
        addGeotargeting(message,url,adtitle,description,nsfw)

def newAdGeotargetingMenuAccept(message,url,adtitle,description,nsfw):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')   
    title = bot.send_message(message.chat.id, "Enter the two character country code(s) you want to target your ad to, separated by commas: \n\nExample: US, DE, GB, FR \n\nFor a list of countries click here (https://dogeclick.com/countries)." , parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw,  callback= addAcceptGeotargeting )

def addAcceptGeotargeting(message,url,adtitle,description,nsfw):
    if(message.text == 'en'):
        newAdGeotargetingMenuAccept(message,url,adtitle,description,nsfw,'en')
    else:
        newAdGeotargetingMenuAccept(message,url,adtitle,description,nsfw)
    
def newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(str(slowest)[0:6]+' DOGE(slowest)',str(faster)[0:6]+' DOGE(faster)',str(fastest)[0:5]+' DOGE(fastest)')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "What is the most you want to pay *per click?* \n\nThe higher your cost per click, the faster people will see your ad. \n\nThe minimum amount is *"+str(slowest)[0:6] +" DOGE*\n\nEnter a value in DOGE:", parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, geotargeting=geotargeting, callback=addCpc)

def addCpc(message,url,adtitle,description,nsfw,geotargeting):
    if(float(str(message.text)[0:6]) >= float(str(slowest)[0:6]) and float(str(message.text)[0:6]) <= float(str(maxamount)[0:6])):
        newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,message.text)
    else:
        newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting)

def newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,cpc):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(str(cents10).split('.')[0]+' DOGE($0.10)',str(cents25).split('.')[0]+' DOGE($0.25)',str(cents100).split('.')[0]+' DOGE($1.00)')
    keyboard.row(str(cents200).split('.')[0]+' DOGE($2.00)',str(cents500).split('.')[0]+' DOGE($5.00)',str(cents1000).split('.')[0]+' DOGE($10.00)')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "How much do you want to spend per day?\n\nThe minimum amount is *"+str(slowest)[0:5]+" DOGE*\n\nEnter a value in DOGE:", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, geotargeting=geotargeting, cpc=cpc, callback=addDailyBudget)

def addDailyBudget(message,url,adtitle,description,nsfw,geotargeting,cpc):
    insertAd(message,url,adtitle,description,nsfw,geotargeting,cpc,str(message.text))

def insertAd(message,url,adtitle,description,nsfw,geotargeting,cpc,dailybudget):
    mycursor = connector.cursor()
    print('Message = '+str(message))
    print('url = '+str(url))
    print('adtitle = '+str(adtitle))
    print('description = '+str(description))
    print('nsfw = '+str(nsfw))
    print('geotargeting = '+str(geotargeting))
    print('cpc = '+str(cpc))
    print('dailybudget = '+str(dailybudget))
    mycursor.execute("INSERT INTO adcampaign(username,url,title,description,nsfw,country,cpc,dailybudget,status,clicks,totalclicks,seconds) VALUES('"+str(message.chat.username)+"','"+str(url)+"','"+str(adtitle)+"','"+str(description)+"','"+str(nsfw)+"','"+str(geotargeting)+"','"+str(cpc)+"','"+str(dailybudget)+"','"+str(1)+"','"+str(0)+"','"+str(0)+"','"+str(10)+"')")
    connector.commit()
    showInsertedAd(message)


def showInsertedAd(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ New ad', '📊 My ads')
    keyboard.add('🏠 Menu')

    mycursor = connector.cursor()
    mycursor.execute("SELECT MAX(campaignId) FROM adcampaign WHERE username = '"+str(message.chat.username)+"'")
    maxid = mycursor.fetchall()

    mycursor = connector.cursor()
    mycursor.execute("SELECT COUNT(campaignId) FROM adcampaign WHERE username = '"+ str(message.chat.username) +"' GROUP BY username")
    countads = mycursor.fetchall()

    mycursor = connector.cursor()
    mycursor.execute("SELECT title, description, url, status, cpc, dailyBudget, totalclicks, clicks  FROM adcampaign WHERE campaignId = '"+str(maxid[0][0])+"'")
    ads = mycursor.fetchall()

    print(str(ads))
    print("showads = "+str(ads))

    adsString = "*Campaign #"+ str(countads[0][0]) +"* \n\nTitle: *"+str(ads[0][0])+"*\nDescription: "+str(ads[0][1])+\
        "\nURL: "+str(ads[0][2])+"\nStatus: "+str(ads[0][3])+\
        "\nCPC: *"+str(ads[0][4])+" DOGE*\nDaily Budget: *"+str(ads[0][5])+" DOGE*"+\
        "\nClicks: *"+str(ads[0][6])+"* total/ *"+str(ads[0][7])+"* today"
    bot.send_message(message.chat.id, adsString,parse_mode='Markdown',reply_markup=keyboard)

    #matita edit, checkmark enabled

    #edit title, edit descript
    #edit url, edit geotag
    #...
    #back, delete
    #new ad, my ads, home

    #after earch press it brings you to the "new+ +Menu"
    #then it says Your ad has been updated.



def balanceMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "Available balance: *"+str(getUserBalance(message.chat.username))+" DOGE*", parse_mode='Markdown',
                     reply_markup=keyboard)

def depositMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "To deposit funds, send at least *1 DOGE* to the following address:\n\n *" + str(getUserAddress(message.chat.username)) + "* \n\n Deposits are not subject to a fee.",
                     parse_mode='Markdown',
                     reply_markup=keyboard)

def withdrawMenu2(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌ Cancel')
    bot.send_message(message.chat.id, "Your balance: *" + str(getUserBalance(message.chat.username)) + " DOGE*\n\nTo withdraw, enter your Dogecoin address:",
                     parse_mode='Markdown',
                     reply_markup=keyboard)

def withdrawMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')

    if(float(getUserBalance(message.chat.username)) < 4):
        bot.send_message(message.chat.id, "Your balance is too small to withdraw.\n\n Available balance: *" + str(getUserBalance(message.chat.username)) + " DOGE* \n\n Minimum withdrawal: *4 DOGE*",
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
    bot.send_message(message.chat.id, "*Click the link below to see your transaction history* \n\n" +str(getUserHistory(message.chat.username))+"", parse_mode='Markdown',
                     reply_markup=keyboard)

def settingsMenu(message):
        nsfw = getNsfw(message.chat.username)
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
            disableNsfw(call.message.chat.username)
        elif call.data == '2':
            answer = 'NSFW Ads have Enabled!'
            enableNsfw(call.message.chat.username)
        elif call.data == '3':
            answer = '⬅ Back to main menu'

        bot.send_message(call.message.chat.id, answer)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)

#inserts new user in the DB
def insertUser(chatId,userAddress,country,username):

    mycursor = connector.cursor()

    sql = "INSERT INTO user (userId, referral, address, taskAlert, seeNsfw, country, username) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (chatId, chatId, userAddress, 1, 1, country, username)
    mycursor.execute(sql, val)
    connector.commit()
    print(mycursor.rowcount, " record inserted.")

#check if user is already inserted in the DB
def checkUserId(username):
    mycursor = connector.cursor()
    mycursor.execute("SELECT * FROM user WHERE username = \'" + str(username)+"\'")
    myresult = mycursor.fetchall()

    if  myresult:
        print("user exists")
        return 0
    else:
        print("user is new")
        return 1

def checkUserAddress(username):
    mycursor = connector.cursor()
    mycursor.execute("SELECT address FROM user WHERE username = \'" + str(username)+"\'")
    myresult = mycursor.fetchall()

    if myresult:
        return myresult[0][0]
    else:
        return 0

#returns the number of ads of a user
def checkUserAds(username):
        mycursor = connector.cursor()
        mycursor.execute("SELECT COUNT(username) FROM adcampaign WHERE username = \'" + str(username)+"\' GROUP BY username")

        myresult = mycursor.fetchall()

        if myresult:
            return myresult[0][0]
        else:
            return 0

def getReferralCode(username):

        mycursor = connector.cursor()
        mycursor.execute('SELECT referral FROM user WHERE username = \'' + str(username)+'\'')
        myresult = mycursor.fetchall()

        if myresult:
            fullReferral = "https://t.me/EarnDogeTodayBot?start="+str(myresult[0][0])
            return fullReferral
        else:
            return 0

def getUserBalance(username):
    balance = block_io.get_address_by(label=username)["data"]["available_balance"]
    print(balance)
    return str(float(balance))

def getUserAddress(username):
    address = checkUserAddress(username)
    print(address)
    return address

def getUserHistory(username):
    address = getUserAddress(username)
    history = "https://sochain.com/address/DOGETEST/"+address
    return history



def getNsfw(username):
    mycursor = connector.cursor()
    mycursor.execute("SELECT seeNsfw FROM user WHERE username = \'" + str(username)+'\'')
    myresult = mycursor.fetchall()

    if myresult:
        return myresult[0][0]
    else:
        return 0

#returns all data of all ads of a user
def getUserAds(username):
        mycursor = connector.cursor()
        mycursor.execute("SELECT * FROM adcampaign WHERE username = \'" + str(username)+'\'')

        myresult = mycursor.fetchall()
        return myresult

def disableNsfw(username):
    mycursor = connector.cursor()
    mycursor.execute("UPDATE user SET seeNsfw = 0 WHERE username = \'" + str(username)+'\'')
    connector.commit()

def enableNsfw(username):
    mycursor = connector.cursor()
    mycursor.execute("UPDATE user SET seeNsfw = 1 WHERE username = \'" + str(username)+'\'')
    connector.commit()

# waitForUserInteraction
bot.polling()

