import machine
import config
import utime

from commands import*

from data import Database
from modem import Sim7070
from findyIoT import FindyIoT


modem = Sim7070()
d = Database()
f = FindyIoT()
class_instance = Commands("inst") # only make instance

num_col_in_log = 4
this_column = 0# в коя колона на лога да се записват данните
global log
global em_row
spase = config.spase
log = config.log


def print_log(log):
    for row in log:
        print(row)
        
def prt_log( log):
    for r in range(len(log)-1):
        row = log[r]
        row2 = log[r+1]
        print("".join(row))
        p1 = 0
        p2 = 0
        for i in range(len(row)):
            if row[i] != spase:
                p1 = i
                #print(row[i])
                #print(spase)
        for j in range( len(row2)):
            if row2[j] != spase:
                p2 = j
        if p1 != p2 and r > 1:
            sr = "arrow"+str(p1)+str(p2)
            # check the sr
            #print(sr)
            print("".join(config.arrows[sr]))
    print("".join(log[-1]))
        
def log_fill(method):
    if len(method) > 16:
        method = method[:16] + "|"
    elif len(method) < 16:
        method = method + " "*(16-len(method)) + "|"
    else:
        method = method +"|"
    em_row = [spase]*num_col_in_log
    em_row[this_column] = method
    #log.append("".join(em_row))
    log.append(em_row)        

def beep():
    log_fill("beep()")
    
    pwm0 = machine.PWM(machine.Pin(27))
    pwm0.duty(50)
    pwm0.freq(3000)
    utime.sleep(0.5)
    pwm0.duty(0)
    
def write_batt_in_db(batt):
    log_fill("write_batt_in_db()")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "write_batt_in_db() |"
    #log.append("".join(em_row))
    
    d.write("223", batt)
    d.store()
    d.store()    


    
def write_gps(gps):
    log_fill("write_gps()")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "write_gps()        |"
    #log.append("".join(em_row))
    for key in gps:
        d.write(key, gps[key])
        d.store()
        d.store()
        
def write_report_type(r_type):
    log_fill("write_rep_type()")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "write_rep_type()|"
    #log.append("".join(em_row))
    d.write("565", r_type)
    d.store()


def recogn_name(command):
    print("METHOD recogn_name()")
    log_fill("recogn_name()")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "recogn_name     |"
    #log.append("".join(em_row))
    
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
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "reading_command |"
    #log.append("".join(em_row))

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
    print("METHOD command_action()")
    log_fill("command_actionn()")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "command_action  |"
    #log.append("".join(em_row))
    
    r = recogn_name(command)
    print("Class name == ",r)
    st = ".return_result('"+command+"')"  # add command as argument
    print("st = ", st)

    return eval(r + st)

def class_instan_method(command): # връща инстанция към класа, за който се отнася командата
    print("METHOD class_instan()")
    log_fill("class_inst_meth()")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "class_inst_met  |"
    #log.append("".join(em_row))
    
    class_name = recogn_name(command)
    return eval(class_name+"('"+command+"')")


def class_instance_action(command):# за тест генерира съобщение с нужните данни и ги изпраща към сървъра 
    log_fill("class_instance_act")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "class_instance_act   |"
    #log.append("".join(em_row))
    
    com = class_instance.return_result()
    if com == "223":
        mess = class_instance.get_dataBat()
        class_instance.send_msg_to_the_server(mess)

def command_cicle(): # чете и изпълнява чакащите команди от сървъра, докато има
    
    global class_instance
    print("METHOD command_cicle()")
    log_fill("command_circle")
    #em_row = [spase]*num_col_in_log
    #em_row[this_column] = "command_cicle   |"
   # log.append("".join(em_row))
    #em_row = [spase]*4
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