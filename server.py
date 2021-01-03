import mysql.connector
from flask import Flask, request, abort
from block_io import BlockIo

mainAccount = "2N1fJnGvvbLexRusQXet77fFAgoL6MuMRDx" #main account with all the founds
version = 2
block_io = BlockIo('8383-cae2-01f4-720f', 'telegrambot', version)

def connect():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'telegrambot',
        password = 'telegrambot',
        database = 'telegrambot')

connector = connect()

app = Flask(__name__)

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
            if(float(request.json["data"]["balance_change"]) >= 0):
                print("positive") #positive transactions (deposit)
                balance = float(request.json["data"]["balance_change"])
                address = str(request.json["data"]["address"])             
                updateUser(address,balance)
            else:
                #print("negative") #negative transactions (withdraw)
                pass
        except:
            print("errore")
              
        return 'success', 200
        
    else:
        abort(400)

def updateUser(address,balance):
        print("address = "+address)
        print("recieved balance = "+str(balance))
        
        mycursor = connector.cursor()
        mycursor.execute("SELECT virtualBalance FROM user WHERE address = \'"+ address +"\'") 
        print("SELECT virtualBalance FROM user WHERE address = \'"+ address +"\'") 
        virtualBalance = mycursor.fetchall()
        if(address == str(mainAccount)):
            print("MAIN ACCOUNT BAL = "+str(virtualBalance[0][0]))
        else:
            print("virtual Balance = "+str(virtualBalance[0][0]))

        totalBalance = float(balance) + float(str(virtualBalance[0][0])) 
        print("Total Balance = "+str(totalBalance))
        mycursor = connector.cursor()
        mycursor.execute("UPDATE user SET virtualBalance = \'"+ str(totalBalance) +"\'  WHERE address = \'" + address + "\'")
        connector.commit()
        print("fee = "+str(block_io.get_network_fee_estimate(amounts=str(balance), to_addresses=str(mainAccount))["data"]["estimated_network_fee"]))
        fee = str(block_io.get_network_fee_estimate(amounts=str(balance), to_addresses=str(mainAccount))["data"]["estimated_network_fee"])
        #amountMinusFee = float(balance)-float(fee) #sometimes when sending from user to main account you have to send amount - fee because it doesnt calculate it automatically?
        amountMinusFee = float(balance)
        #print("amountMinusFee = "+str(amountMinusFee))
        block_io.withdraw_from_addresses(amounts=str(amountMinusFee), from_addresses= address , to_addresses=str(mainAccount))
   
    

if __name__ == '__main__':
    app.run()