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
    try:
        f = open("mydb_user", "r + b")
    except:
        f = open("mydb_user", "w + b")
        print("File")
        
    db = btree.open(f)

    for key in db:
        self.data[key] = db[key]

    db.flush()
    db.close()
    f.close()
        
'''        
'''
свързване със сървъра:

    1.модема да е вкл
    2.модема да е регистриран
    3.конекция към HiGPS
    4.изпращане валиден репорт към сървъра
    5.команда = отговора от сървъра
        изпълняване на командата
    6.проверка за следваща команда
        има -> 5.
    7.затваряне на конекцията
        
'''
        
        
        
u = User()
if u.m.isOn() == False:
    print("Turning on modem")
    u.m.turnOn()
    #beep()