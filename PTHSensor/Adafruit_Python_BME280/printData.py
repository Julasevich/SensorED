#Imports
import sqlite3
import os
from sqlite3 import Error

#Open Your Databse File
db = sqlite3.connect("/home/pi/Documents/PTHSensor/Adafruit_Python_BME280/sensorData.db")
cursor = db.cursor()

#Retrieve Data
cursor.execute('''SELECT mac_address, dateNow, timeNow, degrees, pascals, humidity FROM boards''')
all_rows = cursor.fetchall()

for row in all_rows:
    # row[0] returns the first column in the query (mac_address), row[1] returns date column.
    print('{0} : Date: {1}, Time: {2}, Temperature: {3}C, Pressure: {4}Pa, Humidity: {5}%'.format(row[0], row[1], row[2], row[3], row[4], row[5]))

#Close Databse
db.commit()
db.close()
