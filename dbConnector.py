import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

def connect():
    #remove ' character for connecting to the db 
    return mysql.connector.connect(host = config['mysqlDB']['host'].replace("\'", ""),
                                   user = config['mysqlDB']['user'].replace("\'", ""),
                                   password = config['mysqlDB']['password'].replace("\'", ""),
                                   database = config['mysqlDB']['database'].replace("\'", ""))