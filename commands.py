from modem import *
from config import *
import utime

'''
modem = Sim7070()
if modem.isOn() == False:
    print("Turning on modem")
    modem.turnOn()
    beep()
'''

global log
log = config.log
global spase
spase = config.spase


class Commands:
    CLASS_NAME = "Commands"
    global modem
    global imei  #
    #imei = modem.getImei()
    
    global log
    global spase
    
    def __init__(self, command:str):
        self.command = command
        #self.m = Sim7070()
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command        
        

    def recognition_other(self):
        other = ''
        return other
    
    
    def return_result(self):
        None
        
    def send_msg_to_the_server(self, message):
        print("class Commands:   method send_msg_to_the_server(): ")
        log.append("".join([ spase, "send_msg_serv() |", spase, spase]))
        name = "BeniTest"
        pas = "87654321"
        #eng = modem.getEngLite()
        eng = modem.parseEng()
        #imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt = ",".join(batt) # returns str
      
    
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()
        
    def send_GPS_to_the_server():
        gps = ''
        loc_info = ''
        gps = modem.gps()
        imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt_descr = ",".join(batt) # returns str    
        print("gps = ",gps)
        if gps != False:
            loc_info = modem.return_base64(gps)
            #message = "/input.php?IMEI="+imei+"&bat="+batt+"&GPSArray="+loc_info+"=&"
            message = "/input.php?IMEI="+imei+"&bat="+batt[1]+"&GPSArray="+loc_info+"=&"
        else:
            # try to insert ENG
            name = "BeniTest"
            pas = "87654321"
            #cell_info = modem.parseCpsi()
            eng = modem.parseEng()
            description = name+imei+"BAT-"+batt_descr+"GSM:0000,FFFF"+eng
            message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description
        
        # IMEI=865456054799968&bat=77&GPSArray=WyI0Mi42NzQ4NjMiLCAiMjMuMjg5ODM1IiwgIjYwNC44NDcigpsQ=&
        #message = "/input.php?IMEI="+imei+"&bat="+batt+"&GPSArray="+loc_info+"=&"
        print("message = "+message)
        print("isOnGPS =",modem.isOnGPS())
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        print("connect = ",modem.isConnected())
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
            #modem.cipClose()
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()
        
        
    #message = ("/input.php?IMEI="+str(imei))#+"&bat="+str(batt)+"GPSArray="+loc_info
    #print("message = "+ messaage)
        
    #modem.sendUDP message:
    #/input.php?IMEI=865456054799968&bat=25&data=LTE;CAT-M1,OnlineOK=&
        
    #modem.sendUDP message:
    #/input.php?IMEI=865456054799968&bat=30&GPSArray=eyIgpsNjY4NjA0ODY4IjogWzQyLjY3NDc5LCAyMy4yODk4MywgNjQzLjMzNF19=&    
       
    #  'LTE;CAT-M1,Online,284-05,0gps0066,303617,339,EUTRAN-BAND3,1550,5,5,-10,-67,-44,15OK'

    def send_cpsi_to_the_server():
        name = "BeniTest"
        pas = "87654321"
        #cpsi = modem.getCPSI()
        #eng = modem.getEng()
        imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt = ",".join(batt) # returns str
        cell_info = modem.parseCpsi()
        #print(type(cpsi),"   cpsi = ",cpsi)
        #print(type(eng), "   eng = ", eng)
        print(type(imei),"   imei = ",imei)
        print(type(batt), "   batt = ", batt)
        
        #description = name+imei+"BAT-"+batt+"GSM:"+cell_info["tac"]+","+cell_info["cell_id"]+","+cell_info["mcc"]+','+cell_info["mnc"]+','+cell_info["tac"]+','+cell_info["cell_id"]+","+cell_info["rssi"]
        description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+cell_info
        message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description
        
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()
        
    def send_eng_to_the_server():
        name = "BeniTest"
        pas = "87654321"
        #eng = modem.getEngLite()
        eng = modem.parseEng()
        imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt = ",".join(batt) # returns str
        #cell_info = modem.parseCpsi()
        description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+eng
        #description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+"1,LTECAT-M10,1550,339,-84,-62,-11,5,102,303617,284,05,255"
        message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description       
        
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose() 
        
    

