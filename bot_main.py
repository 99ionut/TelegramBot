#!/usr/bin/python 
import telebot
from block_io import BlockIo
import string
import random
import hashlib
import dbConnector
import validators
import requests
from pycoingecko import CoinGeckoAPI
from datetime import date

# //////////////////////////////// SETTINGS ////////////////////////////////

# DB CONNECTOR SINGLETON
connector = dbConnector.connect()

# BLOCK.IO
mycursor = connector.cursor()
mycursor.execute("SELECT blockIoApi,blockIoSecretPin,blockIoVersion,botToken FROM settings")
botSettings = mycursor.fetchall()
print(str("BOT SETTINGS = "+ str(botSettings)))
blockIoApi = botSettings[0][0]
blockIoSecretPin = botSettings[0][1]
blockIoVersion = botSettings[0][2]
block_io = BlockIo(str(blockIoApi), str(blockIoSecretPin), str(blockIoVersion))

# BOT TOKEN
botToken = botSettings[0][3]
token = str(botToken)

def serverUpdate(request):
    print("ricevuto update")
    print(request.json)

def getDogePrice():
    price = CoinGeckoAPI().get_price(ids='dogecoin', vs_currencies='usd')['dogecoin']['usd']
    return price

# ADMIN LIST (telegram username)
adminlist = ["IonutZuZu", "userTest"]

# WITHDRAW
# minimum withdraw amount (in doge)
minwithdrawamount = 4
# minimum deposit amount (in doge)
mindepositamount = 1

# CPC
# minimum CPC amount
slowest = 0.0001/getDogePrice()
faster = 0.0005/getDogePrice()
fastest = 0.0015/getDogePrice()
# maximum cpc amount, must be lower or equal to the daily budgets min amount
maxamount = 0.10/getDogePrice()


# DAILY BUDGET
# minimum daily budget amount
cents10 = 0.11/getDogePrice()
# daily budget buttons
cents25 = 0.25/getDogePrice()
cents100 = 1/getDogePrice()
cents200 = 2/getDogePrice()
cents500 = 5/getDogePrice()
cents1000 = 10/getDogePrice()
# maximum daily budget amount
cents500000 = 500/getDogePrice()

# COUNTRIES allowed
countries = ["en", "id", "us", "ru", "sg", "de", "ng", "vn", "ph", "in", "nl", "mn", "gb", "br", "ve", "tr", "jp", "fi", 
"my", "eg", "bd", "mm", "fr", "md", "ps", "ua", "ar", "co", "th", "es", "mx", "pk", "it", "ca", "dz", "cu", "ma", "ir", 
"gh", "uz", "hu", "lk", "au", "ec", "pe", "cm", "zm", "sd", "cn", "se", "bj", "ye", "et", "hk", "iq", "ci", "tg", "pl", 
"np", "at", "tw", "za", "ae", "ch", "az", "do", "bg", "ro", "kz", "kr", "pt", "ie", "am", "gr", "bo", "ke", "sk", "mg", 
"ni", "tn", "rs", "by", "cl", "sy", "cz", "af", "bf", "il", "is", "lu", "ao", "cr", "be", "si", "kh", "pa", "jo", "ge", 
"cd", "jm", "hr", "mk", "sn", "kg", "lb", "sr", "tt", "ht", "xk", "ly", "dk", "lt", "mv", "kw", "uy", "al", "gt", "ug", 
"py", "ga", "no", "ml", "zw", "hn", "ba", "bn", "tz", "mz", "cg", "so", "qa", "lv", "me", "nz", "sz", "la", "pr", "tj", 
"cy", "pg", "gn", "bi", "ls", "ee", "ne", "mw", "bw", "mu", "mt", "mp", "to", "rw", "vc", "om", "nc", "ky", "sc", "gi", 
"fj", "cv", "lr", "tc", "gd", "bh", "sl", "bb", "pf", "sm", "er", "xx"]

# //////////////////////////////// COMMANDS ////////////////////////////////
# Create the bot
bot = telebot.TeleBot(token)

# Start command
@bot.message_handler(commands=['start'])
def start_message(message):
    chatId = message.chat.id
    if checkUserId(message.chat.username) == 1:  # if user id is new insert

        print("user inserted")
        userAddress = block_io.get_new_address(label=message.chat.username)
        print(userAddress["data"]["address"])
        insertUser(chatId, userAddress["data"]["address"],message.from_user.language_code, message.chat.username)
        createReferralCode(message)

        referralRecieved = message.text.replace('/start ', '')
        print("referral = "+str(referralRecieved))
        if (referralRecieved == ""): 
            print("no referral inserted")
        else:
            mycursor = connector.cursor()
            mycursor.execute("SELECT username FROM user WHERE referral = \'"+str(referralRecieved)+"\'")
            userReferred = mycursor.fetchall()
            print("USER REFERRED = "+userReferred[0][0])
            if( userReferred[0][0] == ""):
                print("invalid referral")
            else:
                print("VALID referral")
                print("username = "+str(message.chat.username))
                mycursor.execute("UPDATE user SET referredBy = \'" + str(userReferred[0][0]) + "\'  WHERE username = \'" + str(message.chat.username) + "\'")
                connector.commit()

    else:
        print("user not inserted")
        pass
    startMenu(message)


# Menu command
@bot.message_handler(commands=['menu'])
def menu_message(message):
    startMenu(message)


# visit command
@bot.message_handler(commands=['visit'])
def visit_message(message):
    visitSitesMenu(message)


# myads command
@bot.message_handler(commands=['myads'])
def myads_message(message):
    adsMenu(message)


# newad command
@bot.message_handler(commands=['newad'])
def newad_message(message):
    createAdCampaign(message)


# deposit command
@bot.message_handler(commands=['deposit'])
def deposit_message(message):
    depositMenu(message)


# withdraw command
@bot.message_handler(commands=['withdraw'])
def withdraw_message(message):
    withdrawMenu(message)


# history command
@bot.message_handler(commands=['history'])
def history_message(message):
    historyMenu(message)


# referrals command
@bot.message_handler(commands=['referrals'])
def referrals_message(message):
    referralMenu(message)


# cancel command
@bot.message_handler(commands=['cancel'])
def cancel_message(message):
    startMenu(message)


# cancel command
@bot.message_handler(commands=['admin'])
def admin_message(message):
    if(message.chat.username in adminlist):
        print("user is admin")
    else:
        print("user is NOT admin")


