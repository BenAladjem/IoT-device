import machine
import config
import utime
#import time
import ubinascii
import json

registrationStart = utime.time()
registrationTime = 0


def beep():
    pwm0 = machine.PWM(machine.Pin(27))
    pwm0.duty(50)
    pwm0.freq(3000)
    utime.sleep(0.5)
    pwm0.duty(0)

class Sim7070(object):
    registrationStart = utime.time()
    registrationTime = 0

    def __init__(self):

        self.tx = config.PmodemTx
        self.rx = config.PmodemRx
        self.br = 9600
        self.pwr = machine.Pin(config.PmodemPower, machine.Pin.OUT)
        self.key = machine.Pin(config.PmodemPWRKey, machine.Pin.OUT)
        self.apn = config.apn  # "findy"
        self.uart = machine.UART(1, self.br, rx=self.rx, tx=self.tx, txbuf=1024, rxbuf=2048)

    def remov(self, text):
        l = ['\r', '\n', 'OK', '"']
        for el in l:
            if el in text:
                text = text.replace(el, "")
        return text

    def isOn(self):
        #self.uart = machine.UART(1, self.br, rx=self.rx, tx=self.tx, txbuf=1024, rxbuf=2048)
        self.us("AT")
        at = self.us("AT")

        self.us('AT+CNCFG=0,1,"' + self.apn + '"')  # защо е това?
        if "OK" in at:
            return True
        else:
            return False

    def turnOn(self):

        self.pwr.value(0)
        self.key.value(1)

        if self.isOn() == False:
            self.pwr.value(1)
            utime.sleep(0.5)
            self.key.value(0)
            utime.sleep(2)
            self.key.value(1)

        return True

    def turnOff(self):

        try:
            self.us("AT+CPOWD=1")
            utime.sleep(2)
            self.pwr.value(0)
            return self.pwr.value()
        except:
            return False

    def getBat(self):
        # My method for tests
        # b = b'AT+CBC\r\r\n+CBC: 0,73,3955\r\n\r\nOK\r\n'
        # c = b'AT+CBC=?\r\r\n+CBC: (0-2),(1-100),(voltage)\r\n\r\nOK\r\n'
        if not self.isOn():
            self.turnOn()

        while not self.isOn():
            utime.sleep(0.5)
        self.us("AT")
        command = "AT+CBC"
        wrong_command = "AT+CBC=?"
        responce = "+CBC: "
        text = "+CBC:"
        b = self.us("AT+CBC").decode("utf-8")
        b = self.remov(b)
        if command in b and responce in b and not wrong_command in b:
            bat = b.split(responce)[1]
            bat = bat.split(",")
            return bat
        else:
            return "No"

    def us(self, arg, t=0):

        answer = []

        self.uart.write(arg)
        self.uart.write(bytes([0x0d, 0x0a]))
        utime.sleep(0.1)
        utime.sleep(t)
        answer = self.uart.read();

        print(answer)
        if hasattr(answer, "decode"):
            return answer
        else:
            return "False"

    def isReg(self):

        if not self.isOn():
            return "Modem isn't turned ON"

        reg = self.us("AT", 0.1)
        response = self.us("AT+CPSI?", 0.2)

        if "+CME ERROR:" in response:
            return Exception
        elif "NO SERVICE" in response:
            print("No service")
            return False
        else:
            return True
        
    def getCPSI(self):  # copy
        
        eng =  self.us("AT+CPSI?",2).decode("utf-8")
        ee = eng.split("CPSI: ")
        self.us("AT+CENG=0")
        eng = ee[1]
        eng = eng.replace("\r","")
        eng = eng.replace("\n","")
        eng = eng.replace("+","")
        eng = eng.replace(" ",",")# changed ";" -> ","
                
        return eng
    

    def isConnected(self):
        
        status = self.us('AT+CNACT?',2).decode('utf-8')
        status = status.replace("AT+CNACT?", "")
        status = status.replace("+CNACT","")
        status = self.remov(status)
        print(status)
        status = status.split(':')[1:]
        status = [x.split(',') for x in status]
        if status[0][1] == "1":
            return True
        elif status[0][1] == "0":
            return False
        else:
            raise Exception("Wrong CNACT result")

    def getEng(self):
    	# test result 2g to the server 
        # b'AT+CENG?\r\r\n+CENG: 1,1,2,LTE CAT-M1\r\n\r\n+CENG: 0,"1550,339,-73,-47,-12,17,102,303617,284,05,255"\r\n+CENG: 1,"1550,414,-88,-51,-20,17"\r\n\r\nOK\r\n'
        # '1,LTE CAT-M1,0,1550,339,-73,-50,-9,20,102,303617,284,05,255'
        #[+CENG: <cell>,"<earfcn>,<pci>,<rsrp>,<rssi>,<rsrq>,<sinr>,<tac>,<cellid> ,<mcc>,<mnc>,<tx power>"<CR><LF>
        #           0        1      2      3      4      5      6     7       8       9     10      11      12  13
        # +CENG: <cell>,"<earfcn>,<pci>,<rsrp>,<rssi>,<rsrq>,<sinr>"...]OK
        
        # IMEI=860016041012985&User=QubiqoNB&Pass=Ver01_12&Description=QubiqoNB860016041012985BAT-0,90,4171
        # GSM:0000,FFFF,1,LTECAT-M10,1550,339,-84,-62,-11,5,102,303617,284,05,255&er=&regTime=11&
        
        self.us("AT+CENG=1,1")

        eng = self.us("AT+CENG?", 3).decode("utf-8").replace("AT+CENG?","")
        eng = eng.replace("+CENG: 1,1,", "")
        eng = eng.replace("AT+CENG?","")
        eng = self.remov(eng)        
        eng = eng.split("+CENG:")
        system = eng[0].split(",")
        cells = eng[1:]
        num_cells, system_mode = system[-2], system[-1]
        if "CAT" in system_mode or "NB" in system_mode:
            res = ","+"".join(eng)
            res = res.replace(" ","")            
            
        else:
            # GSM:"0000","FFFF",2,GSM0,"0977,38,63,0a56,284,01,0578"1,"0979,27,34,0a53,284,01,0578"
            # GSM:"0000","FFFF",3,GSM0,"0977,42,10,073e,284,01,0578"1,"0975,37,56,0716,284,01,0578"2,"0980,31,37,0755,284,01,044c
            #     GSM:0000,FFFF,3,GSM0,"0977,42,10,073e,284,01,0578"1,"0975,37,56,0716,284,01,0578"2,"0980,31,37,0755,284,01,044c"
            res = ","+"".join(eng)
            res = res.replace(" ","")
        self.us("AT+CENG=0")

        return res
    
    def parseCpsi(self):
        # check for gsm or cat-m or nb-iot
        const = 1
        while const < 4:            
            cpsi = self.getCPSI()
            cpsi = cpsi.split(",")
            const = len(cpsi)            

        system_mode = cpsi [0]

        if system_mode == "LTE":
            operation_mode, tac, cell_id, rssi = cpsi[1], cpsi[4], cpsi[5], cpsi[13]
            mcc,mnc = cpsi[3].split("-")
            cell_info = mcc+','+mnc+','+tac+','+cell_id+','+rssi
        else:
            operation_mode, tac, cell_id, rssi = cpsi[1], cpsi[4], cpsi[5], cpsi[13]
            mcc,mnc = cpsi[3].split("-")

        return cell_info
        
    def parseEng(self):
        '''
        eng = ''
        reg = False
        while not reg:
            eng = self.getEng()
            utime.sleep(0.5)
            reg = self.isReg()
        '''
        
        count = 1
        while count < 15:
            eng = self.getEng()
            l = len(eng.split(","))
            if l > 6:
                return eng
            utime.sleep(0.5)
            count += 1
        return False
    
    def getImei(self):
        if not self.isOn():
            return "Modem isn't turned ON"
        self.us("AT")
        command = "AT+GSN"

        imei = self.us("AT+GSN").decode("utf-8")
        imei = self.remov(imei)
        if command in imei:
            imei = imei.split(command)[1]
            return imei
        else:
            return "No"

    def getCCID(self):
        if not self.isOn():
            return "Modem isn't turned ON"
        self.us("AT")
        command = "AT+CCID"

        ccid = self.us("AT+CCID").decode("utf-8")
        ccid = self.remov(ccid)
        if command in ccid:
            ccid = ccid.split(command)[1]
            return ccid
        else:
            return "No"

    def isOnGPS(self):
        self.us("AT")
        command = "AT+CGNSPWR?"
        wrong_command = "ERROR"  # да напиша проверка
        responce = "+CGNSPWR: "
        st = self.us("AT+CGNSPWR?").decode("utf-8")
        st = self.remov(st)
        if command in st and responce in st:
            st = st.split(responce)[1]
            st = st.split(",")
        if st[0] == '1':
            return True
        elif st[0] == '0':
            return False
        else:
            return "Error"

    def turnOnGPS(self):
        self.us("AT+CGNSPWR=1")
        gps = self.us("AT+CGNSPWR?").decode("UTF-8")
        return gps

    def turnOffGPS(self):
        self.us("AT+CGNSPWR=0")
        gps = self.us("AT+CGNSPWR?").decode("UTF-8")
        print("GPS IS TURNED OFF")
        return gps
    
    def gps(self):
        self.us("AT+CGNSPWR=1")
        self.us("AT")        
        count_start = 0
        count_end = 2
        while count_start < count_end:
            command = "AT+CGNSINF"
            responce = "+CGNSINF:"
            inf = self.us("AT+CGNSINF", 2).decode("UTF-8")
            print("inf " + inf)
            if command in inf and responce in inf:
                inf = inf.split(responce)[1]
                inf = inf.split(",")
                inf = self.remov(inf)
            
            else:
                return "No"
            
            if inf[1]:
                self.turnOffGPS()
                return inf
            
            
            utime.sleep(4)
            count_start += 1
            print(count_start)
            if count_start >= count_end:
                self.turnOffGPS()
                return False
        

    def getGPS(self):
        
        self.us("AT+CGNSPWR=1")
        self.us("AT")
        # b'AT+CGNSINF\r\r\n+CGNSINF: 1,1,20221021130421.000,42.674884,23.289787,592.877,,,1,,3.5,3.6,1.0,,3,,11864.6,143.4\r\n\r\nOK\r\n'

        if Sim7070.isOnGPS(self)[0] == "1":  # ако е вкл GPS
            print("OK,GPS is On")
        else:
            print("GPS is Off")
            
            return
        
        #count_start = 0
        #count_end = 5
        #while count < count_end:
        parameters_info = {}
        command = "AT+CGNSINF"
        responce = "+CGNSINF:"
        inf = self.us("AT+CGNSINF", 2).decode("UTF-8")
        print("inf " + inf)
        parameters = ["GNSS run status = ", "Fix status = ", "UTC date & Time = ", "Latitude = ", "Longitude = ",
                      "MSL Altitude = ",
                      "Speed Over Ground = ", "Course Over Ground = ", "Fix Mode = ", "Reserved1 = ", "HDOP = ",
                      "PDOP = ", "VDOP = ",
                      "Reserved2 = ", "G NSS Satellites in View = ", "Reserved3 = ", "HPA = ", "VPA = "]

        if command in inf and responce in inf:
            inf = inf.split(responce)[1]
            inf = inf.split(",")
            
        else:
            return "No"
        for i in range(len(parameters)):
            parameters_info[parameters[i]] = inf[i]

            print(parameters[i], inf[i])
                     

        if parameters_info["Fix status = "]:
            location = []
            for key in ["Latitude = ", "Longitude = ", "MSL Altitude = "]:
                location.append(parameters_info[key])
            print(inf)
            print(location)
            '''
            l = {location[timestamp]:location}
            
            locJSON = json.dumps(location)
            print(locJSON)
            loc64 = ubinascii.b2a_base64(locJSON)
            loc64 = loc64.decode("utf-8")
            loc64 = loc64.replace("\n", "")
            print(loc64)
            '''   
            return inf
        else:
            return "No GPS"
        
    def return_base64(self, res):
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
        
        
    def getData(self,response):
        #resp = ['AT+CARECV=0,100\r', '+CARECV: 7,*SET,55', '', 'OK', '']
        #resp = ['AT+CARECV=0,100\r', '+CARECV: 0', '', 'OK', '', '+CADATAIND: 0', '', '+CASTATE: 0,0', '']
        #resp = ['AT+CARECV=0,100\r', '+CARECV: 5,15858', '', 'OK', '']
        
        resp = response.split(b'\r\n')
        n = 0
        for repons in resp : 
            if repons == b'AT+CARECV=0,512\r':
                break 
            else:
                n +=1


        
        if len(resp)>0:
        
            datalen =  int(resp[n+1][9:].split(b',')[0])
            print("Data len = ",datalen)
        else:
            return False

        ind = response.index(b'+CARECV: ')
        start = ind+10+len(str(datalen))
        end = start+datalen
        inp = response[start:end]

        return inp
    
    def connectHiGPS(self): 
    	# check if can't connect by LTE , try to change ->gsm network 2G
        global registrationTime
        global registrationStart
                
        connected = False
        retry = 5
        regRetry = 60
        while self.isReg() == False and regRetry >0:
            regRetry -= 1
            utime.sleep(1)
        registrationTime = utime.time() - registrationStart
        print("registration time = ",registrationTime)
        cnact = self.us('AT+CNACT=0,1',3).decode("utf-8")
                #AT+CNACT  APP Network Active
                #  <action> 0 Deactive; 1 Active  2 Auto Active
                
        print("cnact= ",cnact)
        while "DEACTIVE" in cnact  and retry >0 :
            deact = self.us('AT+CNACT=0,0',2)
            cnact = self.us('AT+CNACT=0,1',3).decode("utf-8")
            retry = retry -1 
        if "DEACTIVE" in cnact :                
            self.turnOff()
            self.turnOn() 

    def sendHiGPS(self,message):
        
        # modem.sendHiGPS("/input.php?IMEI="+"865456054799968"+"&bat="+'92'+"&data=2,1&alabala="+"This_is_test_data_message...")
        
        # server : IMEI=865456054799968&set=436,[48];&er=&regTime=4139&cpsi=LTE;CAT-M1,Online,284-05,0x0068,299524,236,EUTRAN-BAND3,1425,4,4,-11,-90,-69,12OK&
        
        # server :  IMEI=865456054799968&User=EconicNB&Pass=014_25_l&Description=EconicNB865456054799968BAT-0,-2,3387GSM:0000,FFFF284,01,62d4,86d5,26&wifij=[]&bat=-3&data=307,1;216,6;264,0;&wake_reason=GPIO_WAKE&reset_reason=DEEPSLEEP_RESET&er=&
        
        # command : modem.sendHiGPS("/input.php?IMEI="+"865456054799968"+"&User="+"BeniTest"+"&Pass="+"87654321"+"&bat="+'62'+"&data=2,1&DATA="+"254:42.674884,255:23.289787")
        
        # eng report : IMEI=865456054799968&User=EconicNB&Pass=014_23_l&Description=EconicNB865456054799968BAT-0,33,3430GSM:0000,FFFF284,05,066f,2e55,53,066f,2f64,38,066f&wifij=[[-50,d8:50:e6:95:b9:d0,3],[-60,08:55:31:e7:02:82,1],[-61,0a:55:31:e7:02:82,1]]&data=307,1;216,1;264,0;290,0;&er=&
        
        # eng command: modem.sendHiGPS("/input.php?IMEI=865456054799968&User=BeniTest&Pass=014_23_l&Description=BeniTest865456054799968BAT-0,33,3430GSM:0000,FFFF284,05,066f,2e55,53,066f,2f64,38,066f&wifij=[[-50,d8:50:e6:95:b9:d0,3],[-60,08:55:31:e7:02:82,1],[-61,0a:55:31:e7:02:82,1]]&data=307,1;216,1;264,0;290,0;&er=&")
        
        # Input Type: dataReport Text: /input.php?IMEI=865456054799968&bat=91&data=254,42.675;255,23.29;258,0.0;256,614.0;519,7;257,1663079193;307,1;216,1;264,0;290,7347;&er=&
        #  modem.sendHiGPS("/input.php?IMEI=865456054799968&bat=91&data=254,42.675;255,23.29;258,0.0;256,614.0;519,7;257,1663079193;307,1;216,1;264,0;290,7347;&er=&")
        
        
        # GPS :  https://www.higps.org/input.php?IMEI=865456054799968&User=F5100001&Pass=DOGPE2V3&Description=%22F5100001%22865456054799968BAT-0,35,3681GSM:%2206A4%22,%222C12%22&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&
        
        #eyIxNjY4MTc1MjM0IjogWzQyLjY3NDgxLCAyMy4yODk3OCwgMC4wXX0=
        
        message = message.replace('"','')
        print("modem.sendUDP message:" )
        print(message)
        self.us("AT+CNACT?",1)  # CNACT APP Network Active
                                #Response
                                # +CNACT: <pdpidx>,<statusx>,<addressx>

        self.us('AT+CAOPEN=0,0,"TCP","in.higps.org",80',4)
                #AT+CAOPEN   Open a TCP/UDP Connection
        
        
        while self.us("AT",1) != b'AT\r\r\nOK\r\n': 
            print("Wait")
            
            
        #AT+CAOPEN   Open a TCP/UDP Connection
        #utime.sleep(1)
        self.us('AT+CASEND=0,'+str(len(message)+6),1)
                # AT+CASEND  Send Data via an Established Connection
        self.us('GET '+message+'\r\n')
        self.us('AT+CAACK=0',1)
                # AT+CAACK  Query Send data information
        resp = self.us('AT+CARECV=0,512',1)
                #  AT+CARECV Receive Data via an Established Connection

        print("resp: ", resp)

        try: 
            toret = self.getData(resp)
            print("Toret = " ,toret)
            if toret == False or toret == b'':
                utime.sleep(1)
                resp = self.us('AT+CARECV=0,512',1)
                print("Retry read")
                toret = self.getData(resp)
            self.us("AT+CACLOSE=0")
            return toret
        except: 
            return False


        datalen = self.calcDataLen(resp)
        print("Data length = ",datalen)

        try: 

            resp = resp.split("\r\n")
            rep  = resp[1].split(",")
        except:
            resp = resp.split(b'\r\n')
            rep  = resp[1].split(b',')
        self.calcDataLen(resp)

        print(resp)

        print("REP")
        print(rep)
        return resp
        if len(resp) <4 :
            print("Fail 1")
            return False
        else:
            rep  = resp[3].split(",")

        if resp[1] == 'ERROR' or resp[3] == "ERROR" or len(rep)<2:
            print("Fail")
            return False
        elif rep[1] == '200':
            print("Success")            
            print(rep)
            #utime.sleep(0.4)
            datalen = rep[2]
            if int(datalen) > 10:
                serverResp  = self.us('AT+SHREAD=0,'+datalen,2)
            else:    
                serverResp  = self.us('AT+SHREAD=0,'+datalen)
            try:
                serverResp = serverResp.split("\r\n")
            except: 
                serverResp = serverResp.split(b'\r\n')
            print(serverResp)

        else: 
            print("Fail")
            return False
        datatoReturn =serverResp[4]
        idc = 4
        while int(datalen) > len(datatoReturn):

            print("Data too short")
            try:
                datatoReturn = serverResp[idc]+"\r\n"+serverResp[idc+1]
                idc = idc+1
            except : 
                break
        return datatoReturn
    
        
        
    def cipClose(self): # затваря конекцията към сървъра
        self.us("AT+CNACT=0,0")
        
    def sleep(self):
        self.dtr.value(1)

    def wakeUp(self):
        self.dtr.value(0)

    def limitNB(self):
        self.us("AT+CNMP=38")
        self.us("AT+CMNB=2")

    def limitCatM(self):
        self.us("AT+CNMP=38")
        self.us("AT+CMNB=1")

    def limit4G(self):
        self.us("AT+CNMP=38")
        self.us("AT+CMNB=3")

    def limit2G(self):
        self.us("AT+CNMP=13")

    def limitOFF(self):
        self.us("AT+CNMP=51")
        self.us("AT+CMNB=3")
        

    def getEngLite(self):

        self.us("AT+CENG=1,1")
        eng =  self.us("AT+CENG?",1).decode("utf-8").replace("+CENG: 1,1","")
        if "NO SERVICE" in eng:
            return "No Cells"
        eng = eng.replace("+CENG: ","")
        eng = eng.replace("AT+CENG?","")
        eng = eng.replace("OK","")
        eng = eng.replace('"',"")
        enn = eng.split("\r\n")
        xx = 3 
        cells = ""

        while xx <  len(enn):

            cell1 = enn[xx].split(",")
            if len(cell1) == 12: #LTE Network first Cell
                print("LTE first Cell")
                cells += cell1[9]+","+cell1[10]+","+cell1[7]+','+cell1[8]+','+cell1[4]
            elif len(cell1) == 7: #LTE Network second Cell
                
                 # Skip this one
                 print("Skip second LTE")
                #cells += ","+cell1[7]+","+cell1[4]+","+cell1[2]
            elif len(cell1) == 8: #2G Network 
                print("2G Cell")
                if xx==3:
                    cells += cell1[5]+","+cell1[6]
            
                cells += ","+cell1[7]+","+cell1[4]+","+cell1[2]

            xx +=1

        self.us("AT+CENG=0")
        #eng = ee[1]
        return cells 