class User(Commands):
    
    CLASS_NAME = "User"
    # Output Type: gprs Text:  0.0096 #User=BeniTest:Pass=123456$
    # Input Type: user Text: IMEI=865456054799968&MSG=User=FC000046;Pass=M2IP1385;&
    
    def __init__(self, command:str):
        super().__init__(command)
        self.command = command
        name = ""
        pas = ""
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command        
       
    def take_name(self):
        print("class User / METHOD take_name()")
        my_command = self.command
        my_command = my_command.split(":")
        name = my_command[0].replace("#User=","")
        return name
    
    
    def take_pass(self):
        print("class User / METHOD take_pass()")
        my_command = self.command
        my_command = my_command.split(":")
        pas = my_command[1].replace("Pass=","")
        pas = pas.replace("$","")
        return pas
    
    def message(self):
        print("class User / METHOD message()")
        my_command = self.command
        my_command = my_command.split(":")
        user = my_command[0].replace("#User=","")
        pas = my_command[1].replace("Pass=","")
        pas = pas.replace("$","")
        message = "/input.php?IMEI="+imei+"&MSG=User="+user+";Pass="+pas+";&"
        return message
    
    def send_to_the_server(self, mess):
        print("class User / METHOD send_to_the_server()")
        


    def return_result(self):
        print("class User / METHOD return_resul()")
        log.append("".join([ spase, "User/return_res()|", spase, spase]))
        return modem.sendHiGPS("/input.php?IMEI=865456054799968&MSG=User=TRTRTRTR;Pass=M2IP1385;&")
    
    def main(self):
        print("class User / METHOD main()")
        pass
    
    def set_user(self,response):
        print("Set User")
        print(response)
        #User=12312341:Pass=12345678$AT
        splitted = response.split("=")
        name = splitted[1].split(":")
        self.db.write(b'name',name[0])
        self.send("user", False)
        

class Phones(Commands):
    CLASS_NAME = "Phones"
    # Output Type: gprs Text:  0.0555 #+359888555197+359889916947+359882107103$
    
    # Input Type: eng Text: IMEI=865456054799968&User=BeniTest&Pass=M2IP1385&Description="BeniTest"
    #  Input Type: phones Text: IMEI=869139052340391&MSG=+359888555197;+359889916947;+359882107103;&
    def __init__(self, command):
        super().__init__(command)
        self.command = command
        #self.other = other
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command
        
    #@staticmethod
    def return_result(self):
        log.append("".join([ spase, "Phones/retur_r()|", spase, spase]))
        my_command = self
        my_command = my_command.replace("#","")
        my_command = my_command.replace("$","")                                
        phones = my_command.split("+")
        phones = ["+"+x+";" for x in phones if len(x) >= 12] # the phones are here
        phones = "".join(phones)
        #imei = modem.getImei()
        message = "/input.php?IMEI="+imei+"&MSG="+phones


    def set_phones(self,response):
        print("Set phones")
        #+359888555197+359889916947+359882107103$AT\r'
        splitted = response.split("+")
        self.db.write(b'phone1',"+"+splitted[1])
        self.db.write(b'phone2',"+"+splitted[2])
        phone3 = splitted[3].split("$")
        self.db.write(b'phone3',"+"+phone3[0])
        self.send("phone", False)