# help command
@bot.message_handler(commands=['help'])
def help_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    bot.send_message(message.chat.id,
'This bot was made by DOGE Click (https://dogeclick.com/), a pay to click service that uses cryptocurrency to process payments.\n\n\
To verify that this bot is really ours, visit dogeclick.com (https://dogeclick.com/) and make sure the link on that page brings you to the same bot you are using to read this message.\n\n\
*Any bot that is not listed on that page is NOT affiliated with us.*\n\n\
Using this bot, you can:\n\n\
- Earn Dogecoin by visiting websites.\n\
- Promote your own websites, bots, channels.\n\
- Withdraw your balance at any time, with NO deposit required.\n\n\
Here s how to earn Dogecoin using this bot:\n\n\
*Visit websites:*\n\n\
1. Press 🖥 Visit sites and wait for an ad to show up.\n\
2. Press 🔎 Go to website to visit the site.\n\
3. Stay on the site for the required amount of time to get your reward.\n\n\
Here are all my commands:\n\n\
/menu - Show the main menu\n\
/visit - Earn by clicking links\n\
/myads - Manage your ads\n\
/newad - Create a new ad\n\
/balance - Show your balance\n\
/deposit - Deposit funds\n\
/withdraw - Withdraw funds\n\
/history - Show transactions\n\
/referrals - Show your referrals\n\
/help - Show help\n\
/cancel - Cancel current action\n\n\
Visit our FAQ (https://dogeclick.com/faq) page for more info.\
Join our news channel at @DOGEClickUpdates 📢\
For technical support, message @DOGEClickSupport 📞',
            parse_mode='Markdown', reply_markup=keyboard)


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

# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
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


# //////////////////////////////// MENUS ////////////////////////////////
# Visit Sites Menu
def visitSitesMenu(message):
    markup = telebot.types.InlineKeyboardMarkup()

    print("USER THAT WANTS AN AD = "+str(message.chat.username))
    userWants = str(message.chat.username)

    mycursor = connector.cursor()
    mycursor.execute("SELECT lastAd FROM user WHERE username = \'"+userWants+"\'")
    lastAd = mycursor.fetchall()
    print("LAST AD = "+str(lastAd[0][0]))

    if(str(lastAd[0][0]) == "-1"): #if there is no last ad give the user a new one
        mycursor = connector.cursor() #expire previous links
        mycursor.execute("DELETE FROM link WHERE username = \'" + userWants + "\'")
        connector.commit()
        print("expired previous links")

        ad = getRandomAd(message)
        while (ad == None):
            ad = getRandomAd(message)

        print("USER RECIEVED AD = "+str(ad[0]))
        userGot = str(ad[0])

        mycursor = connector.cursor()
        mycursor.execute('UPDATE user SET lastAd = \"' + userGot + '\"  WHERE username = \'' + userWants + '\'')
        connector.commit()

        m = hashlib.md5()
        m.update(userWants.encode('utf-8') + userGot.encode('utf-8'))
        customLink = str(int(m.hexdigest(), 16))[0:12]
        print("CUSTOM LINK = "+customLink)
        print("added new valid link")
                                  #also delete all if skip
        mycursor = connector.cursor() #delete after the user visits the ad, use the unique value in the link to see the DB to see what user has to pay who
        mycursor.execute("INSERT INTO link VALUES ( \'" + customLink + "\',\'" + userWants + "\',\'" + userGot + "\' )")
        connector.commit()

        markup.add(telebot.types.InlineKeyboardButton(
            text='🔎 Go to website', url=str(ad[8]), callback_data="goToWebsite"))
        markup.add(telebot.types.InlineKeyboardButton(
            text='🛑 Report', callback_data="reportAd"), telebot.types.InlineKeyboardButton(
            text='⏭ Skip', callback_data="skipAd"))
        bot.send_message(
        message.chat.id, text="custom link = http://localhost/earndogetoday/visit.php?ad="+ customLink +"\n\n"+str(ad[1])+"\n\n"+str(ad[2])+"\n\n--------------------- \nPress the \"Visit website\" button to earn DOGE.\nYou will be redirected to a third party site." , reply_markup=markup)

    else: #if there is a last ad show that one
        print("last ad exists")
        mycursor = connector.cursor()
        mycursor.execute("SELECT * FROM adcampaign WHERE campaignId = \'"+str(lastAd[0][0])+"\'")
        ad = mycursor.fetchall()
        ad = ad[0]
        print("LAST AD = "+str(ad))

        mycursor = connector.cursor()
        mycursor.execute("SELECT customLink FROM link WHERE username = \'"+userWants+"\'")
        customLink = mycursor.fetchall()
        print("LAST CUSTOM LINK = "+str(customLink[0][0]))
        customLink = str(customLink[0][0])
       
        markup.add(telebot.types.InlineKeyboardButton(
            text='🔎 Go to website', url=str(ad[8]), callback_data="goToWebsite"))
        markup.add(telebot.types.InlineKeyboardButton(
            text='🛑 Report', callback_data="reportAd"), telebot.types.InlineKeyboardButton(
            text='⏭ Skip', callback_data="skipAd"))
        bot.send_message(
        message.chat.id, text="custom link = http://localhost/earndogetoday/visit.php?ad="+ customLink +"\n\n"+str(ad[1])+"\n\n"+str(ad[2])+"\n\n--------------------- \nPress the \"Visit website\" button to earn DOGE.\nYou will be redirected to a third party site." , reply_markup=markup)


