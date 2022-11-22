from modem import *
import utime

modem = Sim7070()

class Commands:
    global modem
    def __init__(self, command):
        self.command = command
        self.m = Sim7070()
        
        self.imei = modem.getImei()
        self.batt = modem.getBat()[1]

        self.d = {"#User=":"User",
                  "#+":"Phones",
                  "*MODE-":"Mode",
                  "*MODE?$":"ModeQ",
                  "*GPRS$": "Gprs",
                  "*GSM$": "Eng"
                  }


    def recognition_name(self):
        class_name = ''
        for key in self.d:
            if key in self.command:
                class_name = self.d[key]
            # else:
            #     return "False"
        return class_name


    def recognition_other(self):
        other = ''
        return other

    def return_result(self):
        None


class User(Commands):
    # Output Type: gprs Text:  0.0096 #User=BeniTest:Pass=123456$
    # Input Type: user Text: IMEI=865456054799968&MSG=User=FC000046;Pass=M2IP1385;&
    
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        return modem.sendHiGPS("/input.php?IMEI=865456054799968&MSG=User=BeniTest;Pass=M2IP1385;&")

class Phones(Commands):
    # Output Type: gprs Text:  0.0555 #+359888555197+359889916947+359882107103$
    # Input Type: eng Text: IMEI=865456054799968&User=BeniTest&Pass=M2IP1385&Description="BeniTest"
    #  Input Type: phones Text: IMEI=869139052340391&MSG=+359888555197;+359889916947;+359882107103;&
    def __init__(self, command):
        super().__init__(command)
        self.command = command
        #self.other = other
    #@staticmethod
    def return_result(self):
        my_command = self
        my_command = my_command.replace("#","")
        my_command = my_command.replace("$","")                                
        phones = my_command.split("+")
        phones = ["+"+x+";" for x in phones if len(x) >= 12] # the phones are here
        phones = "".join(phones)
        imei = modem.getImei()
        message = "/input.php?IMEI="+imei+"&MSG="+phones
        
        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()
        
        #print("command = ",self)
    
    def send_to_the_server(self):
        print("SMT")
        print(self)



class Mode(Commands):
    # If I need GPS in responce, call the GPS method! TRANS-3
    
    # Output Type: gprs Text:  0.0527 *MODE-0107000$
    # Input Type: mode Text: IMEI=865456054799968&MSG=SLEEP-0;WORK-1;CYCLE-0;TRANS-7;OHR-0;INPUT-OPEN;&
    
    def __init__(self, command:str):
        super().__init__(command)
        self.command = command



    def return_result(self):

        #modem.sendHiGPS("/input.php?IMEI=865456054799968&MSG=SLEEP-1;WORK-3;CYCLE-0;TRANS-7;OHR-1;INPUT-OPEN;&")
        my_command = self
        c = my_command.replace("*MODE-","")
        c = c.replace("$","")
        c = [x for x in c]  # !!! MODE IS HERE  !!!
        
        if c[5]== "0":
            inp = "OPEN"
        else:
            inp = "CLOSE"
    
        mode = "SLEEP-"+c[0]+";WORK-"+c[1]+";CYCLE-"+c[2]+";TRANS-"+c[3]+";OHR-"+c[4]+";INPUT-"+inp+";"

        imei = modem.getImei()
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
    def __init__(self, command):
        super().__init__(command)


    def return_result(self):
        print(f"ModeQ +")
        
class Loc(Commands):
    # Output Type: gprs Text:  0.0714 *LOC$
    # Input Type: loc Text: IMEI=865456054799968&User=BeniTest&Pass=M2IP1385&Description="BeniTest"865456054799968BAT-0,88,410LOCGSM:"0578","0740"3,"0046,30,11,08ea,284,01,0578"&
    
    def __init__(self, command):
        super().__init__(command)


    def return_result(self):
        #modem.sendHiGPS('/input.php?IMEI=865456054799968&User=BeniTest&Pass=M2IP1385&Description="BeniTest"865456054799968BAT-0,88,410LOCGSM:"0578","0740"3,"0046,30,11,08ea,284,01,0578"&')

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
        