class Mode(Commands):
    # If I need GPS in responce, call the GPS method! TRANS-3
    
    # Output Type: gprs Text:  0.0527 *MODE-0107000$
    # Input Type: mode Text: IMEI=865456054799968&MSG=SLEEP-0;WORK-1;CYCLE-0;TRANS-7;OHR-0;INPUT-OPEN;&
    
    CLASS_NAME = "Mode"
    #imei = Commands.imei
    default_report_type  = {
        "No report":"0",
        "GPS possition by SMS":"1",
        "Battery by GPRS":"2",
        "GPS and Battery by GPRS":"3",
        "Bluetooth by GPRS":"4",
        "GPS possition by SMS and GPRS":"5",
        "GSM information by GPRS":"6",
        "Battery by WiFi":"7"
        }
    
    
    
    def __init__(self, command:str): # command:str
        super().__init__(command)
        self.command = command
        
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command
        
    def prt_imei(self):
        print("immeeii = ",self.imei)
        
    def imei_pr(self):   # Not work !
        print("iiimei = ", imei)
        
    def ret_imei(self):
        return "immeeii = ",self.imei
        
    def imei_ret(self):  # Not work  !
        return "iiimei = ", imei
        
    
    def take_mode_dict(self): # returns mode command
        print("class Mode / METHOD take_mode_dict()")
        my_command = self.command
        mode = my_command.replace("*MODE-","")
        mode = mode.replace("$","")
        mode = [x for x in mode]
        return mode
    
    def take_trance(self): #returns next command type
        print("class Mode / METHOD take_trance()")
        my_command = self.command
        mode = my_command.replace("*MODE-","")
        mode = mode.replace("$","")
        mode = [x for x in mode]
        trance = mode[3]
        return trance

    def return_result(self):
        print("class Mode / METHOD return_result()")
        log.append("".join([ spase, "Mode/return_re()|", spase, spase]))
        #modem.sendHiGPS("/input.php?IMEI=865456054799968&MSG=SLEEP-1;WORK-3;CYCLE-0;TRANS-7;OHR-1;INPUT-OPEN;&")
        my_command = self
        c = my_command.replace("*MODE-","")
        c = c.replace("$","")
        c = [x for x in c]  # !!! MODE IS HERE  !!!
        trans = c[3]
        
        if c[5]== "0":
            inp = "OPEN"
        else:
            inp = "CLOSE"
    
        mode = "SLEEP-"+c[0]+";WORK-"+c[1]+";CYCLE-"+c[2]+";TRANS-"+c[3]+";OHR-"+c[4]+";INPUT-"+inp+";"
        # тук връща същият МОД, който е получен
        #imei = modem.getImei()
        message = "/input.php?IMEI="+imei+"&MSG="+mode
        
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose() 
        
class ModeQ(Commands):
    # Output Type: gprs Text:  0.0436 *MODE?$
    # Input Type: mode Text: IMEI=865456054799968&MSG=SLEEP-0;WORK-2;CYCLE-0;TRANS-7;OHR-0;INPUT-OPEN;&
    #
    CLASS_NAME = "ModeQ"
    def __init__(self, command):
        super().__init__(command)

    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command


    def return_result(self):
        print(f"ModeQ +")
        log.append("".join([ spase, "ModeQ/return_r()|", spase, spase]))
        
class Loc(Commands):
    # Output Type: gprs Text:  0.0714 *LOC$
    # Input Type: loc Text: IMEI=865456054799968&User=BeniTest&Pass=M2IP1385&Description="BeniTest"865456054799968BAT-0,88,410LOCGSM:"0578","0740"3,"0046,30,11,08ea,284,01,0578"&
    CLASS_NAME = "Loc"
    def __init__(self, command):
        super().__init__(command)
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command        


    def return_result(self):
        print("class Loc  METHOD return result()")
        log.append("".join([ spase, "Loc/return_res()|", spase, spase]))

        name = "BeniTest"
        pas = "87654321"
        #eng = modem.getEngLite()
        eng = modem.parseEng()
        #imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt = ",".join(batt) # returns str
        #cell_info = modem.parseCpsi()
        description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+eng
    #description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+"1,LTECAT-M10,1550,339,-84,-62,-11,5,102,303617,284,05,255"
        message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description       
    
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()
        