# return an ad
def getRandomAd(message):
    # 50% to get a high paying ad (fasters), 30% to get a medium paying ad (faster), 20% to get a low paying ad(slow)
    randomPaying = (random.randint(0, 9))
    if (randomPaying >= 0 and randomPaying <= 4):
        # HIGH PAYING
        # 30% to 0-10s, 25% to 10-20s, 20% to 20-30s, 15% to 30-40s, 5% to 40-50s, 5% to 50-60s. 
        randomSeconds = (random.randint(0, 99))  # fastest paying and <= 10 s
        if(randomSeconds >= 0 and randomSeconds <= 29):  # fastest paying and <= 10 s
            seconds = 10
        elif(randomSeconds >= 30 and randomSeconds <= 54):  # fastest paying and <= 20 s
            seconds = 20
        elif(randomSeconds >= 55 and randomSeconds <= 74):  # fastest paying and <= 30 s
            seconds = 30
        elif(randomSeconds >= 75 and randomSeconds <= 89):  # fastest paying and <= 40 s
            seconds = 40
        elif(randomSeconds >= 90 and randomSeconds <= 94):  # fastest paying and <= 50 s
            seconds = 50
        elif(randomSeconds >= 95 and randomSeconds <= 99):  # fastest paying and <= 60 s
            seconds = 60
        else:
            getRandomAd(message)

        mycursor = connector.cursor()
        mycursor.execute("SELECT * FROM adcampaign WHERE speed = \'fastest\' and seconds > \'"+str(seconds-10)+"\' and seconds <= \'"+str(seconds)+"\' ")
        ad = mycursor.fetchall()

        if(str(ad) == "[]"):
            getRandomAd(message)

        else:
            print("SELECT * FROM adcampaign WHERE speed = \'fastest\' and seconds > \'"+str(seconds-10)+"\' and seconds <= \'"+str(seconds)+"\' ")
            print("FASTEST")
            print("seconds = "+str(seconds))

            adnumber = 0
            for i in ad:
                # print("adNumber = "+str(adnumber)+" "+str(ad[adnumber]))
                adnumber = adnumber + 1

            randomAdNumber = (random.randint(0, adnumber-1))
            print("ad selected = "+str(ad[randomAdNumber]))
            return ad[randomAdNumber]

    elif (randomPaying >= 5 and randomPaying <= 7):
        # MEDIUM PAYING
        # 30% to 0-10s, 25% to 10-20s, 20% to 20-30s, 15% to 30-40s, 5% to 40-50s, 5% to 50-60s. 
        randomSeconds = (random.randint(0, 99))
        if(randomSeconds >= 0 and randomSeconds <= 29):  # faster paying and <= 10 s
            seconds = 10
        elif(randomSeconds >= 30 and randomSeconds <= 54):  # faster paying and <= 20 s
            seconds = 20
        elif(randomSeconds >= 55 and randomSeconds <= 74):  # faster paying and <= 30 s
            seconds = 30
        elif(randomSeconds >= 75 and randomSeconds <= 89):  # faster paying and <= 40 s
            seconds = 40
        elif(randomSeconds >= 90 and randomSeconds <= 94):  # faster paying and <= 50 s
            seconds = 50
        elif(randomSeconds >= 95 and randomSeconds <= 99):  # faster paying and <= 60 s
            seconds = 60
        else:
            getRandomAd(message)

        mycursor = connector.cursor()
        mycursor.execute("SELECT * FROM adcampaign WHERE speed = \'faster\' and seconds > \'"+str(seconds-10)+"\' and seconds <= \'"+str(seconds)+"\' ")
        ad = mycursor.fetchall()

        if(str(ad) == "[]"):
            getRandomAd(message)

        else:
            print("SELECT * FROM adcampaign WHERE speed = \'faster\' and seconds > \'"+str(seconds-10)+"\' and seconds <= \'"+str(seconds)+"\' ")
            print("FASTER")
            print("seconds = "+str(seconds))

            adnumber = 0
            for i in ad:
                # print("adNumber = "+str(adnumber)+" "+str(ad[adnumber]))
                adnumber = adnumber + 1

            randomAdNumber = (random.randint(0, adnumber-1))
            print("ad selected = "+str(ad[randomAdNumber]))
            return ad[randomAdNumber]

    elif (randomPaying >= 8 and randomPaying <= 9):
        # LOW PAYING
        # 30% to 0-10s, 25% to 10-20s, 20% to 20-30s, 15% to 30-40s, 5% to 40-50s, 5% to 50-60s.
        randomSeconds = (random.randint(0, 99))
        if(randomSeconds >= 0 and randomSeconds <= 29):  # slowest paying and <= 10 s
            seconds = 10
        elif(randomSeconds >= 30 and randomSeconds <= 54):  # slowest paying and <= 20 s
            seconds = 20
        elif(randomSeconds >= 55 and randomSeconds <= 74):  # slowest paying and <= 30 s
            seconds = 30
        elif(randomSeconds >= 75 and randomSeconds <= 89):  # slowest paying and <= 40 s
            seconds = 40
        elif(randomSeconds >= 90 and randomSeconds <= 94):  # slowest paying and <= 50 s
            seconds = 50
        elif(randomSeconds >= 95 and randomSeconds <= 99):  # slowest paying and <= 60 s
            seconds = 60
            getRandomAd(message)

        mycursor = connector.cursor()
        mycursor.execute("SELECT * FROM adcampaign WHERE speed = \'slowest\' and seconds > \'"+str(seconds-10)+"\' and seconds <= \'"+str(seconds)+"\' ")
        ad = mycursor.fetchall()

        if(str(ad) == "[]"):
            getRandomAd(message)

        else:
            print("SELECT * FROM adcampaign WHERE speed = \'slowest\' and seconds > \'"+str(seconds-10)+"\' and seconds <= \'"+str(seconds)+"\' ")
            print("SLOW")
            print("seconds = "+str(seconds))

            adnumber = 0
            for i in ad:
                # print("adNumber = "+str(adnumber)+" "+str(ad[adnumber]))
                adnumber = adnumber + 1

            randomAdNumber = (random.randint(0, adnumber-1))
            print("ad selected = "+str(ad[randomAdNumber]))
            return ad[randomAdNumber]
    # if the first time you dont find an ad with the random settings, repeat with different settings until you find one
    else:
        getRandomAd(message)


def startMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🖥 Visit sites', '💰 Balance')
    keyboard.add('🙌🏻 Referrals', '⚙ Settings')
    keyboard.add('📊 My ads')
    bot.send_message(message.chat.id,
                     '🔥 Welcome to *EARN DOGE Today* Bot! 🔥 \n\nThis bot lets you earn Dogecoin by completing simple tasks. \n\nPress 🖥 *Visit sites* to earn by clicking links Press \n\nYou can also create your own ads with /newad. Use the /help command for more info.',
                     parse_mode='Markdown', reply_markup=keyboard)


def createReferralCode(message):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(8))

    #m = hashlib.md5()
    #m.update(str(message.chat.username).encode('utf-8'))
    #result_str = str(int(m.hexdigest(), 16))[0:8] #todo test thi

    mycursor = connector.cursor()
    mycursor.execute('UPDATE user SET referral = \"' + result_str + '\"  WHERE username = \'' + str(message.chat.username) + '\'')
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
    markupEnabled = telebot.types.InlineKeyboardMarkup()
    markupDisabled = telebot.types.InlineKeyboardMarkup()

    keyboard.row('➕ New ad', '📊 My ads')
    keyboard.add('🏠 Menu')

    markupEnabled.add(telebot.types.InlineKeyboardButton(
                text='✏️ Edit', callback_data="editAd"), telebot.types.InlineKeyboardButton(
                text='✅ Enable', callback_data="changeAdStateEnabled"))

    markupDisabled.add(telebot.types.InlineKeyboardButton(
                    text='✏️ Edit', callback_data="editAd"), telebot.types.InlineKeyboardButton(
                    text='🚫 Disable', callback_data="changeAdStateDisabled"))
    # if the user DESN'T have any ads
    if checkUserAds(message.chat.username) == 0:
        bot.send_message(message.chat.id, "You don't have any ad campaigns yet.", parse_mode='Markdown',
                     reply_markup=keyboard)
    # if the user HAS ads show all of them
    else:
        bot.send_message(message.chat.id, "You currently have *" +str(checkUserAds(message.chat.username))+"* Ads", parse_mode='Markdown',
                         reply_markup=keyboard)
        ads = getUserAds(message.chat.username)
        nrAds = checkUserAds(message.chat.username)
        adsString = ""
        print("ads="+str(ads))
        for i in range(int(nrAds)):
                adsString = "*Campaign#"+ str(i+1) +"* \n\nTitle: *"+str(ads[i][1])+"*\nDescription: "+str(ads[i][2])+\
                "\nURL: "+str(ads[i][8])+"\nStatus: "
                if(str(ads[i][7])=="1"):
                    adsString = adsString + "* Enabled* ✅ "
                    enabled = 1
                elif(str(ads[i][7])=="0"):
                    adsString = adsString + "*Disabled* 🚫 " 
                    enabled = 0        
                else:
                    adsString = adsString + "*UNKNOWN* "

                adsString = adsString + "\nCPC: *"+str(ads[i][5])+" DOGE*\nDaily Budget: *"+str(ads[i][6])+" DOGE*"+\
                "\nClicks: *"+str(ads[i][11])+"* total/ *"+str(ads[i][4])+"* today"

                if(enabled == 1):
                    bot.send_message(message.chat.id, adsString,parse_mode='Markdown',reply_markup=markupDisabled)
                elif(enabled == 0):
                    bot.send_message(message.chat.id, adsString,parse_mode='Markdown',reply_markup=markupEnabled)
               
                adsString = ""

