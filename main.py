import machine
#import config
from config import *
import utime
import gc

from modem import Sim7070
from commands import*

from data import Database

#from findyIoT import FindyIoT
#test дали ще се запамети

modem = Sim7070()

d = Database()
#f = FindyIoT()
#class_instance = Commands("inst") # only make instance
gc.enable()

this_column = 0# в коя колона на лога да се записват данните
#global log
#global em_row
#spase = config.spase
#log = config.log
#num_col = config.num_col

'''
def pr_log(log):
    for row in log:
        print("".join(row))
'''        
        
def log_fill(method):
    if len(method) > 18:
        method = method[:18] + "|"
    elif len(method) < 18:
        method = method + " "*(18-len(method)) + "|"
    else:
        method = method +"|"
    em_row = [spase]*num_col
    em_row[this_column] = method
    log.append(em_row)
    
def log_gc(method):
    method = str(method)
    if len(method) > 18:
        method = method[:18] + "|"
    elif len(method) < 18:
        method = method + " "*(18-len(method)) + "|"
    else:
        method = method +"|"
    em_row = [spase]*num_col
    em_row[5] = method
    log.append(em_row)
    
def arrow_row(a, b):
    if any([a<0, b<0, a>num_col, b>num_col]):
        return False
    row = []
    if a<b:
        for i in range(num_col):
            if i<a or i>b:
                row.append(spase)
            elif i>a and i < b:
                row.append(line)
            elif i == a:
                row.append(line_r)
            elif i == b:
                row.append(arrow_r)
    elif a>b:
        for i in range(num_col):
            if i>a or i<b:
                row.append(spase)
            elif i<a and i > b:
                row.append(line)
            elif i == a:
                row.append(line_l)
            elif i == b:
                row.append(arrow_l)
                            
    print("".join(row))
    
def print_log():
    for r in range(len(log)-1):
        row = log[r]
        row2 = log[r+1]
        print("".join(row))
        p1 = 0
        p2 = 0
        for i in range(len(row)):
            if row[i] != spase:
                p1 = i
        for j in range(len(row2)):
            if row2[j] != spase:
                p2 = j
        if p1 != p2 and r > 1:
            arrow_row(p1, p2)

    print("".join(log[-1]))

def beep():
    log_fill("beep()")
    
    pwm0 = machine.PWM(machine.Pin(27))
    pwm0.duty(50)
    pwm0.freq(3000)
    utime.sleep(0.5)
    pwm0.duty(0)
    
def write_batt_in_db(batt):
    log_fill("write_batt_in_db()")
    
    d.write("223", batt)
    d.store()
    d.store()    


    
def write_gps(gps):
    log_fill("write_gps()")
    for key in gps:
        d.write(key, gps[key])
        d.store()
        d.store()
        
def write_report_type(r_type):
    log_fill("write_rep_type()")
    d.write("565", r_type)
    d.store()


def recogn_name(command):
    print("METHOD recogn_name()")
    log_fill("recogn_name()")
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
    class_name = ''
    for key in config.d:
        if key in command:
            class_name = config.d[key]
            # else:
            #     return "False"
    print("class name = ", class_name, " : type = ", type(class_name))
    return class_name



def reading_command(): #изпраща команда обръщение към сървъра, за да прочете чакаща команда, ако има
    print("METHOD reading_command()")
    log_fill("reading_command()")

    modem.cipClose()
    modem.connectHiGPS()    
    com = modem.sendHiGPS("/input.php?IMEI=865456054799968")
    modem.cipClose()
    print("com= ", com)
    if com == False:
        raise Exception("Connection error")
    if len(com) > 1:
        com = com.decode("utf-8")
        
        return com
    else:
        return False
'''
def command_action(command): # is calling method return_result
    print("METHOD command_action()")
    log_fill("command_actionn()")
    
    r = recogn_name(command)
    print("Class name == ",r)
    st = ".return_result('"+command+"')"  # add command as argument
    print("st = ", st)

    return eval(r + st)
'''

def command_action(command): # is calling method return_result
    print("METHOD command_action()")
    log_fill("command_actionn()")

    st = class_instance.CLASS_NAME+".return_result('"+command+"')"  # add command as argument
    print("class/ret_res = ", st)

    return eval(st)

def class_instan_method(command): # връща инстанция към класа, за който се отнася командата
    print("METHOD class_instan()")
    log_fill("class_inst_meth()")
    
    class_name = recogn_name(command)
    return eval(class_name+"('"+command+"')")


def class_instance_action(command):# за тест генерира съобщение с нужните данни и ги изпраща към сървъра 
    log_fill("class_instance_act")
    
    com = class_instance.return_result()
    if com == "223":
        mess = class_instance.get_dataBat()
        class_instance.send_msg_to_the_server(mess)

def command_cycle(): # чете и изпълнява чакащите команди от сървъра, докато има
    
    global class_instance
    print("METHOD command_cicle()")
    log_fill("command_circle")

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
        log_gc(gc.mem_free())
        #print(class_instance.command)
        #print("TRANCE = ", class_instance.command)
        
        command_action(c)
        log_gc(gc.mem_free())
        #class_instance_action(c)
        #class_instance.send_to_the_server(x)
    




log_gc(gc.mem_free())
modem.turnOn()

if modem.isOn() == False:
    print("Turning on modem")
    while not modem.isOn():
        modem.turnOn()
        beep()
print("Check if modem is registered to network -> ", modem.isReg())

imei = modem.getImei()
class_instance = Commands(imei)
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
#command_cycle()
#print_log()