class Gprs(Commands):
    # Output Type: gprs Text:  0.0752 *GPRS$
    # GPS :  https://www.higps.org/input.php?IMEI=865456054799968&User=F5100001&Pass=DOGPE2V3&Description=%22F5100001%22865456054799968BAT-0,35,3681GSM:%2206A4%22,%222C12%22&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&
    CLASS_NAME = "Gprs"
    
    def __init__(self, command):
        super().__init__(command)
        #self.other = other
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command
     
    def send_GPS_to_the_server(): # return_result methot make the same
        print("class Gprs:   method return_result(): ")


    def return_result(self):
        print("class Gprs:   method return_result(): ")
        log.append("".join([ spase, "Gprs/return_re()|", spase, spase]))
        # send GPS to the server
        gps = ''
        loc_info = ''
        eng = modem.parseEng()
        print("eng = ", eng)
        gps = modem.gps()
        #imei = modem.getImei()
        #imei = self.imei
        batt = modem.getBat()#[1]
        print()  
        print("gps = ",gps)
        if gps != False:
            loc_info = modem.return_base64(gps)
        #message = "/input.php?IMEI="+imei+"&bat="+batt+"&GPSArray="+loc_info+"=&"
            message = "/input.php?IMEI="+imei+"&bat="+batt[1]+"&GPSArray="+loc_info+"=&"
            modem.turnOffGPS()
            modem.cipClose()
            
            
        else:
            # try to insert ENG
            modem.turnOffGPS()
            modem.cipClose()
            name = "BeniTest"  # need to read from . . .
            pas = "87654321"   # need to read from . . .
            batt = ",".join(batt)
            #eng = modem.getEng()
            #eng = modem.parseEng()  преместих го на 194 ред
            description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+eng
            message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description+"&GPS-OFF"
            modem.cipClose()

        modem.connectHiGPS()
        print("connect = ",modem.isConnected())
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()
        


class Eng(Commands):
    #
    CLASS_NAME = "Eng"
    def __init__(self, command):
        super().__init__(command)
        #self.other = other
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command        
        
    def send_eng_to_the_server(self):
        name = "BeniTest"
        pas = "87654321"
        #eng = modem.getEngLite()
        eng = modem.parseEng()
        #imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt = ",".join(batt) # returns str
        #cell_info = modem.parseCpsi()
        description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+eng
    #description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+"1,LTECAT-M10,1550,339,-84,-62,-11,5,102,303617,284,05,255"
        message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description       
    
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()

    def return_result(self):
        
        log.append("".join([ spase, "Eng/return_res()|", spase, spase]))
        name = "BeniTest"
        pas = "87654321"
        #eng = modem.getEngLite()
        eng = modem.parseEng()
        #imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt = ",".join(batt) # returns str
        #cell_info = modem.parseCpsi()
        description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+eng
    #description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+"1,LTECAT-M10,1550,339,-84,-62,-11,5,102,303617,284,05,255"
        message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description       
    
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()
    


class Wifi(Commands):
    CLASS_NAME = "WiFi" 
    # Input Type: eng Text: IMEI=865456054799968&User=BeniTest&Pass=014_23_l&Description=BeniTest865456054799968BAT-0,33,3430GSM:0000,FFFF284,05,066f,2e55,53,066f,2f64,38,066f&wifij=[[-50,d8:50:e6:95:b9:d0,3],[-60,08:55:31:e7:02:82,1],[-61,0a:55:31:e7:02:82,1]]&data=307,1;216,1;264,0;290,0;&er=&
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command

    def return_result(self):
        pass
    
class Start(Commands):
    CLASS_NAME = "Start"
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command

    def return_result(self):
        pass
    
class Stop1(Commands):
    CLASS_NAME = "Stop1" 
    # Output Type: gprs Text:  0.0703 *STOP1$
    # Input Type: stop Text: IMEI=865456054799968&MSG=STOP1&
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command        

    def return_result(self):
        pass

class Stop3(Commands):
    # Output Type: gprs Text:  0.0685 *STOP3$
    # Input Type: stop Text: IMEI=865456054799968&MSG=STOP3&
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass
    
class Set(Commands):
    CLASS_NAME = "Set"

    def __init__(self, command):
        super().__init__(command)
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command

    def return_result(self):
        log.append("".join([ spase, "Set/return_res()|", spase, spase]))
        print("class Set : METHOD return result()")
    
    
