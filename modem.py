import machine
import config
import utime


from data import Database
from modem import Sim7070
from findyIoT import FindyIoT
modem = Sim7070()

d = Database()

f = FindyIoT()

def beep():
    pwm0 = machine.PWM(machine.Pin(27))
    pwm0.duty(50)
    pwm0.freq(3000)
    utime.sleep(0.5)
    pwm0.duty(0)

if modem.isOn() == False:
    print("Turning on modem")
    modem.turnOn()
    beep()
    #while not modem.isOn():
        #utime.sleep(0.5)

print("Check if modem is registered to network", modem.isReg())

imei = modem.getImei()
#imei = '2111111111111'
#да проверя дали не е празна базата. Ако няма ИМЕИ, значи е празна
if not d.read("200"):
    print("not 200")
    d.initDefaults(imei)  # зарежда базата с имеи и дефолтни стойности
    d.store()
#ccid = modem.getCCID()
batt = modem.getBat()[1]
#batt = '66'

latitude = 42.674884  # 254
longitude = 23.289787  #255
msl_altitude = 592.877  #256
timestamp = 5  #257
speed = 44.2  #258
gps_d = {"254": "42.674884", "255": "23.289787", "256": "592.877", "257": "5", "258": "44.2"}
gps_def = {"254": "00", "255": "00", "256": "00", "257": "00", "258": "00"}
value = d.read("565")
print(value)

    

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
    
def try_to_get_gps():
    # only for database
    count = 0
    gps_dict = {"254":"", "255":"", "256": "", "257":"", "258":""}
    if modem.isOnGPS() == "No":
        return "Turn GPS ON"
    while count < 20:
        res = modem.getGPS()
        if res == "No GPS":
            utime.sleep(5)
        else:
            gps_dict["254"] = res[3]
            gps_dict["255"] = res[4]
            gps_dict["256"] = res[5]
            gps_dict["257"] = res[2].split(".")[0]
            gps_dict["258"] = res[6]
            
            return gps_dict
        count += 1
    return False

def try_while_get_gps():
    count = 0
    while count < 5:
        res = modem.getGPS()
        if res == "No GPS":
            utime.sleep(5)
        else:
            return res
            
        count += 1
        
        if count == 5:
            return False



def reading_command():
    
    #modem.turnOn()
    #modem.connectHiGPS()
    
    com = modem.sendHiGPS("/input.php?IMEI=865456054799968").decode("utf-8")
    #com = modem.sendHiGPS("/input.php?IMEI=865456054799968&MSG=SLEEP-2;WORK-2;CYCLE-0;TRANS-3;OHR-1;INPUT-OPEN;&").decode("utf-8")

    print("com= ", com)
    
def send_GPS_to_the_server():
    x = ''
    loc_info = ''
    x = modem.gps()
    #print(x)
    if x:
        loc_info = modem.return_base64(x)
    print(loc_info)
    #print(type(loc_info))
    print(batt)
    #print(type(batt))
    
    # IMEI=865456054799968&bat=77&GPSArray=WyI0Mi42NzQ4NjMiLCAiMjMuMjg5ODM1IiwgIjYwNC44NDciXQ=&
    message = "/input.php?IMEI="+imei+"&bat="+batt+"GPSArray="+loc_info
    print(message)
    modem.connectHiGPS()
    modem.sendHiGPS(message)
    
    
print("/input.php?IMEI="+imei+"&bat=")
    
#message = ("/input.php?IMEI="+str(imei))#+"&bat="+str(batt)+"GPSArray="+loc_info
#print("message = "+ messaage)
   
  