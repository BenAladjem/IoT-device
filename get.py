from modem import *
import utime

modem = Sim7070()
if modem.isOn() == False:
    print("Turning on modem")
    modem.turnOn()
    beep()

class Commands:
    CLASS_NAME = "Commands"
    global modem
    #global imei  #
    imei = modem.getImei()
    
    def __init__(self, command:str):
        self.command = command
        #self.m = Sim7070()
        
    def __repr__(self):
        return "class name : ",self.CLASS_NAME, "command : ", self.command        
        

    def recognition_other(self):
        other = 'other'
        return other
    
    
    def return_result(self):
        None
        
    def send_msg_to_the_server(self, message):
        print("class Commands:   method send_msg_to_the_server(): ")
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

    
class Get(Commands):
    CLASS_NAME = "Get"
    commands_dict = {
        "200":"",
        "217","",
        "218","",
        "219":"",
        "220":"",
        "221":"",
        "222":"",
        "223":"get_dataBat",
        "224":"",
        "225":"",
        "227":"",
        "228":"",
        "229":"",
        "312":"",
        "565":""
        
        }
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
        # description = "F5100001"865456054799968BAT-0,35,3681GSM:"06A4","2C12"&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&
        # message = IMEI=865456054799968&User=F5100001&Pass=DOGPE2V3&Description=+description
        name = "BeniTest"
        pas = "87654321"
        imei = self.imei
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

class_instance = Commands("inst") # only make instance

def recogn_name(command):
    print("METHOD recogn_name()")
    d = {"#User=":"User",
             "#+":"Phones",
         "*MODE-":"Mode",
        "*MODE?$":"ModeQ",
         "*GPRS$": "Gprs",
          "*GSM$": "Eng",
         "*ENG$" : "Eng",
         "*GET," : "Get"
        }
        
    class_name = ''
    for key in d:
        if key in command:
            class_name = d[key]
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

def command_action(command): # is calling method return_result WITHOUT INSTANCE
    print("METHOD command_action()")
    r = recogn_name(command)
    print("Class name == ",r)
    st = ".return_result('"+command+"')"  # add command as argument
    print("st = ", st)

    return eval(r + st)

def class_instance_return(command): # връща инстанция към класа, за който се отнася командата
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
        class_instance = class_instance_return(c)  # returns class instance

        class_instance.return_result()
        
        



        