# ///////////////////////// CREATE NEW AD ///////////////////////
def cancelAdMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ New ad', '📊 My ads')
    keyboard.add('🏠 Menu')
    bot.send_message(message.chat.id, "Your ad has been canceled.", parse_mode='Markdown', reply_markup=keyboard)


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
    if(str(message.text) == '❌Cancel'):
        cancelAdMenu(message)
    else:
        try:
            if requests.get(str(message.text)).status_code == 200:
                valid = validators.url(str(message.text))
                if(valid == True):
                    newAdTitleMenu(message, str(message.text))
                elif(str(message.text) == '❌Cancel'):
                    cancelAdMenu(message)
                else:
                    newAdUrlMenu(message)
            else:
                newAdUrlMenu(message)
        except:
            newAdUrlMenu(message)
# todo if url has weird characters it breakes because of markdown

def newAdTitleMenu(message, url):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⏭️ Skip', '❌Cancel')
    title = bot.send_message(message.chat.id, "Enter a title for your ad: \n\nIt must be between *5* and *80* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, callback=addTitle)


def addTitle(message, url):
    if(str(message.text) == '❌Cancel'):
        cancelAdMenu(message)
    elif(len(str(message.text)) >= 5 and len(str(message.text)) <= 80):
        newAdDescriptionMenu(message, url, str(message.text))
    else:
        newAdTitleMenu(message, url)


def newAdDescriptionMenu(message, url, adtitle):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⏭️ Skip', '❌Cancel')
    title = bot.send_message(message.chat.id, "Enter a description for your ad:\n\nIt must be between *10* and *180* characters. \n\nPress \"Skip\" to use the site's title for this ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, callback=addDescription)


def addDescription(message, url, adtitle):
    if(str(message.text) == '❌Cancel'):
        cancelAdMenu(message)
    elif(len(str(message.text)) >= 10 and len(str(message.text)) <= 180):
        newAdNsfwMenu(message, url, adtitle, str(message.text))
    else:
        newAdDescriptionMenu(message, url, adtitle)


def newAdNsfwMenu(message, url, adtitle, description):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('✅ Yes', '🚫 No')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "Does your advertisement contain *pornographic / NSFW* content?", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, callback=addNsfw)


def addNsfw(message, url, adtitle, description):
    if(str(message.text) == '❌Cancel'):
        cancelAdMenu(message)
    elif(message.text == '✅ Yes'):
        newAdGeotargetingMenu(message, url, adtitle, description, 1)
    elif(message.text == '🚫 No'):
        newAdGeotargetingMenu(message, url, adtitle, description, 0)
    else:
        newAdNsfwMenu(message, url, adtitle, description)


def newAdGeotargetingMenu(message, url, adtitle, description, nsfw):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('✅ Yes', '🚫 No')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "Do you want to use Geotargeting? 🌍\n\n If enabled, only users from certain countries will see your ad.", parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, callback=addGeotargeting)


def addGeotargeting(message, url, adtitle, description, nsfw):
    if(str(message.text) == '❌Cancel'):
        cancelAdMenu(message)
    elif(message.text == '✅ Yes'):
        newAdGeotargetingMenuAccept(message, url, adtitle, description, nsfw)
    elif(message.text == '🚫 No'):
        newAdSecondsMenu(message, url, adtitle, description, nsfw, 'xx') # xx means no country selected
    else:
        newAdGeotargetingMenu(message, url, adtitle, description, nsfw)

def newAdGeotargetingMenuAccept(message, url, adtitle, description, nsfw):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')   
    title = bot.send_message(message.chat.id, "Enter the two character country code(s) you want to target your ad to, separated by commas: \n\nExample: US, DE, GB, FR \n\nFor a list of countries click here (https://dogeclick.com/countries)." , parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw,  callback= addAcceptGeotargeting )

def addAcceptGeotargeting(message,url,adtitle,description,nsfw):
    if(str(message.text) == '❌Cancel'):
        cancelAdMenu(message)
        pass

    result = [x.strip() for x in message.text.split(',')]
    result = [x.lower() for x in result]
    print("user inserted countries = " + str(result))
    print("count 0 = " + str(result[0]))
    usercountries = ""
    for i in result:
            if i in countries:
                print("result in = "+ i)
                usercountries = usercountries + str(i)+","
            else:
                print("result not = "+ i)

    if(usercountries == ""):
        newAdGeotargetingMenuAccept(message,url,adtitle,description,nsfw)
    else:
        newAdSecondsMenu(message,url,adtitle,description,nsfw,usercountries)
    
def newAdSecondsMenu(message,url,adtitle,description,nsfw,geotargeting): #todo sites like btc.org break
    try:
        r = requests.get(url)
        #print("HEADERS = "+str(r.headers))

        if ("X-Frame-Options" in str(r.headers)):
            print("can't use xframe")
            newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting,str(-1)) # default seconds
        else:
            print("xframe allowed")
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('✅ Yes','🚫 No')
            keyboard.row('❌Cancel') 
            bot.send_message(message.chat.id, "Your link URL supports *visitor timing.* ⏲ \n\nRequire visitors to stay on the page for at least *10 seconds?*",parse_mode='Markdown',reply_markup=keyboard)
            bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, geotargeting=geotargeting, callback=newAdSeconds)
    except ValueError:
        newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting,str(10))

def newAdSeconds(message,url,adtitle,description,nsfw,geotargeting):
    if(str(message.text)=='❌Cancel'):
        cancelAdMenu(message)
    elif(message.text == '✅ Yes'):
        newAdSecondsMenuAccept(message,url,adtitle,description,nsfw,geotargeting)
    elif(message.text == '🚫 No'):
        newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting,str(-1))    # default seconds  
    else:
        newAdSecondsMenu(message,url,adtitle,description,nsfw,geotargeting)
    
