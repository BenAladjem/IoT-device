import btree
from data1 import Database
from modem import Sim7070

class User:
    def __init__(self):
        self.d = Database()
        self.m = Sim7070()
        
        self.user = "BeniTest"
        self.password = "12345678"
        self.imei = self.d.read('200')
        self.batt = self.d.read('223') # read from db, check from modem , when I need
        
            
'''
свързване със сървъра:

    1.модема да е вкл
    2.модема да е регистриран
    3.конекция към HiGPS
    4.изпращане валиден репорт към сървъра
    5.команда = отговора от сървъра
        изпълняване на командата
    6.проверка за следваща команда
        няма -> сървъра връща "ОК"
        има -> сървъра връща команда
            установяване типа на командата
            отговора трябва да бъде според типа команда mode-mode; eng-eng, gps-gps
        5.
    7.затваряне на конекцията


    MODE: "/input.php?IMEI=865456054799968&MSG=SLEEP-2;WORK-2;CYCLE-0;TRANS-3;OHR-1;INPUT-OPEN;&"
    ENG:
    GPS:
    gprs text:   "/input.php?IMEI=865456054799968"
    
    Важно!
    За timestamp :
    
    timestamp = modem.sendHiGPS('/t/')
    locations[loc["Timestamp"]] = [loc["Lat"],loc["Lon”],loc[“Speed"]]
    loc = {"1668175234": [42.67481, 23.28978, 0.0]}
        
'''
        
        
        
u = User()
if u.m.isOn() == False:
    print("Turning on modem")
    u.m.turnOn()
    #beep()
