import mysql.connector
from flask import Flask, request, abort
from block_io import BlockIo
import math
import telebot
import time
from botProcessHandlerIonut import restartBot
from flask_cors import CORS, cross_origin
#///////////////// DB CONNECT
def connect():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'telegrambot')

connector = connect()

#//////////////// SETTINGS
connector = connect()
mycursor = connector.cursor()
mycursor.execute("SELECT blockIoApi,blockIoSecretPin,blockIoVersion,mainAccount,botToken FROM settings")
botSettings = mycursor.fetchall()
mycursor.close()
connector.close()
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

#1) start server.py
#2) from cmd in telegramBot ngrok http 5000
#3) create notification from the interactive python block_io doc
#4) must close and open to update code

#in bot main once block_io.create_notification(type='account', url='http://785a748f02bb.ngrok.io/webhook')

#block_io.enable_notification(notification_id='3614d812342f08eba83cfac8')
#block_io.list_notifications(page='1')

#todo https not http because http doesnt work irl

@app.route('/restart', methods=['POST'])  #WEBSITE WEBHOOK
@cross_origin()
def restart():
    print(str(request))
    if request.method == 'POST':
        #get webhook data
        print("restarting from website...")
        restartBot()
        return 'success', 200       
    else:
        abort(400)


@app.route('/withdraw', methods=['POST'])  #WEBSITE WEBHOOK
@cross_origin()
def withdraw():
    if request.method == 'POST':
        #get webhook data
        print("WITHDRAW")
        try:
            dati = str(request.form)
            print(dati)
        
            withdrawId = dati.split("\"")[3]
            print(withdrawId)
            withdrawUserAddress =  dati.split("\"")[7]
            print(withdrawUserAddress)
            withdrawAmount =  dati.split("\"")[11]
            print(withdrawAmount)
            withdrawUserPersonalAddress =  dati.split("\"")[15]
            print(withdrawUserPersonalAddress)

            transactionFee = block_io.get_network_fee_estimate(amounts=withdrawAmount, to_addresses=withdrawUserPersonalAddress)
            transactionFee = transactionFee['data']['estimated_network_fee']
            amoutWithoutFee = float(withdrawAmount) - float(transactionFee)
            block_io.withdraw_from_addresses(amounts=str(amoutWithoutFee), from_addresses= mainAccount , to_addresses=str(withdrawUserPersonalAddress), priority='custom', custom_network_fee= str(transactionFee))
        
            #Delete temporary link
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("DELETE FROM withdraw WHERE id = \'"+ withdrawId +"\'")
            print("DELETED Withdraw")
            connector.commit()
            mycursor.close()
            connector.close()
        
        except ValueError:
            print("Withdraw error")

        return 'success', 200       
    else:
        abort(400)

@app.route('/revoke', methods=['POST'])  #WEBSITE WEBHOOK
@cross_origin()
def revoke():
    if request.method == 'POST':
        #get webhook data
        print("REVOKE")

        try:
            dati = str(request.form)
            print(dati)

            revokeId = dati.split("\"")[3]
            print(revokeId)
            revokeAmount =  dati.split("\"")[7]
        
            print(revokeAmount)

            #get revoked user username
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("SELECT username FROM withdraw WHERE id = \'"+ str(revokeId) +"\'")
            usernameRevoke = mycursor.fetchall()[0][0]
            mycursor.close()
            connector.close()
            print("Username = "+str(usernameRevoke))


            #Return user balance
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET virtualBalance = virtualBalance + "+ str(revokeAmount) +" WHERE username = \'"+ str(usernameRevoke) +"\'")
            connector.commit()
            mycursor.close()
            connector.close()

            #Delete revoke withdraw
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("DELETE FROM withdraw WHERE id = \'"+ str(revokeId) +"\'")
            print("DELETED Withdraw")
            connector.commit()
            mycursor.close()
            connector.close()
        except ValueError:
            print("Revoke error")

        return 'success', 200       
    else:
        abort(400)