class Gprs(Commands):
    # Output Type: gprs Text:  0.0752 *GPRS$
    # GPS :  https://www.higps.org/input.php?IMEI=865456054799968&User=F5100001&Pass=DOGPE2V3&Description=%22F5100001%22865456054799968BAT-0,35,3681GSM:%2206A4%22,%222C12%22&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&
    def __init__(self, command):
        super().__init__(command)
        #self.other = other        
     
    def send_GPS_to_the_server(): # return_result methot make the same
        gps = ''
        loc_info = ''
        gps = modem.gps()
        imei = modem.getImei()
        batt = modem.getBat()#[1]
        batt = ",".join(batt) # returns str    
        print("gps = ",gps)
        if gps != False:
            loc_info = modem.return_base64(gps)
        #message = "/input.php?IMEI="+imei+"&bat="+batt+"&GPSArray="+loc_info+"=&"
            message = "/input.php?IMEI="+imei+"&Description="+batt+"&GPSArray="+loc_info+"=&"
        else:
            # try to insert ENG
            name = "BeniTest"
            pas = "87654321"
            #eng = modem.getEng()
            eng = modem.parceCpsi()
            description = name+imei+"BAT-"+batt+"GPS-OFF"+"GSM:0000,FFFF"+eng  #  !!!   add "GPS-OFF"
            message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description

        modem.turnOffGPS()
        modem.cipClose()
        modem.connectHiGPS()
        print("connect = ",modem.isConnected())
        if modem.isConnected():
            print("MODEM IS CONNECTED")
            modem.sendHiGPS(message)
        else:
            print("MODEM NOT CONNECTED")
        modem.cipClose()


    def return_result(self):
        # send GPS to the server
        gps = ''
        loc_info = ''
        gps = modem.gps()
        imei = modem.getImei()
        batt = modem.getBat()#[1]   
        print("gps = ",gps)
        if gps != False:
            loc_info = modem.return_base64(gps)
        #message = "/input.php?IMEI="+imei+"&bat="+batt+"&GPSArray="+loc_info+"=&"
            message = "/input.php?IMEI="+imei+"&bat="+batt[1]+"&GPSArray="+loc_info+"=&"
        else:
            # try to insert ENG
            modem.turnOffGPS()
            modem.cipClose()
            name = "BeniTest"
            pas = "87654321"
            batt = ",".join(batt)
            #eng = modem.getEng()
            eng = modem.parseEng()
            description = name+imei+"BAT-"+batt+"GSM:0000,FFFF"+eng
            message = "/input.php?IMEI="+imei+"&User="+name+"&Pass="+pas+"&Description="+description

        modem.turnOffGPS()
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
    #
    def __init__(self, command):
        super().__init__(command)
        #self.other = other
        
    def send_eng_to_the_server(self):
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

    def return_result(self):
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
    


class Wifi(Commands):
    # 
    # Input Type: eng Text: IMEI=865456054799968&User=BeniTest&Pass=014_23_l&Description=BeniTest865456054799968BAT-0,33,3430GSM:0000,FFFF284,05,066f,2e55,53,066f,2f64,38,066f&wifij=[[-50,d8:50:e6:95:b9:d0,3],[-60,08:55:31:e7:02:82,1],[-61,0a:55:31:e7:02:82,1]]&data=307,1;216,1;264,0;290,0;&er=&
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass
    
class Start(Commands):
    #
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass
    
class Stop1(Commands):
    # Output Type: gprs Text:  0.0703 *STOP1$
    # Input Type: stop Text: IMEI=865456054799968&MSG=STOP1&
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

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
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass
class Get(Commands):
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass

    def get_samplings(self):
        #кой параметри по ID искаме да предаваме
        pass

    def get_samplingsAlarm(self):
        return self.get_samplings() + "440,1;"

    def get_dataBat(self):
        pass

    def get_data(self):
        pass

    def get_setting(self, id):
        pass

    def get_command(self, id):
        pass



def recogn_name(command):
    d = {"#User=":"User",
             "#+":"Phones",
         "*MODE-":"Mode",
        "*MODE?$":"ModeQ",
         "*GPRS$": "Gprs",
          "*GSM$": "Eng",
         "*ENG$" : "Eng"
        }
        
    class_name = ''
    for key in d:
        if key in command:
            class_name = d[key]
            # else:
            #     return "False"
    return class_name



def reading_command():
    modem.connectHiGPS()    
    com = modem.sendHiGPS("/input.php?IMEI=865456054799968").decode("utf-8")
    print("com= ", com)
    return com

def command_action(command):
    r = recogn_name(command)
    print("Class name == ",r)
    st = ".return_result('"+command+"')"  # add command as argument
    print("st = ", st)

    return eval(r + st)



def command_cicle():
    c = ""
    while not c == "OK":
        c = reading_command()
        if c == "OK":
            return "No more commands "
        command_action(c)
        
        
        





#a = Commands("*MODE?$")
#r = a.recognition_name()
#eval(r+".return_result(a)")

#b = Commands("*MODE-2468135$")
#rr = b.recognition_name()
#eval(rr+".return_result(b)")