def newAdSecondsMenuAccept(message,url,adtitle,description,nsfw,geotargeting):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')   
    title = bot.send_message(message.chat.id, "How many *seconds* are visitors required to *stay on the page?*\n\n Using a higher value results in a lower display rank, meaning it will take longer for people to see your ad. \n\nEnter a value between *10* and *60*:" , parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, geotargeting=geotargeting,  callback= addAcceptSeconds )


def addAcceptSeconds(message,url,adtitle,description,nsfw,geotargeting):
    try:  
        if(str(message.text)=='❌Cancel'):
            cancelAdMenu(message)
        elif(int(message.text)>=10 and int(message.text)<=60):
            newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting,str(message.text))
        else:
            newAdSecondsMenuAccept(message,url,adtitle,description,nsfw,geotargeting)
    except ValueError:
        newAdSecondsMenuAccept(message,url,adtitle,description,nsfw,geotargeting)       

def newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting,seconds):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(str(slowest)[0:6]+' DOGE(slowest)',str(faster)[0:6]+' DOGE(faster)',str(fastest)[0:6]+' DOGE(fastest)')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "What is the most you want to pay *per click?* \n\nThe higher your cost per click, the faster people will see your ad. \n\nThe minimum amount is *"+str(slowest)[0:6] +" DOGE*\n\nEnter a value in DOGE:", parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, geotargeting=geotargeting, seconds=seconds, callback=addCpc)

def addCpc(message,url,adtitle,description,nsfw,geotargeting,seconds):
        try:        
            if(str(message.text)=='❌Cancel'):
                cancelAdMenu(message)
            elif(float(str(message.text)[0:6]) >= float(str(slowest)[0:6]) and float(str(message.text)[0:6]) < float(str(faster)[0:6])):
                speed = "slowest"
                newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,seconds,message.text,speed)
            elif(float(str(message.text)[0:6]) >= float(str(faster)[0:6]) and float(str(message.text)[0:6]) < float(str(fastest)[0:6])):
                speed = "faster"
                newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,seconds,message.text,speed)
            elif(float(str(message.text)[0:6]) >= float(str(fastest)[0:6]) and float(str(message.text)[0:6]) <= float(str(maxamount)[0:6])):
                speed = "fastest"
                newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,seconds,message.text,speed)        
            else:
                newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting,seconds)
        except ValueError:
            newAdCpcMenu(message,url,adtitle,description,nsfw,geotargeting,seconds)

def newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,seconds,cpc,speed):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(str(cents10).split('.')[0]+' DOGE($0.10)',str(cents25).split('.')[0]+' DOGE($0.25)',str(cents100).split('.')[0]+' DOGE($1.00)')
    keyboard.row(str(cents200).split('.')[0]+' DOGE($2.00)',str(cents500).split('.')[0]+' DOGE($5.00)',str(cents1000).split('.')[0]+' DOGE($10.00)')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "How much do you want to spend per day?\n\nThe minimum amount is *"+str(slowest)[0:5]+" DOGE*\n\nEnter a value in DOGE:", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, url=url, adtitle=adtitle, description=description, nsfw=nsfw, geotargeting=geotargeting, seconds=seconds, cpc=cpc, speed=speed, callback=addDailyBudget)

def addDailyBudget(message,url,adtitle,description,nsfw,geotargeting,seconds,cpc,speed):
        try:
            if(str(message.text)=='❌Cancel'):
                cancelAdMenu(message)
            elif(float(str(message.text).split(' ')[0]) >= float(cents10) and float(str(message.text).split(' ')[0]) <= float(cents500000)):
                insertAd(message,url,adtitle,description,nsfw,geotargeting,seconds,cpc,speed,str(message.text))        
            else:
                newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,seconds,cpc,speed)
        except ValueError:
             newDailyBudgetMenu(message,url,adtitle,description,nsfw,geotargeting,seconds,cpc,speed)

def insertAd(message,url,adtitle,description,nsfw,geotargeting,seconds,cpc,speed,dailybudget):
    mycursor = connector.cursor()
    #print('Message = '+str(message))
    print('url = '+str(url))
    print('adtitle = '+str(adtitle))
    print('description = '+str(description))
    print('nsfw = '+str(nsfw))
    print('geotargeting = '+str(geotargeting))
    print('cpc = '+str(cpc))
    print('dailybudget = '+str(dailybudget))
    print('seconds = '+str(seconds))
    print('speed = '+str(speed))
    mycursor.execute("INSERT INTO adcampaign(username,url,title,description,nsfw,country,cpc,dailybudget,status,clicks,totalclicks,seconds,dateAdded,speed) VALUES('"+str(message.chat.username)+"','"+str(url)+"','"+str(adtitle)+"','"+str(description)+"','"+str(nsfw)+"','"+str(geotargeting)+"','"+str(cpc)+"','"+str(dailybudget)+"','"+str(1)+"','"+str(0)+"','"+str(0)+"','"+str(seconds)+"','"+str(date.today().year)+"/"+str(date.today().month)+"/"+str(date.today().day)+"','"+str(speed)+"')")
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


# ///////////////////////// MENUS ////////////////////////

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
    bot.send_message(message.chat.id, "To deposit funds, send at least *"+str(mindepositamount) +" DOGE* to the following address:\n\n *" + str(getUserAddress(message.chat.username)) + "* \n\n Deposits are not subject to a fee.",
                     parse_mode='Markdown',
                     reply_markup=keyboard)

