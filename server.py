import mysql.connector
from flask import Flask, request, abort
from block_io import BlockIo
import math
import telebot
import time

#///////////////// DB CONNECT
def connect():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'telegrambot')

connector = connect()

#//////////////// SETTINGS
mycursor = connector.cursor()
mycursor.execute("SELECT blockIoApi,blockIoSecretPin,blockIoVersion,mainAccount,botToken FROM settings")
botSettings = mycursor.fetchall()
print("BOT SETTINGS = "+str(botSettings))
blockIoApi = botSettings[0][0]
blockIoSecretPin = botSettings[0][1]
blockIoVersion = botSettings[0][2]
block_io = BlockIo(str(blockIoApi), str(blockIoSecretPin), str(blockIoVersion))

mainAccount = botSettings[0][3] #main account with all the founds

# BOT TOKEN
botToken = botSettings[0][4]
token = str(botToken)
bot = telebot.TeleBot(token)

app = Flask(__name__)
mycursor = connector.cursor()
#1) start server.py
#2) from cmd in telegramBot ngrok http 5000
#3) create notification from the interactive python block_io doc
#4) must close and open to update code

#in bot main once block_io.create_notification(type='account', url='http://785a748f02bb.ngrok.io/webhook')

#block_io.enable_notification(notification_id='3614d812342f08eba83cfac8')
#block_io.list_notifications(page='1')

@app.route('/website', methods=['POST'])  #WEBSITE WEBHOOK
def website():
    if request.method == 'POST':
        
        try:
            #get webhook data
            print("WEBSITE WEBHOOK")    
            dati = request.get_json(force=True)
            print(dati)     
            websiteXframe = dati["xframe"]
            print("websiteXframe = "+websiteXframe)
            websiteCustomLink = dati["customLink"]
            print("websiteCustomLink = "+websiteCustomLink)
            websiteUsername = dati["username"]
            print("websiteUsername = "+websiteUsername)
            websiteCampaignId = dati["campaignId"]
            print("websiteCampaignId = "+websiteCampaignId)

            #webhook query
            mycursor = connector.cursor()

            #get ownerTake
            mycursor.execute("SELECT ownerTake,referralTake FROM settings")
            getResults = mycursor.fetchall()
            ownerTake = getResults[0][0]
            referralTake = getResults[0][1]
            print("OWNER TAKE % = "+str(ownerTake))
            print("REFERRAL TAKE % = "+str(referralTake))

            #delete temporary link
            #mycursor.execute("DELETE FROM link WHERE customLink = \'"+ websiteCustomLink +"\'")
            print("DELETED LINK")
            #connector.commit()

            #get the campaign cpc,dailyBudget,dailyBudgetSpent,username 
            mycursor.execute("SELECT cpc,dailyBudget,dailyBudgetSpent,username FROM adcampaign WHERE campaignId = \'"+ websiteCampaignId +"\'")
            websiteAd = mycursor.fetchall()
            print("WEBSITE AD = "+str(websiteAd))

            #if virtual balance <= 0 set ad status to 0 (disabled)
            mycursor.execute("SELECT virtualBalance FROM user WHERE username = \'"+ str(websiteAd[0][3]) +"\'")
            userVirtualBalance = mycursor.fetchall()[0][0]
            print("USER VB = "+str(userVirtualBalance))
            if(userVirtualBalance <= 0):
                print("DISABLED AD")
                mycursor.execute("UPDATE adcampaign SET status = 0 WHERE campaignId = \'"+ str(websiteCampaignId) +"\'")
                connector.commit()

            #remove from virtual balance of the user that posted the ad
            mycursor.execute("UPDATE user SET virtualBalance = virtualBalance - \'"+ str(websiteAd[0][0]) +"\' WHERE username = \'"+ str(websiteAd[0][3]) +"\'")
            connector.commit()
            print("REMOVED VB")

            #set last ad -1 to the user that has seen the ad
            mycursor.execute("UPDATE user SET lastAd = -1 WHERE username = \'"+ websiteUsername +"\'")
            connector.commit()
            print("REMOVED LAST AD")

            #give the user that has seen the ad money
            userCpc = websiteAd[0][0]-((websiteAd[0][0]*ownerTake)/100)
            userCpcDecimals = "{:.4f}".format(userCpc)
            #give the referral user ad money
            mycursor.execute("SELECT referredBy,userId,country FROM user WHERE username = \'"+ websiteUsername +"\'")
            userResults = mycursor.fetchall()
            referralUsername = userResults[0][0]
            userId = userResults[0][1]
            userCountry = userResults[0][2]
            if(referralUsername == "[]"):
                mycursor.execute("UPDATE user SET virtualBalance = virtualBalance + \'"+ str(userCpcDecimals) +"\' WHERE username = \'"+ websiteUsername +"\'")
                connector.commit()
                earningMinusReferral = userCpcDecimals
                print("GIVE CPC = "+str(earningMinusReferral))
            else:
                referralCpc = ((float(userCpcDecimals)*referralTake)/100)
                referralCpcDecimals = "{:.4f}".format(referralCpc)
                earningMinusReferral = float(userCpcDecimals)-float(referralCpcDecimals)
                earningMinusReferral = "{:.4f}".format(earningMinusReferral)
                mycursor.execute("UPDATE user SET virtualBalance = virtualBalance + \'"+ str(referralCpcDecimals) +"\' WHERE username = \'"+ referralUsername +"\'")
                connector.commit()
                print("GIVE REF.CPC = "+str(referralCpcDecimals))
                #add to the total referralEarnings
                mycursor.execute("UPDATE user SET referralEarning = referralEarning + \'"+ str(referralCpcDecimals) +"\' WHERE username = \'"+ referralUsername +"\'")
                connector.commit()
                mycursor.execute("UPDATE user SET virtualBalance = virtualBalance + \'"+ str(earningMinusReferral) +"\' WHERE username = \'"+ websiteUsername +"\'")
                connector.commit()
                print("GIVE CPC = "+str(earningMinusReferral))

            #increase country clicks
            mycursor.execute("UPDATE country SET clicks = clicks + 1 WHERE code =  \'"+ str(userCountry) +"\'")
            connector.commit()

            #increase clicks
            mycursor.execute("UPDATE adcampaign SET clicks = clicks + 1 WHERE campaignId =  \'"+ websiteCampaignId +"\'")
            connector.commit()
            mycursor.execute("UPDATE adcampaign SET clicksToday = clicksToday + 1 WHERE campaignId =  \'"+ websiteCampaignId +"\'")
            connector.commit()
            print("CLICKED")

            #increase dailyBudgetSpent
            mycursor.execute("UPDATE adcampaign SET dailyBudgetSpent = dailyBudgetSpent + \'"+ str(websiteAd[0][0]) +"\' WHERE campaignId = \'"+ websiteCampaignId +"\'")
            connector.commit()
            print("INCREASE DAILY BUDGET")
            print("DONE")
            if(websiteXframe == 1): #send message immedialy if xframe == 1 (so the user already waited on the website)
                bot.send_message(userId, text="You earned "+earningMinusReferral+" DOGE!")
            else:                   #else wait 10 seconds
                sendMessage(userId,earningMinusReferral)

        except Exception as e:
            print(e)
        return 'success', 200       
    else:
        abort(400)