class Get(Commands):
    # да се пренапише метода. Трябва да чете от паметта стойността на параметъра,
    # който отговаря на номера команда и да върне стойността към сървъра
    CLASS_NAME = "Get"
    def __init__(self, command):
        super().__init__(command)
        

    def get_samplings(self):
        print("class Get:   method get_sampling(): ")
        #кой параметри по ID искаме да предаваме
        pass

    def get_samplingsAlarm(self):
        print("class Get:   method get_samplingAlarm(): ")
        return self.get_samplings() + "440,1;"

    def get_dataBat(self):
        print("class Get:   method get_dataBat(): ")
        log.append("".join([ spase, "Get/g_dataBat()|", spase, spase]))
        # description = "F5100001"865456054799968BAT-0,35,3681GSM:"06A4","2C12"&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&
        # message = IMEI=865456054799968&User=F5100001&Pass=DOGPE2V3&Description=+description
        name = "BeniTest"
        pas = "87654321"
        batt = modem.getBat()
        batt = ",".join(batt)
        #description = name+imei+"BAT-"+batt+"GSM:"+"06A4"+","+"2C12"+"&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&"
        description = "'"+name+"'"+imei+"BAT-"+batt+"GSM:"+"'"+"06A4"+"','"+"2C12"+"'&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&"
        message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description
        
        return message

    def get_data(self):
        print("class Get:   method get_data(): ")
        pass

    def get_setting(self, id):
        print("class Get:   method get_setting(): ")
        pass

    def get_command(self, id):
        print("class Get:   method get_command(): ")
        pass
    
    def return_result(self): # returns command type
        print("class Get:   method return_result(): ")
        log.append("".join([ spase, "Get/return_res()|", spase, spase]))
        my_command = str(self)
        print("command_ = ", my_command ,"  type = ", type(my_command))
        c = my_command.replace("*GET,","")
        command_type = c.replace("$","")
        print("command_type = ", command_type ,"  type = ", type(command_type))
        
        #return command_type
        #if command_type == "223":
        
        batt_message = self.get_dataBat()
        #x = '/input.php?IMEI=865456054799968&User=BeniTest&Pass=87654321&Description="BeniTest"865456054799968BAT-0,93,4219GSM:"06A4","2C12"&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&'
        self.send_msg_to_the_server(batt_message)
        #self.send_msg_to_the_server(x)
'''
class_instance = Commands("inst") # only make instance

def recogn_name(command):
    print("METHOD recogn_name()")
    
    '''
'''
    d = {"#User=":"User",
             "#+":"Phones",
         "*MODE-":"Mode",
        "*MODE?$":"ModeQ",
         "*GPRS$": "Gprs",
          "*GSM$": "Eng",
         "*ENG$" : "Eng",
         "*GET," : "Get",
         "*SET," : "Set"
        }
     '''
'''
    class_name = ''
    for key in config.d:
        if key in command:
            class_name = config.d[key]
            # else:
            #     return "False"
    return class_name



def reading_command(): #изпраща команда обръщение към сървъра, за да прочете чакаща команда, ако има
    print("METHOD reading_command()")
    modem.cipClose()
    modem.connectHiGPS()    
    com = modem.sendHiGPS("/input.php?IMEI=865456054799968")
    print("com= ", com)
    if len(com) > 1 :
        com = com.decode("utf-8")
        
        return com
    else:
        return False

def command_action(command): # is calling method return_result
    print("METHOD command_action()")
    r = recogn_name(command)
    print("Class name == ",r)
    st = ".return_result('"+command+"')"  # add command as argument
    print("st = ", st)

    return eval(r + st)

def class_instan_method(command): # връща инстанция към класа, за който се отнася командата
    print("METHOD class_instan()")
    class_name = recogn_name(command)
    return eval(class_name+"('"+command+"')")


def class_instance_action(command):# за тест генерира съобщение с нужните данни и ги изпраща към сървъра 
    com = class_instance.return_result()
    if com == "223":
        mess = class_instance.get_dataBat()
        class_instance.send_msg_to_the_server(mess)

def command_cicle(): # чете и изпълнява чакащите команди от сървъра, докато има
    global class_instance
    print("METHOD command_cicle()")
    c = ""
    while not c == "OK":
        c = reading_command()
        if c == "OK":
            return "No more commands "
        elif c == "":
            return "No command"
                # да се провери какво дава сървъра без чакаща команда
        #command_action(c)
        class_instance = class_instan_method(c)  # returns class instance
        #print(class_instance.command)
        #print("TRANCE = ", class_instance.command)
        
        command_action(c)
        
        #class_instance_action(c)
        #class_instance.send_to_the_server(x)
        
        

'''

        

#a = Commands("*MODE?$")
#r = a.recognition_name()
#eval(r+".return_result(a)")