# ///////////////// WITHDRAW
def withdrawMenu2(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌ Cancel')
    bot.send_message(message.chat.id, "Your balance: *" + str(getUserBalance(message.chat.username)) + " DOGE*\n\nTo withdraw, enter your Dogecoin address:",
                     parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, callback=withdrawAddress)

def withdrawAddress(message):
    print(message.text)
    validate = block_io.is_valid_address(address=message.text) #must address be on the same network (Doge testnet or Doge official ecc..)
    print(validate["data"]["is_valid"]) 
    if(str(validate["data"]["is_valid"]) == "True"): #todo inputs break on special characters like ()'ecc.. add try catch everywhere?
        print("ok withdraw")
        withdrawAddressConfirm(message)
    else:     
        print("invalid withdraw")
        withdrawMenu2(message)

def withdrawAddressConfirm(message):
    address = message
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌ Cancel')
    bot.send_message(message.chat.id, "Enter the amount to withdraw: \n\n Minimum: *" + str(minwithdrawamount) +" DOGE*",
                     parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, address=address, callback=withdrawAddressAmount)

def withdrawAddressAmount(message,address):
    amount = message
    print("amount to withdraw = "+str(amount.text))
    print("address to withdraw = "+str(address.text))
    userBalance = getUserBalance(amount.chat.username)
    print("user balance = "+str(userBalance))
    if( float(amount.text) >= float(minwithdrawamount) and float(amount.text) <= float(userBalance) ):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('✅ Confirm','❌ Cancel')
        bot.send_message(message.chat.id, "Are you sure you want to send *"+ str(amount.text) + " DOGE* to *"+ str(address.text) +"* ? \n\nYou will be charged a blockchain fee of 0.056 DOGE.",
                     parse_mode='Markdown',
                     reply_markup=keyboard)
        bot.register_next_step_handler(message=message, amount = amount, address = address, callback=withdrawAddressSend)
    else:
        withdrawAddressConfirm(address)

def withdrawAddressSend(message,amount,address):
    if(str(message.text)=='❌ Cancel'):
        cancelWithdrawMenu(message) 
    elif(str(message.text)=='✅ Confirm'):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('➕ Deposit', '💵 Withdraw')
        keyboard.add('💰 Balance', '🕑 History')
        keyboard.add('🏠 Menu')
        title = bot.send_message(message.chat.id, "✅ Your withdrawal has been requested!\n\nUse the /history command to view your transaction.", parse_mode='Markdown',reply_markup=keyboard)  
    
    else:
        cancelWithdrawMenu(message) 

#todo max amount of ads a day
#todo max amount of high paying ads

def withdrawMenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('➕ Deposit', '💵 Withdraw')
    keyboard.add('💰 Balance', '🕑 History')
    keyboard.add('🏠 Menu')

    if(float(getUserBalance(message.chat.username)) < minwithdrawamount):
        bot.send_message(message.chat.id, "Your balance is too small to withdraw.\n\n Available balance: *" + str(getUserBalance(message.chat.username)) + " DOGE* \n\n Minimum withdrawal: *"+str(minwithdrawamount) +" DOGE*",
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

# \\\\\\\\\\\\\ END WITHDRAW

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
            text='❌ Disable NSFW Advertisments', callback_data="disableNSFW"))
            markup.add(telebot.types.InlineKeyboardButton(
            text='⬅ Back', callback_data="goBack"))
        else:
            markup.add(telebot.types.InlineKeyboardButton(
            text='✅ Enable NSFW Advertisments', callback_data="enableNSFW"))
            markup.add(telebot.types.InlineKeyboardButton(
            text='⬅ Back', callback_data="goBack"))

        if nsfw == 1:
            bot.send_message(
            message.chat.id, text="NSFW/pornographic Ads are currently ✅ *Enabled*", reply_markup=markup, parse_mode='Markdown')
        else:
            bot.send_message(
            message.chat.id, text="NSFW/pornographic Ads are currently ❌ *Disabled*", reply_markup=markup, parse_mode='Markdown')

# //////////////////////// EDIT AD AFTER CREATION /////////////////////////////////

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        #bot.answer_callback_query(callback_query_id=call.id, text='Settings Saved!')
        if call.data == 'disableNSFW':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id) 
            bot.send_message(call.message.chat.id, "NSFW Advertisments have been ❌ *Disabled*!",parse_mode='Markdown',reply_markup=keyboard)
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET seeNsfw = 0 WHERE username = \'" + str(call.message.chat.username)+'\'')
            connector.commit()
        elif call.data == 'enableNSFW':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, "NSFW Advertisments have been ✅ *Enabled*!",parse_mode='Markdown',reply_markup=keyboard)
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET seeNsfw = 1 WHERE username = \'" + str(call.message.chat.username)+'\'')
            connector.commit()
        elif call.data == 'skipAd':
            #bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  #deletes reply markup keyboard
            bot.send_message(call.message.chat.id, "Skipping Task...",parse_mode='Markdown',reply_markup=keyboard)           
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET lastAd = -1 WHERE username = \'" + str(call.message.chat.username)+'\'')
            connector.commit()
            visitSitesMenu(call.message)
            print("AD SKIPPED")
        elif call.data == 'reportAd':
            #todo nrOfTimesReported in db for each ad an then you can see the most reported. If the customer support says its allowed set the nr to 0, if not remove the ad.
            #BASED ON THE CUSTOM URL which redirects the user to earndogetoday.com/visit/customurl which is created with the adid+url+userid, which is passed in the "call" object
            print(call)
            mycursor = connector.cursor()
            mycursor.execute("SELECT campaignId FROM link WHERE username = \'" + str(call.message.chat.username) +"\'")
            reportedAd = mycursor.fetchall()
            reportedAd = reportedAd[0][0]
            print("reported Ad = "+str(reportedAd[0][0]))
            mycursor.execute("UPDATE adcampaign SET reports = reports+1 WHERE campaignId = \'" + str(reportedAd)+"\'")
            connector.commit()

            print("AD REPORTED")
        elif call.data == 'goToWebsite':
            print("goToWebsite")
        elif call.data == 'changeAdStateEnabled':

            print("changeAdStateEnabled")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))

            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET status = 1 WHERE campaignId = \'" + str(userAd)+'\'')
            connector.commit()

            newMessage = str(call.message.text).replace('Disabled 🚫','Enabled ✅')
            newMessage = newMessage.replace('Campaign#','*Campaign#')
            newMessage = newMessage.replace('Title:','*Title:*')
            newMessage = newMessage.replace('Description:','*Description:')
            newMessage = newMessage.replace('Status:','Status:*')
            newMessage = newMessage.replace('CPC:','*CPC:*')
            newMessage = newMessage.replace('Daily Budget:','*Daily Budget:*')
            newMessage = newMessage.replace('Clicks:','*Clicks:*')
            newMessage = newMessage.replace('total/','*total/*')
            newMessage = newMessage.replace('today','*today')
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=newMessage, parse_mode='Markdown')

            editKeyboard = telebot.types.InlineKeyboardMarkup()
            editKeyboard.add(telebot.types.InlineKeyboardButton(
            text='✏️ Edit', callback_data="editAd"), telebot.types.InlineKeyboardButton(
            text='🚫 Disable', callback_data="changeAdStateDisabled"))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=editKeyboard)
            
        elif call.data == 'changeAdStateDisabled':      
                        
            print("changeAdStateDisabled")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
        
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET status = 0 WHERE campaignId = \'" + str(userAd)+'\'')
            connector.commit()

            newMessage = str(call.message.text).replace('Enabled ✅','Disabled 🚫')
            newMessage = newMessage.replace('Campaign#','*Campaign#')
            newMessage = newMessage.replace('Title:','*Title:*')
            newMessage = newMessage.replace('Description:','*Description:')
            newMessage = newMessage.replace('Status:','Status:*')
            newMessage = newMessage.replace('CPC:','*CPC:*')
            newMessage = newMessage.replace('Daily Budget:','*Daily Budget:*')
            newMessage = newMessage.replace('Clicks:','*Clicks:*')
            newMessage = newMessage.replace('total/','*total/*')
            newMessage = newMessage.replace('today','*today')
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=newMessage, parse_mode='Markdown')

            editKeyboard = telebot.types.InlineKeyboardMarkup()
            editKeyboard.add(telebot.types.InlineKeyboardButton(
            text='✏️ Edit', callback_data="editAd"), telebot.types.InlineKeyboardButton(
            text='✅ Enable', callback_data="changeAdStateEnabled"))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=editKeyboard)
            
        elif call.data == 'editAd':

            editKeyboard = telebot.types.InlineKeyboardMarkup()
            editKeyboard.add(telebot.types.InlineKeyboardButton(
            text='Edit Title', callback_data="editAdTitle"), telebot.types.InlineKeyboardButton(
            text='Edit Description', callback_data="editAdDescription"))
            editKeyboard.add(telebot.types.InlineKeyboardButton(
            text='Edit URL', callback_data="editAdUrl"), telebot.types.InlineKeyboardButton(
            text='Geotargeting', callback_data="editAdGeotargeting"))
            editKeyboard.add(telebot.types.InlineKeyboardButton(
            text='Edit CPC', callback_data="editAdCpc"), telebot.types.InlineKeyboardButton(
            text='Edit Budget', callback_data="editAdBudget"))
            editKeyboard.add(telebot.types.InlineKeyboardButton(
            text='⬅️ Back', callback_data="goAdBack"), telebot.types.InlineKeyboardButton(
            text='🗑️ Delete', callback_data="deleteAd"))

            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("Message ID = "+str(call.message.message_id))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=editKeyboard)
            
        elif call.data == 'editAdTitle':
            print("EDIT AD TITLE")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
            editAdTitleMenu(call.message, userAd)

        elif call.data == 'editAdDescription':
            print("EDIT AD Description")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
            editAdDescriptionMenu(call.message, userAd)

        elif call.data == 'editAdUrl':
            print("EDIT AD Url")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
            editAdUrlMenu(call.message, userAd)

        elif call.data == 'editAdGeotargeting':
            print("EDIT AD Geotargeting")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
            editAdGeotagetingMenu(call.message, userAd)

        elif call.data == 'editAdCpc':
            print("EDIT AD CPC")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
            editAdCpcMenu(call.message, userAd)

        elif call.data == 'editAdBudget':
            print("EDIT AD Budget")
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
            editAdBudgetMenu(call.message, userAd)

        elif call.data == 'goAdBack':
            
            print(call.message)
            if (str(call.message).find('Enabled ✅') == -1):
                editKeyboard = telebot.types.InlineKeyboardMarkup()
                editKeyboard.add(telebot.types.InlineKeyboardButton(
                text='✏️ Edit', callback_data="editAd"), telebot.types.InlineKeyboardButton(
                text='✅ Enable', callback_data="changeAdStateEnabled"))
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=editKeyboard)
            else:
                editKeyboard = telebot.types.InlineKeyboardMarkup()
                editKeyboard.add(telebot.types.InlineKeyboardButton(
                text='✏️ Edit', callback_data="editAd"), telebot.types.InlineKeyboardButton(
                text='🚫 Disable', callback_data="changeAdStateDisabled"))
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=editKeyboard)           

        elif call.data == 'deleteAd':
                campaign = str(str(call.message.text).split("#")[1].split(" ")[0])
                print("username = "+str(call.message.chat.username))
                userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
                print("USER AD = "+str(userAd))
                newMessage = "*Campaign#"+str(campaign)+" *\n\nAre you sure you want to *delete* this ad?\n\n*This action cannot be undone.*"
                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=newMessage, parse_mode='Markdown')
                editKeyboard = telebot.types.InlineKeyboardMarkup()
                editKeyboard.add(telebot.types.InlineKeyboardButton(
                text='✅ Yes', callback_data="deleteYes"), telebot.types.InlineKeyboardButton(
                text='❌ Cancel', callback_data="deleteNo"))
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=editKeyboard)           
                #todo deleteNo
        elif call.data == 'deleteYes':
            
            print("AD user NR = "+str(str(call.message.text).split("#")[1].split(" ")[0]))
            print("username = "+str(call.message.chat.username))
            userAd = getUserAds(call.message.chat.username)[int(str(call.message.text).split("#")[1].split(" ")[0])-1][0]
            print("USER AD = "+str(userAd))
            editAdDelete(call.message, userAd)

            newMessage = "*Your Ad has been deleted.*"
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=newMessage, parse_mode='Markdown')               
                        