def sendMessage(userId,earningMinusReferral):
    bot.send_message(userId, text="Please stay on the site for at least 10 seconds...")
    time.sleep(10)
    bot.send_message(userId, text="You earned "+earningMinusReferral+" DOGE!")


@app.route('/webhook', methods=['POST'])  #BLOCKIO WEBHOOK
def webhook():
    if request.method == 'POST':
        #print(request.json)   
        #print(dati["xframe"])      
        try:     
            if(float(request.json["data"]["balance_change"]) > 0 and request.json["data"]["address"] != mainAccount): #also todo check main account?
                print("BLOCKIO WEBHOOK")
                print("positive") #positive transactions (deposit)
                balance = float(request.json["data"]["balance_change"])
                address = str(request.json["data"]["address"])
                txid = str(request.json["data"]["txid"])

                mycursor.execute("SELECT transaction FROM transaction WHERE transaction = \'"+ txid +"\'")
                existingTransaction = mycursor.fetchall()
                print("existing transaction = " + str(existingTransaction))
                if(str(existingTransaction) == "[]"): #this is to avoid doing the same thing twice, because the block_io sends the same webhook more than once
                    updateUser(address,balance,mycursor,txid)
                else:
                    print("!ALREADY EXISTS")
            else:
                #print("negative") #negative transactions (withdraw)
                pass
        except Exception as e:
            print(e)
            if(e == "MySQL Connection not available."):
                connector.cursor()
              
        return 'success', 200
        
    else:
        abort(400)

def updateUser(address,balance,mycursor,txid):
        print("address = "+address)
        print("recieved balance = "+str(balance))

        print("fee = "+str(block_io.get_network_fee_estimate(amounts=str(balance), to_addresses=str(mainAccount))["data"]["estimated_network_fee"]))
        fee = str(block_io.get_network_fee_estimate(amounts=str(balance), to_addresses=str(mainAccount))["data"]["estimated_network_fee"])
        amountMinusFee = '%.3f'%(float(balance)-float(fee)) #need to keep 3 decimals, too many decimals break the transaction
        print("amount minus fee = "+str(amountMinusFee))
        amountToSend = float(balance)
        print("total amount to send = "+str(amountToSend))
        if(float(amountMinusFee) < 2 ): #block io need at least 2 (without fee) doge to send the transaction
            print("!AMOUNT TOO LOW")
        else:
            mycursor.execute("SELECT virtualBalance FROM user WHERE address = \'"+ address +"\'") 
            print("SELECT virtualBalance FROM user WHERE address = \'"+ address +"\'") 
            virtualBalance = mycursor.fetchall()
            print("virtual Balance = "+str(virtualBalance[0][0]))
            totalBalance = float(balance) + float(str(virtualBalance[0][0])) 
            print("Total Balance = "+str(totalBalance))
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET virtualBalance = \'"+ str(totalBalance) +"\'  WHERE address = \'" + str(address) + "\'")
            connector.commit()

            mycursor = connector.cursor()
            mycursor.execute("SELECT username FROM user WHERE address = \'"+ str(address) +"\' ")
            username = str(mycursor.fetchall()[0][0])
            connector.commit()
            mycursor = connector.cursor()
            mycursor.execute("INSERT INTO transaction(transaction,amount,userAddress,userUsername) VALUES ( \'" + str(txid) + "\',\'" + str(balance) + "\',\'" + str(address) + "\',\'" + str(username) + "\')")
            connector.commit()
            print("DB Insert")
            block_io.withdraw_from_addresses(amounts=str(amountMinusFee), from_addresses= address , to_addresses=str(mainAccount), priority='custom', custom_network_fee= str(fee))
            print("SENT!")
    

if __name__ == '__main__':
    app.run()
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)