@app.route('/website', methods=['POST'])  #WEBSITE WEBHOOK
@cross_origin()
def website():
    print(str(request))
    if request.method == 'POST':
        
        try:
            #get webhook data
            print("WEBSITE WEBHOOK")

            dati = str(request.form)
            print(dati)

            websiteXframe = dati.split("\"")[15]
            print("websiteXframe = "+websiteXframe)
            websiteCustomLink = dati.split("\"")[3]
            print("websiteCustomLink = "+websiteCustomLink)
            websiteUsername = dati.split("\"")[7]
            print("websiteUsername = "+websiteUsername)
            websiteCampaignId = dati.split("\"")[11]
            print("websiteCampaignId = "+websiteCampaignId)

            #webhook query
            connector = connect()
            mycursor = connector.cursor()
            #get ownerTake
            mycursor.execute("SELECT ownerTake,referralTake FROM settings")
            getResults = mycursor.fetchall()
            mycursor.close()
            connector.close()
            ownerTake = getResults[0][0]
            referralTake = getResults[0][1]
            print("OWNER TAKE % = "+str(ownerTake))
            print("REFERRAL TAKE % = "+str(referralTake))

            ###delete temporary link
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("DELETE FROM link WHERE customLink = \'"+ websiteCustomLink +"\'")
            print("DELETED LINK")
            connector.commit()
            mycursor.close()
            connector.close()

            #get the campaign cpc,dailyBudget,dailyBudgetSpent,username 
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("SELECT cpc,dailyBudget,dailyBudgetSpent,username FROM adcampaign WHERE campaignId = \'"+ websiteCampaignId +"\'")
            websiteAd = mycursor.fetchall()
            mycursor.close()
            connector.close()
            print("WEBSITE AD = "+str(websiteAd))

            #if virtual balance <= 0 set ad status to 0 (disabled)
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("SELECT virtualBalance FROM user WHERE username = \'"+ str(websiteAd[0][3]) +"\'")
            userVirtualBalance = mycursor.fetchall()[0][0]
            mycursor.close()
            connector.close()
            print("USER VB = "+str(userVirtualBalance))
            if(userVirtualBalance <= 0):
                print("DISABLED AD")
                mycursor.execute("UPDATE adcampaign SET status = 0 WHERE campaignId = \'"+ str(websiteCampaignId) +"\'")
                connector.commit()

            #remove from virtual balance of the user that posted the ad
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET virtualBalance = virtualBalance - \'"+ str(websiteAd[0][0]) +"\' WHERE username = \'"+ str(websiteAd[0][3]) +"\'")
            connector.commit()
            mycursor.close()
            connector.close()
            print("REMOVED VB")

            #set last ad -1 to the user that has seen the ad
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET lastAd = -1 WHERE username = \'"+ websiteUsername +"\'")
            connector.commit()
            mycursor.close()
            connector.close()
            print("REMOVED LAST AD")

            #give the user that has seen the ad money
            userCpc = float(websiteAd[0][0])-((float(websiteAd[0][0])*ownerTake)/100)
            userCpcDecimals = userCpc
            #give the referral user ad money
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("SELECT referredBy,userId,country FROM user WHERE username = \'"+ websiteUsername +"\'")
            userResults = mycursor.fetchall()
            mycursor.close()
            connector.close()
            referralUsername = userResults[0][0]
            userId = userResults[0][1]
            userCountry = userResults[0][2]
            if(referralUsername == "[]"):
                connector = connect()
                mycursor = connector.cursor()
                mycursor.execute("UPDATE user SET virtualBalance = virtualBalance + \'"+ str(userCpcDecimals) +"\' WHERE username = \'"+ websiteUsername +"\'")
                connector.commit()
                mycursor.close()
                connector.close()
                earningMinusReferral = userCpcDecimals
                print("GIVE CPC = "+str(earningMinusReferral))
            else:
                referralCpc = ((float(userCpcDecimals)*referralTake)/100)
                referralCpcDecimals = "{:.4f}".format(referralCpc)
                earningMinusReferral = float(userCpcDecimals)-float(referralCpcDecimals)
                earningMinusReferral = "{:.4f}".format(earningMinusReferral)
                connector = connect()
                mycursor = connector.cursor()
                mycursor.execute("UPDATE user SET virtualBalance = virtualBalance + \'"+ str(referralCpcDecimals) +"\' WHERE username = \'"+ referralUsername +"\'")
                connector.commit()
                mycursor.close()
                connector.close()
                print("GIVE REF.CPC = "+str(referralCpcDecimals))
                #add to the total referralEarnings
                connector = connect()
                mycursor = connector.cursor()
                mycursor.execute("UPDATE user SET referralEarning = referralEarning + \'"+ str(referralCpcDecimals) +"\' WHERE username = \'"+ referralUsername +"\'")
                connector.commit()
                mycursor.close()
                connector.close()
                connector = connect()
                mycursor = connector.cursor()
                mycursor.execute("UPDATE user SET virtualBalance = virtualBalance + \'"+ str(earningMinusReferral) +"\' WHERE username = \'"+ websiteUsername +"\'")
                connector.commit()
                mycursor.close()
                connector.close()
                print("GIVE CPC = "+str(earningMinusReferral))

            #increase country clicks
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE country SET clicks = clicks + 1 WHERE code =  \'"+ str(userCountry) +"\'")
            connector.commit()
            mycursor.close()
            connector.close()
            #increase clicks
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET clicks = clicks + 1 WHERE campaignId =  \'"+ websiteCampaignId +"\'")
            connector.commit()
            mycursor.close()
            connector.close()

            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET clicksToday = clicksToday + 1 WHERE campaignId =  \'"+ websiteCampaignId +"\'")
            connector.commit()
            mycursor.close()
            connector.close()
            print("CLICKED")

            #increase dailyBudgetSpent
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE adcampaign SET dailyBudgetSpent = dailyBudgetSpent + \'"+ str(websiteAd[0][0]) +"\' WHERE campaignId = \'"+ websiteCampaignId +"\'")
            connector.commit()
            mycursor.close()
            connector.close()
            print("INCREASE DAILY BUDGET")
            print("DONE")
            print(str(websiteXframe))
            if(websiteXframe == "1"): #send message immedialy if xframe == 1 (so the user already waited on the website)
                bot.send_message(userId, text="You earned "+earningMinusReferral+" DOGE!")
            elif(websiteXframe == "0"):    #else wait 10 seconds

                bot.send_message(userId, text="Please stay on the site for at least 10 seconds...")
                time.sleep(10)
                bot.send_message(userId, text="You earned "+earningMinusReferral+" DOGE!")

        except Exception as e:
            print(e)
        return 'success', 200       
    else:
        abort(400)


