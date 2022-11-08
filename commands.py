from modem import *
import utime

class Commands:
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
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass

class Phones(Commands):
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass


class Mode(Commands):
    def __init__(self, command:str):
        super().__init__(command)
        self.command = command

    def return_str_to_server(self):
        pass




    def return_result(self):
        self.mode_value = self.command[6:-1]
        #print(f"Mode {self.command[6:]}")
        print("Mode  "+self.mode_value)

class ModeQ(Commands):
    def __init__(self, command):
        super().__init__(command)


    def return_result(self):
        print(f"ModeQ +")

class Gprs(Commands):
    
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
        

    def return_result(self):
        print("something")
        
g = Gprs("L")

class Eng(Commands):
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass

class Wifi(Commands):
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass
class Start(Commands):
    def __init__(self, command, other):
        super().__init__(command)
        self.other = other

    def return_result(self):
        pass
class Stop(Commands):
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

#a = Commands("*MODE?$")
#r = a.recognition_name()
#eval(r+".return_result(a)")

#b = Commands("*MODE-2468135$")
#rr = b.recognition_name()
#eval(rr+".return_result(b)")