def editAdDelete(message, userAd):
    print("deleted campaign id = "+str(userAd))
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    mycursor = connector.cursor()
    mycursor.execute("DELETE FROM adcampaign WHERE campaignId = \'" + str(userAd)+"\'")
    connector.commit()   

def editAdDescriptionMenu(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "Enter the new Description for your ad: \n\nIt must be between *10* and *180* characters.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, userAd=userAd, callback=editAdDescriptionInput)

def editAdDescriptionInput(message,userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    if(str(message.text)=='❌Cancel'):
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')
        title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)  
    elif(len(str(message.text))>=10 and len(str(message.text))<=180):
        mycursor = connector.cursor()
        mycursor.execute("UPDATE adcampaign SET description = \'"+ str(message.text)+"\' WHERE campaignId = \'" + str(userAd)+"\'")
        connector.commit()
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')
        #print("MESSAGE " + str(message))
        #bot.edit_message_text(chat_id=message.chat.id,message_id=message.message_id,text="HELLO", parse_mode='Markdown')

        title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)
    else:
        editAdDescriptionMenu(message,userAd)

def editAdTitleMenu(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "Enter the new title for your ad: \n\nIt must be between *5* and *80* characters.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, userAd=userAd, callback=editAdTitleInput)

def editAdTitleInput(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    if(str(message.text)=='❌Cancel'):
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')
        title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)  
    elif(len(str(message.text))>=5 and len(str(message.text))<=80):
        mycursor = connector.cursor()
        mycursor.execute("UPDATE adcampaign SET title = \'"+ str(message.text)+"\' WHERE campaignId = \'" + str(userAd)+"\'")
        connector.commit()
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')     
        title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)
    else:
        editAdTitleMenu(message,userAd)

def editAdUrlMenu(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "Enter the new URL for your ad:\n\nIt should begin with https:// or http://", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, userAd=userAd, callback=editAdUrlInput)

def editAdUrlInput(message,userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    
    if(str(message.text)=='❌Cancel'):
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')
        title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)  
    else:
        try:
            if requests.get(str(message.text)).status_code == 200:
                valid = validators.url(str(message.text))
                if(valid == True):
                    mycursor = connector.cursor()
                    mycursor.execute("UPDATE adcampaign SET url = \'"+ str(message.text)+"\' WHERE campaignId = \'" + str(userAd)+"\'")
                    connector.commit()
                    keyboard.row('➕ New ad', '📊 My ads')
                    keyboard.add('🏠 Menu')
                    title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)
                elif(str(message.text)=='❌Cancel'):
                    keyboard.row('➕ New ad', '📊 My ads')
                    keyboard.add('🏠 Menu')
                    title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)  
                else:
                    editAdUrlMenu(message, userAd)
            else:
                editAdUrlMenu(message, userAd)
        except:
            editAdUrlMenu(message, userAd)