@app.route('/webhook', methods=['POST'])  #BLOCKIO WEBHOOK
@cross_origin()
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

                connector = connect()
                mycursor = connector.cursor()
                mycursor.execute("SELECT transaction FROM transaction WHERE transaction = \'"+ txid +"\'")
                existingTransaction = mycursor.fetchall()
                mycursor.close()
                connector.close()
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
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("SELECT virtualBalance FROM user WHERE address = \'"+ address +"\'") 
            print("SELECT virtualBalance FROM user WHERE address = \'"+ address +"\'") 
            virtualBalance = mycursor.fetchall()
            mycursor.close()
            connector.close()
            print("virtual Balance = "+str(virtualBalance[0][0]))
            totalBalance = float(balance) + float(str(virtualBalance[0][0])) 
            print("Total Balance = "+str(totalBalance))
            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("UPDATE user SET virtualBalance = \'"+ str(totalBalance) +"\'  WHERE address = \'" + str(address) + "\'")
            connector.commit()
            mycursor.close()
            connector.close()

            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("SELECT username FROM user WHERE address = \'"+ str(address) +"\' ")
            username = str(mycursor.fetchall()[0][0])
            connector.commit()
            mycursor.close()
            connector.close()

            connector = connect()
            mycursor = connector.cursor()
            mycursor.execute("INSERT INTO transaction(transaction,amount,userAddress,userUsername) VALUES ( \'" + str(txid) + "\',\'" + str(balance) + "\',\'" + str(address) + "\',\'" + str(username) + "\')")
            connector.commit()
            mycursor.close()
            connector.close()
            print("DB Insert")
            block_io.withdraw_from_addresses(amounts=str(amountMinusFee), from_addresses= address , to_addresses=str(mainAccount), priority='custom', custom_network_fee= str(fee))
            print("SENT!")
    

if __name__ == '__main__':
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run()
    
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)