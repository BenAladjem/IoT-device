import machine
import config
import utime

from commands import *

from data import Database
from modem import Sim7070
from findyIoT import FindyIoT


modem = Sim7070()
d = Database()
f = FindyIoT()
class_instance = Commands("inst") # only make instance

#log = []
#spase = "                |"
#log_empty_row  = [spase]*4
#log_1_row = ["Main            |", "Command         |", "Modem           |", "DataBase        |"]
#log.append(log_1_row)
#log.append(log_empty_row)

def print_log(log):
    for row in log:
        print(row)

def beep():
    config.log.append("".join(["beep               |", spase, spase, spase]))
    pwm0 = machine.PWM(machine.Pin(27))
    pwm0.duty(50)
    pwm0.freq(3000)
    utime.sleep(0.5)
    pwm0.duty(0)
    
def write_batt_in_db(batt):
    d.write("223", batt)
    d.store()
    d.store()    


    
def write_gps(gps):
    for key in gps:
        d.write(key, gps[key])
        d.store()
        d.store()
        
def write_report_type(r_type):
    d.write("565", r_type)
    d.store()


def recogn_name(command):
    config.log.append("".join(["recogn_name     |", spase, spase, spase]))
    print("METHOD recogn_name()")
       
    class_name = ''
    for key in config.d:
        if key in command:
            class_name = config.d[key]
            # else:
            #     return "False"
    print("class name = ", class_name)
    return class_name



def reading_command(): #изпраща команда обръщение към сървъра, за да прочете чакаща команда, ако има
    config.log.append("".join(["reading_command |", spase, spase, spase]))
    print("METHOD reading_command()")
    modem.cipClose()
    modem.connectHiGPS()    
    com = modem.sendHiGPS("/input.php?IMEI=865456054799968")
    #modem.cipClose()
    print("com= ", com)
    if len(com) > 1 :
        com = com.decode("utf-8")
        
        return com
    else:
        return False

def command_action(command): # is calling method return_result
    config.log.append("".join(["command_action  |", spase, spase, spase]))
    print("METHOD command_action()")
    r = recogn_name(command)
    print("Class name == ",r)
    st = ".return_result('"+command+"')"  # add command as argument
    print("st = ", st)

    return eval(r + st)

def class_instan_method(command): # връща инстанция към класа, за който се отнася командата
    config.log.append("".join(["class_inst_met  |", spase, spase, spase]))
    print("METHOD class_instan()")
    class_name = recogn_name(command)
    return eval(class_name+"('"+command+"')")


def class_instance_action(command):# за тест генерира съобщение с нужните данни и ги изпраща към сървъра 
    config.log.append("".join(["class_instance_act   |", spase, spase, spase]))
    com = class_instance.return_result()
    if com == "223":
        mess = class_instance.get_dataBat()
        class_instance.send_msg_to_the_server(mess)

def command_cicle(): # чете и изпълнява чакащите команди от сървъра, докато има
    global class_instance
    config.log.append("".join(["command_cicle   |", spase, spase, spase]))
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
    
if modem.isOn() == False:
    print("Turning on modem")
    modem.turnOn()
    beep()

print("Check if modem is registered to network -> ", modem.isReg())

imei = modem.getImei()
batt = modem.getBat()[1]
#да проверя дали не е празна базата. Ако няма ИМЕИ, значи е празна
if not d.read("200"):
    print("not 200")
    d.initDefaults(imei)  # зарежда базата с имеи и дефолтни стойности
    d.store()


latitude = 42.674884  # 254
longitude = 23.289787  #255
msl_altitude = 592.877  #256
timestamp = 1669029794  #257
speed = 44.2  #258
gps_d = {"254": "42.674884", "255": "23.289787", "256": "592.877", "257": "1669029794", "258": "44.2"}
gps_def = {"254": "00", "255": "00", "256": "00", "257": "00", "258": "00"}
value = d.read("565")
print(value)