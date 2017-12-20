#Imports
from Adafruit_BME280 import *
import time
import datetime
import sqlite3
from sqlite3 import Error

#Find The Mac Address(Unique) of Rasperry Pi Board
def getEthName():
    try:
        for root,dirs,files in os.walk('/sys/class/net'):
            for dir in dirs:
                if dir[:3] == 'enx' or dir[:3] == 'eth':
                    interface = dir
    except:
        interface = "None"
    return interface

def getMAC(interface='eth0'):
    try:
        str = open('/sys/class/net/%s/address' %interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]


#Main Function
def main():
    #Variables
    repeat = 5 #Number of times you want while loop to repeat
    wait_period = 5 #Seconds you want to wait between each reading
    count = 0 #Keep 0, incriment each time you take a reading
    
    
    eth_name = getEthName()  #Get ethernet connection
    mac_address = getMAC(eth_name) #Get mac adress
    
    #Debug Sensor
    #tsl = TSL2561(debug=True)
    sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    #OpenFile
    #ile_object = open("LuxSensorData.txt", "w")

    #Database
    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect("/home/pi/Documents/SensorED2/sensorData.db")
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
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        humidity = sensor.read_humidity()
        dateNow = time.strftime("%d/%m/%Y")
        timeNow = time.strftime("%H:%M:%S")
        cursor.execute('''INSERT INTO boards(mac_address, dateNow, timeNow, degrees, pascals, humidity)
                  VALUES(?,?,?,?,?,?)''', (mac_address, dateNow, timeNow, degrees, pascals, humidity))
        print 'Temp      = {0:0.3f} deg C'.format(degrees)
        print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
        print 'Humidity  = {0:0.2f} %'.format(humidity)
        print('Data saved to table')
        #Write To Text File
        #file_object.write(mac_address + " " + dateNow + " " + timeNow + " " + str(luxNo) + "\n")
        #Increase incrimenter
        count += 1
        #Tell Board to wait 'wait_peroid' amount of secionds before moving on
        time.sleep(wait_period)
        

    #Save Text File    
    #file_object.close()
    

    #Test Retrive Data
    cursor.execute('''SELECT mac_address, dateNow, timeNow, degrees, pascals, humidity FROM boards''')
    all_rows = cursor.fetchall()
    for row in all_rows:
        # row[0] returns the first column in the query (mac_address), row[1] returns date column.
        print('{0} : {1}, {2}, {3}, {4}, {5}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))

    #Update Changes And Close Databse
    db.commit()    
    db.close()

#RUN MAIN FUNCTION
if __name__ == '__main__':
    main()








    