def editAdGeotagetingMenu(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('✅ Yes', '🚫 No')
    keyboard.row('❌Cancel')
 
    title = bot.send_message(message.chat.id, "Do you want to use Geotargeting? 🌍\n\n If enabled, only users from certain countries will see your ad.", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, userAd=userAd, callback=editAdGeotagetingInput)

def editAdGeotagetingInput(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    if(str(message.text)=='❌Cancel'):
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')
        title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)  
    elif(message.text == '✅ Yes'):
        newAdGeotargetingInputInput(message, userAd)
    elif(message.text == '🚫 No'):
        mycursor = connector.cursor()
        mycursor.execute("UPDATE adcampaign SET country = \'xx\' WHERE campaignId = \'" + str(userAd)+"\'")
        connector.commit()
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')     
        title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)
    else:
        editAdGeotagetingMenu(message,userAd)

def newAdGeotargetingInputInput(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('❌Cancel')   
    title = bot.send_message(message.chat.id, "Enter the two character country code(s) you want to target your ad to, separated by commas: \n\nExample: US, DE, GB, FR \n\nFor a list of countries click here (https://dogeclick.com/countries)." , parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(message=message, userAd=userAd, callback= newAdGeotargetingInputInputAccept )

def newAdGeotargetingInputInputAccept(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    if(str(message.text)=='❌Cancel'):
        keyboard.row('➕ New ad', '📊 My ads')
        keyboard.add('🏠 Menu')
        title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)  
    else:
        result = [x.strip() for x in message.text.split(',')]
        result = [x.lower() for x in result]
        print("user inserted countries = " + str(result))
        print("count 0 = " + str(result[0]))
        usercountries = ""
        for i in result:
            if i in countries:
                print("result in = "+ i)
                usercountries = usercountries + str(i)+","
            else:
                print("result not = "+ i)

        if(usercountries == ""):
            newAdGeotargetingInputInput(message, userAd)
        else:
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET country = \'" + usercountries + "\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            keyboard.row('➕ New ad', '📊 My ads')
            keyboard.add('🏠 Menu')     
            title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)
    

def editAdCpcMenu(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(str(slowest)[0:6]+' DOGE(slowest)',str(faster)[0:6]+' DOGE(faster)',str(fastest)[0:6]+' DOGE(fastest)')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "What is the most you want to pay *per click?* \n\nThe higher your cost per click, the faster people will see your ad. \n\nThe minimum amount is *"+str(slowest)[0:6] +" DOGE*\n\nEnter a value in DOGE:", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, userAd=userAd, callback=editAdCpcInput)

def editAdCpcInput(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    try:        
        if(str(message.text)=='❌Cancel'):
            keyboard.row('➕ New ad', '📊 My ads')
            keyboard.add('🏠 Menu')
            title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)      
        elif(float(str(message.text)[0:6]) >= float(str(slowest)[0:6]) and float(str(message.text)[0:6]) < float(str(faster)[0:6])):
            speed = "slowest"
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET cpc = \'" + str(message.text)[0:6] + "\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            mycursor.execute("UPDATE adcampaign SET speed = \'" + speed + "\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            keyboard.row('➕ New ad', '📊 My ads')
            keyboard.add('🏠 Menu')     
            title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)
        elif(float(str(message.text)[0:6]) >= float(str(faster)[0:6]) and float(str(message.text)[0:6]) < float(str(fastest)[0:6])):
            speed = "faster"
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET cpc = \'" + str(message.text)[0:6] + "\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            mycursor.execute("UPDATE adcampaign SET speed = \'" + speed + "\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            keyboard.row('➕ New ad', '📊 My ads')
            keyboard.add('🏠 Menu')     
            title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)
        elif(float(str(message.text)[0:6]) >= float(str(fastest)[0:6]) and float(str(message.text)[0:6]) <= float(str(maxamount)[0:6])):
            speed = "fastest"
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET cpc = \'" + str(message.text)[0:6] + "\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            mycursor.execute("UPDATE adcampaign SET speed = \'" + speed + "\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            keyboard.row('➕ New ad', '📊 My ads')
            keyboard.add('🏠 Menu')     
            title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)    
        else:
            editAdCpcMenu(message, userAd)
    except ValueError:
        editAdCpcMenu(message, userAd)


def editAdBudgetMenu(message, userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(str(cents10).split('.')[0]+' DOGE($0.10)',str(cents25).split('.')[0]+' DOGE($0.25)',str(cents100).split('.')[0]+' DOGE($1.00)')
    keyboard.row(str(cents200).split('.')[0]+' DOGE($2.00)',str(cents500).split('.')[0]+' DOGE($5.00)',str(cents1000).split('.')[0]+' DOGE($10.00)')
    keyboard.row('❌Cancel')
    title = bot.send_message(message.chat.id, "How much do you want to spend per day?\n\nThe minimum amount is *"+str(slowest)[0:5]+" DOGE*\n\nEnter a value in DOGE:", parse_mode='Markdown',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message=message, userAd=userAd, callback=editAdBudgetMenuInput)

def editAdBudgetMenuInput(message,userAd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    try:
        if(str(message.text)=='❌Cancel'):
            keyboard.row('➕ New ad', '📊 My ads')
            keyboard.add('🏠 Menu')
            title = bot.send_message(message.chat.id, "Your edit has been cancelled.", parse_mode='Markdown',reply_markup=keyboard)  
        elif(float(str(message.text).split(' ')[0]) >= float(cents10) and float(str(message.text).split(' ')[0]) <= float(cents500000)):
            print("fatto "+ str(message.text).split(' ')[0])
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET dailyBudget = \'"+ str(message.text).split(' ')[0]+"\' WHERE campaignId = \'" + str(userAd)+"\'")
            connector.commit()
            keyboard.row('➕ New ad', '📊 My ads')
            keyboard.add('🏠 Menu')
            title = bot.send_message(message.chat.id, "Your ad has been updated.", parse_mode='Markdown',reply_markup=keyboard)        
        else:
            editAdBudgetMenu(message, userAd)
    except ValueError:        
        editAdBudgetMenu(message, userAd)
                    
# //////////////////////////////////// USER FUNCTIONS ///////////////////////////////
#inserts new user in the DB
def insertUser(chatId,userAddress,country,username):

    mycursor = connector.cursor()

    sql = "INSERT INTO user (userId, referral, address, taskAlert, seeNsfw, country, username, dateJoined) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (chatId, chatId, userAddress, 1, 1, country, username, str(date.today().year)+"/"+str(date.today().month)+"/"+str(date.today().day))
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
    mycursor = connector.cursor()
    mycursor.execute("SELECT virtualBalance FROM user WHERE username = \'"+ username +"\'")  
    balance = mycursor.fetchall()[0][0]  
    connector.commit() #updates balance after being changed by the server, if not included it keeps the last value
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

# waitForUserInteraction
bot.polling()

