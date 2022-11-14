from modem import *
import utime

modem = Sim7070()

class Commands:
    global modem
    def __init__(self, command):
        self.command = command
        self.m = Sim7070()
        
        self.imei = self.m.getImei()
        self.batt = self.m.getBat()[1]

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
    
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass


class Mode(Commands):
    # If I need GPS in responce, call the GPS method! TRANS-3
    
    # Output Type: gprs Text:  0.0527 *MODE-0107000$
    # Input Type: mode Text: IMEI=865456054799968&MSG=SLEEP-0;WORK-1;CYCLE-0;TRANS-7;OHR-0;INPUT-OPEN;&
    
    def __init__(self, command:str):
        super().__init__(command)
        self.command = command

    def return_str_to_server(self):
        pass




    def return_result(self):
        self.mode_value = self.command[6:-1]
        # print(f"Mode {self.command[6:]}")
        print("Mode  "+self.mode_value)
        modem.sendHiGPS("/input.php?IMEI=865456054799968&MSG=SLEEP-2;WORK-2;CYCLE-0;TRANS-3;OHR-1;INPUT-OPEN;&")

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
        modem.sendHiGPS('/input.php?IMEI=865456054799968&User=BeniTest&Pass=M2IP1385&Description="BeniTest"865456054799968BAT-0,88,410LOCGSM:"0578","0740"3,"0046,30,11,08ea,284,01,0578"&')

class Gprs(Commands):
    # Output Type: gprs Text:  0.0752 *GPRS$
    # GPS :  https://www.higps.org/input.php?IMEI=865456054799968&User=F5100001&Pass=DOGPE2V3&Description=%22F5100001%22865456054799968BAT-0,35,3681GSM:%2206A4%22,%222C12%22&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&
    def __init__(self, command):
        super().__init__(command)
        #self.other = other
        
    def test(self):
        #global m
        #m = Sim7070()
        print(self.m.isOn())
        self.m.turnOnGPS()
        print(self.m.isOnGPS())
        print(self.m.getGPS())
        
     
    def try_to_get_gps(self):
        count = 0
        #global m
        #m = Sim7070()
        gps_dict = {"254":"", "255":"", "256": "", "257":"", "258":""}
        if self.m.isOnGPS() == "0":
            return "Turn GPS ON"
        while count < 50:
            res = self.m.getGPS()
            print("res = ",res)
            if res == "No GPS":
                utime.sleep(5)
            else:
                gps_dict["254"] = res[3]
                gps_dict["255"] = res[4]
                gps_dict["256"] = res[5]
                gps_dict["257"] = res[2]
                gps_dict["258"] = res[6]
                return gps_dict
            count += 1
        return False
    
    # connection to the server
    # get timestamp
    # make dict{timestamp:[lat, lon, speed]}
    # convert ubinascii.b2a_base64(locJSON)
    # return GPSArray=
    
    def return_base64(res):
        # res = [' 1', '1', '20221114101637.000', '42.675474', '23.289744', '621.057', '', '', '1', '', '500.0', '500.0', '500.0', '', '3', '', '5683.3', '189.4\r\n\r\nOK\r\n']
        t = res[2].split(".")[0]
        t = (int(t[0:4]), int(t[4:6]), int(t[6:8]), int(t[8:10]), int(t[10:12]), int(t[12:14]), 0, 0)

        timestamp = str(utime.mktime(t) + 946684800)

        loc_data = {}
        loc_data[timestamp] = [float(res[3]), float(res[4]), float(res[5])]
    #print(loc_data)

        locJSON = json.dumps(loc_data)
        loc64 = ubinascii.b2a_base64(locJSON)
        loc64 = loc64.decode("utf-8")
        loc64 = loc64.replace("\n", "")
        return loc64

    def return_result(self):
        print("something")
        
g = Gprs("L")

class Eng(Commands):
    #
    #
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass

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


def command_action(command):
    global a
    a = Commands(command)
    r = a.recognition_name()
    return eval(r + ".return_result(a)")

def reading_command():
    
    #modem.turnOn()
    #modem.connectHiGPS()
    
    com = modem.sendHiGPS("/input.php?IMEI=865456054799968").decode("utf-8")
    #com = modem.sendHiGPS("/input.php?IMEI=865456054799968&MSG=SLEEP-2;WORK-2;CYCLE-0;TRANS-3;OHR-1;INPUT-OPEN;&").decode("utf-8")

    print("com= ", com)
    return com

#a = Commands("*MODE?$")
#r = a.recognition_name()
#eval(r+".return_result(a)")

#b = Commands("*MODE-2468135$")
#rr = b.recognition_name()
#eval(rr+".return_result(b)")


