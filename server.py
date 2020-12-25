import dbConnector
from flask import Flask, request, abort

app = Flask(__name__)
connector = dbConnector.connect()


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
        print("balance = "+str(float(request.json["data"]["balance_change"])))
        try:
            
            if(float(request.json["data"]["balance_change"]) >= 0):
                print("positivo") #positive transactions (deposit)
                #print(request.json)

                address = str(request.json["data"]["address"])
                updateUser(address)               
                print("porcoddio")
            else:
                print("negativo") #negative transactions (withdraw)
        except:
            print("richiesta non da block_io")
        return 'success', 200
    else:
        abort(400)

def updateUser(address):
    print("address = "+address)
    mycursor = connector.cursor()
    mycursor.execute("SELECT username FROM user WHERE address = "+ address)
    user = mycursor.fetchall()
    print("user sent = "+str(user))

if __name__ == '__main__':
    app.run()