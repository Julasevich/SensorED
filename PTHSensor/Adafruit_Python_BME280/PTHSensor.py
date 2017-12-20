#!/usr/bin/python

#Imports
from Adafruit_BME280 import *
import time
import datetime
import sqlite3
import os
from sqlite3 import Error

#Find The Mac Address(Unique) of Rasperry Pi Board
def getMAC():
    try:
        mac_addr = open('/sys/class/net/wlan0/address').read()
        return mac_addr[0:17]
    except Exception as e:
        return e



#Main Function
def main():
    #Variables
    repeat = 11 #Number of times you want while loop to repeat
    wait_period = 300 #Seconds you want to wait between each reading
    count = 0 #Keep 0, incriment each time you take a reading
    

    mac_address = str(getMAC())
    
    #Debug Sensor
    sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)


    #Database
    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect("/home/pi/Documents/PTHSensor/Adafruit_Python_BME280/sensorData.db")
    cursor = db.cursor()
    
    #Create a 'boards' table if it does not exist
    try:
        cursor.execute('''
            CREATE TABLE boards(id INTEGER PRIMARY KEY, mac_address TEXT,
                           dateNow TEXT, timeNow TEXT, degrees TEXT, pascals TEXT, humidity TEXT)
        ''')
    except Error as e:
        print("Error: " + str(e))
    
    #Collect Data every 'wait_period' seconds for 'repeat' amount of times
    while(repeat > count):
        degrees = float("{0:.2f}".format(sensor.read_temperature()))
        pascals = float("{0:.2f}".format(sensor.read_pressure()))
        humidity = float("{0:.2f}".format(sensor.read_humidity()))
        dateNow = time.strftime("%d/%m/%Y")
        timeNow = time.strftime("%H:%M:%S")
        cursor.execute('''INSERT INTO boards(mac_address, dateNow, timeNow, degrees, pascals, humidity)
                  VALUES(?,?,?,?,?,?)''', (mac_address, dateNow, timeNow, degrees, pascals, humidity))
        print('Temp      : ' + str(degrees) + 'C')
        print('Pressure  : ' + str(pascals) + 'Pa')
        print('Humidity  : ' + str(humidity) + '%')
        print('Database Updated')
        #Increase incrimenter
        count += 1
        #Tell Board to wait 'wait_peroid' amount of secionds before moving on
        time.sleep(wait_period)

    #Update Changes And Close Databse
    db.commit()    
    db.close()

#RUN MAIN FUNCTION
if __name__ == '__main__':
    main()








    

