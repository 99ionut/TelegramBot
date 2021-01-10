import mysql.connector
from flask import Flask, request, abort
from block_io import BlockIo
import math

#///////////////// DB CONNECT
def connect():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'telegrambot',
        password = 'telegrambot',
        database = 'telegrambot')

connector = connect()

#//////////////// SETTINGS
mycursor = connector.cursor()
mycursor.execute("SELECT blockIoApi,blockIoSecretPin,blockIoVersion,mainAccount FROM settings")
botSettings = mycursor.fetchall()
print("BOT SETTINGS = "+str(botSettings))
blockIoApi = botSettings[0][0]
blockIoSecretPin = botSettings[0][1]
blockIoVersion = botSettings[0][2]
block_io = BlockIo(str(blockIoApi), str(blockIoSecretPin), str(blockIoVersion))

mainAccount = botSettings[0][3] #main account with all the founds

app = Flask(__name__)
mycursor = connector.cursor()
#1) start server.py
#2) from cmd in telegramBot ngrok http 5000
#3) create notification from the interactive python block_io doc
#4) must close and open to update code

#in bot main once block_io.create_notification(type='account', url='http://785a748f02bb.ngrok.io/webhook')

#block_io.enable_notification(notification_id='3614d812342f08eba83cfac8')
#block_io.list_notifications(page='1')

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        #print(request.json)
        try:           
            if(float(request.json["data"]["balance_change"]) > 0 and request.json["data"]["address"] != mainAccount): #also todo check main account?
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