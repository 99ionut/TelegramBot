import os
import subprocess
import time
handleBot = subprocess.Popen("cmd.exe",shell=False)
def startBot():
    global handleBot 
    global handleServer 
    handleBot = subprocess.Popen("python bot_main.py", shell=True)
    handleServer = subprocess.Popen("python server.py", shell=False)

def restartBot():
    global handleBot 
    subprocess.Popen("taskkill /F /T /PID %i"%handleBot.pid , shell=False)
    time.sleep(30)
    handleBot = subprocess.Popen("python bot_main.py", shell=False)

if __name__ == "__main__":
    print("QUESTO E IL MAIN")
    startBot()

