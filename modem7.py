import machine
import config
import utime
import time

registrationStart = utime.time()
registrationTime = 0


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
            time.sleep(0.5)
            self.key.value(0)
            time.sleep(2)
            self.key.value(1)

        return True

    def turnOff(self):

        try:
            self.us("AT+CPOWD=1")
            time.sleep(2)
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
            time.sleep(0.5)
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
        time.sleep(0.1)
        time.sleep(t)
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
            # print(response)
            return True
        
    def getCPSI(self):  # copy
        
        eng =  self.us("AT+CPSI?",1).decode("utf-8")
        ee = eng.split("CPSI: ")
        self.us("AT+CENG=0")
        eng = ee[1]
        eng = eng.replace("\r","")
        eng = eng.replace("\n","")
        eng = eng.replace("+","")
        eng = eng.replace(" ",";")
        return eng
        
    def isConnected(self):  #copy
        if "SHSTATE: 1" in self.us('AT+SHSTATE?',1):
            return True
        elif "SHSTATE: 0" in self.us('AT+SHSTATE?',1):
            self.us('AT+SHCONN')
        elif "PDP DEACT" in self.us("AT+SHSTATE?",1) :
            self.turnOff()
            self.turnOn()
            if numb > 0:
                self.connectUDP(1)
        else:
            return False

    def getEng(self):

        self.us("AT+CENG=1,1")
        # self.us("AT+CENG?", 1)

        eng = self.us("AT+CENG?", 2).decode("utf-8").replace("+CENG: 1,1,", "")
        eng = eng.replace("+CENG: ", ",") #
        eng = eng.replace("AT+CENG?", "")
        eng = self.remov(eng)
        return eng

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
            return st
        else:
            return "No"

    def turnOnGPS(self):
        self.us("AT+CGNSPWR=1")
        gps = self.us("AT+CGNSPWR?").decode("UTF-8")
        return gps

    def turnOffGPS(self):
        self.us("AT+CGNSPWR=0")
        gps = self.us("AT+CGNSPWR?").decode("UTF-8")
        return gps

    def getGPS(self):
        self.us("AT")
        # b'AT+CGNSINF\r\r\n+CGNSINF: 1,1,20221021130421.000,42.674884,23.289787,592.877,,,1,,3.5,3.6,1.0,,3,,11864.6,143.4\r\n\r\nOK\r\n'

        if Sim7070.isOnGPS(self)[0] == "1":  # ако е вкл GPS
            print("OK,GPS is On")
        else:
            print("GPS is Off")
            return
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
            # return inf
        else:
            return "No"
        for i in range(len(parameters)):
            parameters_info[parameters[i]] = inf[i]

            print(parameters[i], inf[i])

        if parameters_info["Fix status = "]:
            return inf
        else:
            return "No GPS"
        
        
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
        global registrationTime
        global registrationStart
                
        connected = False
        retry = 3
        regRetry = 60
        while self.isReg() == False and regRetry >0:
            regRetry -= 1
            time.sleep(1)
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
        
        # Input Type: dataReport Text: IMEI=865456054799968&bat=91&data=254,42.675;255,23.29;258,0.0;256,614.0;519,7;257,1663079193;307,1;216,1;264,0;290,7347;&er=&
                    # modem.sendHiGPS("/input.php?IMEI=865456054799968&bat=91&data=254,42.675;255,23.29;258,0.0;256,614.0;519,7;257,1663079193;307,1;216,1;264,0;290,7347;&er=&")
        
        
        # GPS :  https://www.higps.org/input.php?IMEI=865456054799968&User=F5100001&Pass=DOGPE2V3&Description=%22F5100001%22865456054799968BAT-0,35,3681GSM:%2206A4%22,%222C12%22&GPS=$GNRMC,114315.000,A,4240.4835,N,02317.3902,E,1.26,200.42,070222,,,A*70&ACUM=&
        
        message = message.replace('"','')
        print("modem.sendUDP message:" )
        print(message)
        self.us("AT+CNACT?",1)  # CNACT APP Network Active
                                #Response
                                # +CNACT: <pdpidx>,<statusx>,<addressx>

        self.us('AT+CAOPEN=0,0,"TCP","in.higps.org",80',4)
                #AT+CAOPEN   Open a TCP/UDP Connection
        time.sleep(1)
        self.us('AT+CASEND=0,'+str(len(message)+6),1)
                # AT+CASEND  Send Data via an Established Connection
        self.us('GET '+message+'\r\n')
        self.us('AT+CAACK=0',1)
                # AT+CAACK  Query Send data information
        resp = self.us('AT+CARECV=0,512',1)
                #  AT+CARECV Receive Data via an Established Connection
        print(resp)
      
        print("resp")
        print(resp)
        try: 
            toret = self.getData(resp)
            print("Toret = " ,toret)
            if toret == False or toret == b'':
                time.sleep(1)
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
            #time.sleep(0.4)
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






