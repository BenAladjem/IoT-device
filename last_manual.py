noReg = 0
Gimei = "0"
Glocations = b''
timeStart = 0 
distance = 0 


apn = "findy"
PmodemPower = 26
PmodemPWRKey = 23
PmodemTx = 32
PmodemRx = 21
PmodemStatus = 22
PmodemDTR = 33
PmodemRing = 13


Psda = 18
Pscl = 19
PperipherialPower = 25
Pbuzzer = 27
Pinput14 = 14
Pinput4 = 4
Preed = 2

#datalist = ['443','421']
datalistGPS = ["421",'443',"521"]
datalist = ["421",'443',"521"]



import time
import utime
import gc
import machine
from machine import mem32
import struct

wakeCause = "Unknown"
resetCause ="Unknown"
causeSent = False
errors = ""
errorsSent = True
connectionSuccess = False

registrationStart = utime.time()
registrationTime = 0
timestamp = 0
def wdtAlert(p):
    print("WDT Reset")
    machine.reset()
wdt = machine.Timer(10)
wdt.init(period=120000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
   
class sim7070(object):
    
    
    def __init__(self):


        #,power,key,tx,rx,br
        #self.pwr = machine.Pin(power,machine.Pin.OUT)

        self.key = machine.Pin(PmodemPWRKey,machine.Pin.OUT)
        self.key.value(1)
        self.tx = PmodemTx
        self.rx = PmodemRx
        self.br = 9600
        self.apn = apn


        
        self.pwr = machine.Pin(PmodemPower,machine.Pin.OUT)
        self.status = machine.Pin(PmodemStatus, machine.Pin.IN)
        self.dtr = machine.Pin(PmodemDTR, machine.Pin.OUT)
        self.ri = machine.Pin(PmodemRing, machine.Pin.IN)
        

        
        self.dtr.value(0)
        return


    def isOn(self):
        
        self.uart = machine.UART(1,self.br, rx=self.rx, tx=self.tx, txbuf=1024,rxbuf=2048)

        self.us("AT")
        
        at = self.us("AT")
        if type(at)  != bytes and type(at) != str:
            return False
        self.us('AT+CNCFG=0,1,"'+self.apn+'"')
        if  "OK" in at:        
            return True
        else :
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

            
            #time.sleep(10)
            self.us("AT",0.5)
            self.us("AT",0.5)
            
            x = 0
            time.sleep(1)
            #self.us('AT+COPS=1,2,"28401",9',2)
            self.limitCatM()
            self.us('AT+CNCFG=0,1,"'+self.apn+'"',1)
            self.us('AT+CCID')
            self.us('AT+CNCFG=0,1,"'+self.apn+'"',1)
            #self.limitCatM()
            
            if self.isReg():
            
                
                self.us('AT+CNCFG=0,1,"'+self.apn+'"')
            else:
                #self.us('AT+COPS=1,2,"28401",9',2)
                #self.us('AT+COPS=1,2,"28405",7',1)
                while x <0 :

                    if self.isReg():
                        time.sleep(1)

                        self.us('AT+CNCFG=0,1,"'+self.apn+'"')
                        return
                    else:
                        time.sleep(1)
                    x = x+1
                #self.us("AT+CMCFG=1")
                #self.us("AT+CNMP=51")
                #self.us("AT+CMNB=1")
                #self.us("AT+CCID")

            return True

    def turnOff(self):
        
        
        try: 
            self.us("AT+CPOWD=1")
            
            time.sleep(2)
            self.pwr.value(0)
            return self.pwr.value()
        except :
            return False
        #else :
        #    return True
    
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


    def isReg(self):

        global noReg 
        noReg = 0 
       # return True
        
        if self.us("AT",0.1) is not None :
            if  'NO SERVICE' in self.us('AT+CPSI?'):
                noReg += 1
                return False
            else:

                noReg = 0 
                return True
            
        else :
            print("None from isReg()")
            if self.isOn():
                return False
            else : 
                self.turnOff()
                self.turnOn()
                return False
                
    def getEng(self):
        #b'AT+CENG?\r\r\n+CENG: 1,1,1,LTE NB-IOT\r\n\r\n+CENG: 0,"3700,29,-74,-72,-3,12,199,8381899,284,01,255"\r\n\r\nOK\r\n'

        self.us("AT+CENG=1,1")
        eng =  self.us("AT+CENG?",1).decode("utf-8").replace("+CENG: 1,1","")
        ee = eng.split("CENG: ")
        self.us("AT+CENG=0")
        #eng = ee[1]
        eng = eng.replace("\r","")
        eng = eng.replace("\n","")
        eng = eng.replace("+CENG: ","")
        eng = eng.replace("AT+CENG?","")
        eng = eng.replace("OK","")


        
        return eng
    def getEngLite(self):

        self.us("AT+CENG=1,1")
        eng =  self.us("AT+CENG?",1).decode("utf-8").replace("+CENG: 1,1","")
        
        eng = eng.replace("+CENG: ","")
        eng = eng.replace("AT+CENG?","")
        eng = eng.replace("OK","")
        eng = eng.replace('"',"")
        enn = eng.split("\r\n")
        xx = 3 
        cells = ""

        while xx <  len(enn):

            cell1 = enn[xx].split(",")
            if xx==3:
                cells += cell1[5]+","+cell1[6]
            if len(cell1) == 8 :
                cells += ","+cell1[7]+","+cell1[4]+","+cell1[2]

            xx +=1

        self.us("AT+CENG=0")
        #eng = ee[1]
        return cells        


    def getImei(self):
        self.us("AT")
        imei = self.us("AT+GSN").decode("utf-8")
        imei = imei.replace("AT+GSN","")
        imei = imei.replace("\r","")
        imei = imei.replace("\n","")
        imei = imei.replace("OK","")
        return imei
    def getCCID(self):
        self.us("AT")

        ccid = self.us("AT+CCID").decode("utf-8")
        ccid = ccid.replace("AT+CCID","")
        ccid = ccid.replace("\r","")
        ccid = ccid.replace("\n","")
        ccid = ccid.replace("OK","")
        return ccid
    def getBat(self):
        self.us("AT")
        bat = self.us("AT+CBC").decode("utf-8")
        bat = bat.replace("AT+CBC","")
        bat = bat.replace("\r","")
        bat = bat.replace("\n","")
        bat = bat.replace("OK","")
        bat = bat.replace("+CBC: ","")
        spl = bat.split(",")
        
        
        #self.fillEng()
        return spl

    def isConnected(self):
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





    def getTime(self):
        
        self.us("AT")
        localTime = self.us("AT+CCLK?").decode("utf-8")
        #'AT+CCLK?\r\r\n+CCLK: "20/11/23,13:31:58+00"\r\n\r\nOK\r\n'
        parsedTime = self.parseTime(localTime)
        if parsedTime :
            return parsedTime
        else:
            #self.us('AT+SAPBR=1,1',1)

            self.us('AT+CNTPCID=0',2)
            self.us('AT+CNTP="0.bg.pool.ntp.org",0',2)
            self.us("AT+CNTP",2)
            localTime = self.us("AT+CCLK?",1).decode("utf-8")
            parsedTime = self.parseTime(localTime)

            return parsedTime
    def getTimeF(self):
        self.us("AT")
        self.connectHiGPS(1)
        tim = self.sendHiGPS("/t/")
        try:
            return tim.decode("utf-8")
        except:
            return False

    def parseTime(self,timeString):
        import utime

        timeString = timeString.replace("\r","")
                                     
        timeString = timeString.replace("\n","")
        ee = timeString.split('"')        
        time = ee[1].split("/")
        year = "20"+time[0]
        if (year == '2080'):
            return False
        month = time[1]
        dateTime = time[2].split(",")
        date = dateTime[0]
        time = dateTime[1].split("+")[0].split(":")
        hour = time[0]
        minutes = time[1]
        second = time[2]

        
        from machine import RTC 
        t = (int(year),int(month),int(date),0,int(hour),int(minutes),int(second),0)
        clock = RTC()
        clock.datetime(t)


        t = (int(year),int(month),int(date),int(hour),int(minutes),int(second),0,0)
        print(t)
        return utime.mktime(t)+946684800

    def getCPSI(self):
        
        eng =  self.us("AT+CPSI?",1).decode("utf-8")
        ee = eng.split("CPSI: ")
        self.us("AT+CENG=0")
        eng = ee[1]
        eng = eng.replace("\r","")
        eng = eng.replace("\n","")
        eng = eng.replace("+","")
        eng = eng.replace(" ",";")
        return eng
    def connectHiGPS(self,num): 
            global registrationTime
            global registrationStart
                
            connected = False
            retry = 3
            regRetry = 60
            while self.isReg() == False and regRetry >0:
                regRetry = regRetry-1
                time.sleep(1)
            registrationTime = utime.time() - registrationStart
            print("registration time = ",registrationTime)
            cnact = self.us('AT+CNACT=0,1',3).decode("utf-8")
            while "DEACTIVE" in cnact  and retry >0 :
                deact = self.us('AT+CNACT=0,0',2)
                cnact = self.us('AT+CNACT=0,1',3).decode("utf-8")
                retry = retry -1 
            if "DEACTIVE" in cnact :                
                self.turnOff()
                self.turnOn()


            
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

    def sendHiGPS(self,message):
        message = message.replace('"','')
        print("modem.sendUDP message:" )
        print(message)
        self.us("AT+CNACT?",1)  # CNACT APP Network Active


        self.us('AT+CAOPEN=0,0,"TCP","in.higps.org",80',4)
        time.sleep(1)
        self.us('AT+CASEND=0,'+str(len(message)+6),1)
        self.us('GET '+message+'\r\n')
        self.us('AT+CAACK=0',1)
        resp = self.us('AT+CARECV=0,512',1)
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
        
    def cipClose(self):
        

        self.us("AT+CNACT=0,0")
        
    def us(self,arg,t=0):
        
        #print(arg)
        answer = []
    
        self.uart.write(arg)
        self.uart.write(bytes([0x0d,0x0a]))
        time.sleep(0.1)
        time.sleep(t)
        answer = self.uart.read();
        
        print(answer)
        if hasattr(answer,"decode"):
            return answer
        else:
            return "False"
class database(object):
    def __init__(self):
        
        import btree
        import uos
        self.newdata = False

        #key = higpsID
        #param[0] = Allowed operations - R (read), W (read-write), E (execute)
        #param[1] = Type: 1 - number, 0 - string, 2 - boolean, 9 - function
        #param[2] = Storage: 0 - file system, 1 - RAM, 2 - Function 
        #param[3] = Path = 0 - default / function name
        #param[4] = Default value
        database.params = {"200":["R",1,0,0,"0","R"],"51":["W",0,0,0,"0","R"],"52":["E",9,2,"update()","0","R"],"53":["R",1,1,0,"0","R"],"54":["R",1,1,0,"0","R"],"55":["E",9,2,"downloadUpdate()","0","R"],"217":["R",0,1,0,"findy IoT","R"],"218":["R",0,1,0,"q-wm-01","R"],"219":["R",9,2,"serialNumber()","123","R"],"220":["R",0,1,0,"1.02","R"],"221":["E",9,2,"restart()","0","R"],"222":["E",9,2,"factoryReset()","0","R"],"223":["R",2,1,0,"0","R"],"224":["R",2,1,0,"0","R"],"225":["R",5,0,0,"0","R"],"227":["R",0,1,0,"waterMeter","R"],"228":["R",0,1,0,"1","R"],"229":["R",0,1,0,"1","R"],"312":["E",9,2,"get_settings()","0","R"],"420":["W",0,0,0,"0","R"],"421":["W",0,0,0,"300","R"],"422":["W",0,0,0,"2","R"],"423":["W",0,0,0,"1","R"],"440":["R",1,1,0,"0","R"],"441":["R",0,1,0,"0","R"],"442":["R",0,1,0,"0","R"],"443":["R",0,0,0,"0","R"],"520":["R",0,1,0,"0","R"],"521":["R",0,0,0,"0","R"],"522":["R",0,0,0,"0","R"],"523":["W",0,0,0,"3.9","W"],"524":["W",0,0,0,"20","W"],"525":["W",0,0,0,"0","W"],"553":["W",0,0,0,"4","W"],"554":["W",0,0,0,"20","W"],"555":["W",0,0,0,"0","W"],"556":["W",0,0,0,"6","W"]}
        try:
            try:
                f = open("vfs1/mydb", "r+b")
            except OSError:
                f = open("vfs1/mydb", "w+b")        
            db = btree.open(f)
            self.data = {}
            for key in db:
                #if data[key][1] == 0
                self.data[key] = db[key]

            db.flush()
            db.close()
            f.close()
        except:
            print("Exception")
            return False
            
            

    def getParameterData(self,uri):
        try:
            #if 
            return self.params[uri]
        except:
            return False
    
    def getParameterByHiGPS(self,higpsId):
        print("in get parameter by HiGPS")
        print(higpsId)
        try:
            return self.params[higpsId]
        except:
            return False   



    def initDefaults(self):
        import os
        if len(self.data) > 0:
            os.remove('vfs1/mydb')
        
        
        
            print("old db removed")
            utime.sleep(5)
            machine.reset()
        else:
            print("no previous DB ")
        n = 0
        imei = '2111111111111'
        while n< 3 and len(imei) != 15:  
            imei = modem.getImei()
            n +=1

        
        self.newdata = True
        for higpsID in self.params:
            if self.params[higpsID][4] != None and self.params[higpsID][2] == 0:
                if higpsID == "200":
                    self.write(higpsID,imei)    
                else:
                    self.write(higpsID,self.params[higpsID][4])



    def read(self,property,echo=True):
        import btree

        try:
            if type(property) == str :
                property = str.encode(property)
            if echo:
                print("Reading "+str(property)+ " = " + str(self.data[property]))
            return self.data[property]
            
        except:
            return False


    def write(self,property,value):
        self.newdata = True
        try:
            if type(value) == int: 
                value = str(value)
            if type(value) == str:
                value = str.encode(value)
            if type(property) == str:
                property = str.encode(property)
            print("Writing "+str(property)+ " = " + str(value))
            self.data[property] = value

            return True
        except:
            return False
    def store(self):
        if self.newdata == False:
            print("No data to write")
            return True


        try:
            import btree
            print("Database store started")
            try:
                f = open("vfs1/mydb", "r+b") 
            except OSError:
                f = open("vfs1/mydb", "w+b")
            db = btree.open(f)

            for key in self.data:
                if self.params[key.decode('utf-8')][2] == 0:
                    db[key] = self.data[key]
                
            db.flush()
            db.close()
            f.close()
            print("Database store completed")
            return True
        except Exception as e:

            print("Failed writing in database ",e)
            return False
class findyIoT(object):
    def __init__(self):
        
        
        findyIoT.requestType = ""
        findyIoT.responceType = ""
        #higps.modem = modem #sim7000(26,23,32,21,9600)
        imei =db.read('200')
        if imei == False:
            findyIoT.imei = False
        else :
            findyIoT.imei = imei.decode("utf-8")
        #higps.modem.isOn()
    def main(self,command,execute = True):
        
        global lastReportTime
        while command:
            command = self.send(command,execute)

            
            
        lastReportTime = utime.time()
        print("Last report was on ")
        print(lastReportTime)
        return command
    def send(self,commandtype,execute):
        import utime
        global lastReportTime
        global errors
        global errorsSent
        global connectionSuccess
        global registrationTime
        global timestamp
        connectionSuccess = False
        if "," in commandtype :
            spl = commandtype.split(",")
            commandtype = spl[0]
            parameter  = spl[1]
            symbols = {"self": self,"parameter" : parameter}

            data = eval("self.get_"+commandtype+"(parameter)", symbols)
        else: 
            symbols = {"self": self}   
            data = eval("self.get_"+commandtype+"()", symbols)
        modem.connectHiGPS(2)
        cpsi = modem.getCPSI()
        response = modem.sendHiGPS('/input.php?'+data+"&er="+errors.replace(' ','%')+"&regTime="+str(registrationTime)+"&cpsi="+cpsi)
        #timestamp = modem.sendHiGPS('/t/')
        #print(timestamp)
        #modem.cipClose()
        print("Response in send")
        print(response)
        if response == False:
            print("retry")
            if modem.isOn():
                modem.connectHiGPS(2)
                response = modem.sendHiGPS('/input.php?'+data)#+"&error="+errors.replace(' ','%'))
                
        

        
        
        if response:
            response = response.decode("utf-8")
            connectionSuccess = True
            print("SENT OK") 
            
            errorsSent = True
            errors = ""
            command = self.parse(response)
            #global wdt
            #wdt.feed()

            print(command)
            # ok
        else : 
            command = False


        print(command)
        if execute:
            timestamp = modem.sendHiGPS('/t/')
            print(timestamp)
            decodedTs = timestamp.decode("utf-8")
            if len(decodedTs) == 10: 
                ttt=time.localtime(int(decodedTs)-946684800)
                machine.RTC().init((ttt[0],ttt[1],ttt[2],0,ttt[3],ttt[4],ttt[5],0))
                print(machine.RTC().datetime())
        modem.cipClose()
        if command  and execute :

            symbols = {"self": self,"data": response} 
            return eval("self.set_"+command+"(data)", symbols)
        #else:
        #    return command

   
		# определя вида на командата, дошла от сървъра и какво да прави
    def parse(self,rsp) :

        #from machine import WDT
        #wdt = WDT(timeout=2000)  # enable it with a timeout of 2 seconds
        #wdt.feed()
        
        
        if "#" in rsp :
            
            if "#User=" in rsp : 
                parsed = "user"
            elif "#+" in rsp : 
                parsed ="phones"
            else :
                parsed =False
        elif "*" in rsp:

            if "*MODE-" in rsp : 
                parsed ="mode"
            elif "*MODE?$" in rsp : 
                parsed ="modeQ"
            elif "*GPRS$" in rsp : 
                parsed ="gprs"
            elif "*GSM$" in rsp : 
                parsed ="eng"
            elif "*WIFI$" in rsp : 
                parsed ="wifi" 
            elif "*START" in rsp :     
                parsed ="start" 
            elif "*STOP" in rsp :     
                parsed ="stop" 
            elif "*SET" in rsp: 
                parsed = 'set' 
            elif "*GET" in rsp: 
                parsed = 'get' 
            else : 
                parsed =False
        else : 
            parsed = False
            #       print(parsed)
        return parsed

    def set_set(self,response): # когато от сървъра идва команда със set
        print(response)
        #response = response.decode("latin-1", 'ignore')
        response = response.replace('$','')
        splitted = response.split(",")
        if len(splitted) == 2 : 
            print("Execute command")
            print(splitted[1])
            parameterData = db.getParameterByHiGPS(splitted[1])
            print(parameterData)
            if(parameterData[0] == "E"):
                
                
                print(parameterData[3])
                
                #eval("device.device.memoryTotal()")
                eval("self."+parameterData[3])
                #return "command,"+str(splitted[1])

            #execute
        elif len(splitted) == 3 :
            print("Write setting" + splitted[1] +" = "+ splitted[2])
            parameterData = db.getParameterByHiGPS(splitted[1])
            if(parameterData[0] == "W"):
                print(parameterData[0])
                
                db.write(splitted[1],splitted[2])
           
                db.store()
                return "setting,"+str(splitted[1])

        else : 
            return False
    def set_get(self,response):
        #response = response.decode("latin-1", 'ignore')
        response = response.replace('$','')
        splitted = response.split(",")
        
        print("Get Measurement" + splitted[1])
        parameterData = db.getParameterByHiGPS(splitted[1])
        if parameterData[0] == "W" or  parameterData[0] == "R":
            value = db.read(splitted[1])
                
            return "setting,"+str(splitted[1])

        else : 
            return False

    def get_samplings(self):
        #global wakeCause
        #global resetCause
        #global causeSent 
        try:
            bat= modem.getBat()
        except:
            bat= modem.getBat()
        batPercent  = str(bat[1])
        batVolt  = str(bat[2])
        
        message =  "IMEI="+str(findyIoT.imei)+"&bat="+batPercent+"&data="+self.get_data(datalist)
        return message
    def get_samplingsAlarm(self):
        
        return self.get_samplings()+"440,1;"

    def get_dataBat(self):
        global Gimei
        try:
            bat= modem.getBat()
        except:
            bat= modem.getBat()
        
        batPercent  = str(bat[1])
        batVolt  = str(bat[2])
        message = 'IMEI='+str(findyIoT.imei)+'&bat='+batPercent+'&batVolt='+batVolt

        return message


    def get_data(self,datalist):
        import ubinascii
        
        data = ""


        for par in datalist:
            if par in db.params:
                if par == '521':
                    raw = db.read(par)
                    #raw.split(b'\xff\xff')
                    print(raw.split(b'\xff\xff'))
                    value = "["
                    for val in raw.split(b'\xff\xff'):
                        try: 
                            num = struct.unpack('f',val)
                            print(num)
                            value += str(num[0])
                            value += ":"
                        except:
                            print("Except ", val)
                            if val != b'':
                                value += ":"
                    value = value[:-1] + "]"
                    
                else:
                    value = db.read(par).decode("utf-8")
                if  value:
                    value = value
                else :
                    value=""
                data += par+","+value+";"
        
        return data

    def get_setting(self,id):
        parameterData = db.getParameterByHiGPS(id)
        if parameterData[0] == "W" or parameterData[0] == "R":
            datalist = [id]
            message = "IMEI="+str(findyIoT.imei)+"&set="+self.get_data(datalist)
            print(message)
            return message

    def get_command(self,id):
        parameterData = db.getParameterByHiGPS(id)
        if parameterData[0] == "E":
            datalist = [0]
            message = "IMEI="+str(findyIoT.imei)+"&set="+id
            print(message)
            return message

    def downloadUpdate(self):
        #55
        import time
        
        import machine
        
        wdt = machine.Timer(10)
        wdt.init(period=60000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
        print("starting Download")
        downloadImage = db.read('51')
        if downloadImage != b'':
            print(downloadImage)
            downloadImage = downloadImage.decode("utf-8")
            db.write('53','1')
            db.write('54','0')
            self.main("setting,53",False)
            
            modem.connectHiGPS(2)
            fileSize = modem.sendHiGPS('/repo/'+str(downloadImage))
            modem.cipClose()
            print(fileSize)
            fileSize = fileSize


            n = 0
            a = True
            resp = ""
            if n ==0 :
                f = open( 'new.mpy', 'w' )
                f.write( "" )
                f.close()
            frames = 0
            
            while a == True :
                wdt.init(period=90000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
                #wdt = machine.Timer(10)
                #wdt.init(period=360000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
                modem.connectHiGPS(2)
                resp = modem.sendHiGPS('/repo/'+str(downloadImage)+'/512/'+str(n))
                time.sleep(2)
                part2 = modem.uart.read()
                if resp != None:
                    if part2 != None:
                        decodedResp = resp+part2
                    else:
                        decodedResp = resp
                print(decodedResp)
                modem.cipClose()
                


                totalSize = int(fileSize)
                frames = int(totalSize/512)
                if totalSize == frames*512:
                    frames = frames-1
                print("Total packets in the package = ") 
                print(totalSize)
                print("Number of frames")
                print(frames)
                print("Current frame") 
                print(n)
                
                print("checkpoint1")
                if n == frames :
                    f=open("new.mpy", "a")
                    f.write(decodedResp)  
                    f.close()
                    import os 
                    fsize=os.stat("new.mpy")
                    print("File size =") 
                    print(fsize[6])
                    if fsize[6] == totalSize:
                        wdt.init(period=90000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)
                        db.write('53','2')

                        self.main("setting,53",False)
                        time.sleep(1)
                        self.main("setting,54",False)
                        time.sleep(1)
                        print("finishing download")
                        self.main("command,55")        
                        a = False
                    else:
                        db.write('53','0') 
                        self.main("setting,53",False)
                        db.write('54','7')
                        self.main("setting,54",False)
                        return False


                print("checkpoint2")
                if decodedResp != False :
                    print("checkpoint3")
                    print(len(decodedResp))
                    if(len(decodedResp) == 512):
                        n = n+1 
                        f = open("new.mpy", "a")
                        f.write(decodedResp)  
                        f.close()

        return True
    def update(self):
        #52
        print("Updating Firmware")
        db.write('53','0')
        import os
        db.write('54','1')
        self.main("setting,53",False)
        self.main("setting,54",False)
        try: 
            import new
            os.rename('new.mpy','last.mpy')
            self.main("command,52",False)
            import machine
            time.sleep(3)
            machine.reset()
        #device.device.update()
        except: 
            os.remove('new.mpy')

        
        return True    

    def updateTime(self):
        device.updateTime()
        self.main("command,8")
    def serialNumber():
        self.main("setting,"+str(device.serialNumber()))
        return True
    def restart(self):
        
        self.main("command,221",False)
        
        machine.reset()
        return True
    def factoryReset(self):
        self.main("command,222",False)
        device.factoryReset()
        return True


class device(object):

    def restart():
        import time
        import machine
        machine.reset()
        
    
    def factoryReset():
        #import time
        #import machine
        #fwv = fw()
        #fwv.initDefaults()
        db.initDefaults()
        db.store()
        time.sleep(20)
        #ToDo
        #get clean objects file
        machine.reset()
    
    def freeMemory():
        import gc
        return round(gc.mem_free()/1024)
    
    def serialNumber():
        import ubinascii
        import machine
        return ubinascii.hexlify(machine.unique_id()).decode()

    def getBat():
        f = fw()
        f.higps.modem.isOn()
        return f.higps.modem.getBat()[1]

    
    def memoryTotal():
        import gc
        return round(gc.mem_alloc()/1024)

    def getTimestamp():
        from machine import RTC
        import utime
        clock = RTC()
        timeArray = clock.datetime()
        if timeArray[0] == 2000 :
          #  print("Wrong date")
            f = fw()
            f.higps.modem.turnOn()
            f.higps.modem.getTime()
            timeArray = clock.datetime()
        #else :
           # print("Date OK")
        t = (timeArray[0],timeArray[1],timeArray[2],timeArray[4],timeArray[5],timeArray[6],0,0)
        print(t)
        timestamp = str(utime.mktime(t)+946684800)
        return timestamp

class buffer(object):
    def set(self,bufferID):
        print("Setting buffer ID ",bufferID)
        currentBuffer = self.get(bufferID)


    def get(self,bufferID):
        print("Getting buffer ID ",bufferID)

        
class fw(object):
    def __init__(self):
    	print("Core v. 1")
    	
    	machine.freq(80000000)
    	if protocol.imei == False:
    		modem.turnOn()
    		imei = modem.getImei()
    		protocol.imei = imei
    		db.initDefaults()
    		db.store()
    	
    def start(self):
    	print("Firmware v. 1.02")
        
        
        import time
        
        
        print("Normal Start")
        if machine.wake_reason() == 2 :
            beep()
            print("Alarm Start")
            modem.turnOn()
            regRetry = 60
            while modem.isReg() == False and regRetry >0:
                regRetry = regRetry-1
                time.sleep(1)
            if modem.isReg():
                beep()
                time.sleep(0.5)
                beep()
                
                self.report(True)
                if connectionSuccess:
                    beep()
                    time.sleep(0.2)

                    beep()
                    time.sleep(0.2)
                    beep()

        else:
            self.measure()

            if db.read('525') == b'1' and (float(db.read('520')) > float(db.read('524')) or  float(db.read('520')) < float(db.read('523'))):
                modem.turnOn()
                self.report(True)
            else :
                wakeCount = float(db.read('522'))
                if  wakeCount >= float(db.read('422')):
                    modem.turnOn()
                    self.report()
                else:
                    wakeCount = int(wakeCount) + 1

                    db.write('522',wakeCount) 

             
            
            
        #self.report()
                
        try: 
            sleepTime = int(db.read('421'))
            #sleepTime = 60
            print(sleepTime)
            self.prepareSleep(sleepTime,True)

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(str(e))
            errors = str(e)
            machine.deepsleep(10000)
    def measure(self):
        adc = machine.Pin(PperipherialPower,machine.Pin.OUT)
        adc.value(1)
        time.sleep(0.1)
        pressure = round(self.adcMeasure(b'\x90')*0.03960396,2)
        
        db.write('520',str(pressure))
        
        lastArray = db.read('521')

        lastArray += struct.pack("f", pressure) + b'\xff\xff'

        db.write('521',lastArray) 
        adc.value(0)
    def adcMeasure(self,n):
        i2c = machine.SoftI2C(freq=100000,scl=machine.Pin(Pscl),sda=machine.Pin(Psda))
        i2c.start()
        #print(i2c.scan())
        i2c.writeto(104,b'\x18')
        time.sleep(0.01)
        i2c.writeto(104,n)
        time.sleep(0.01)
        sampling =int.from_bytes(i2c.readfrom(104,4)[0:2],"big")
        

        return sampling
       
    def report(self,alarm=False):
        global timestamp
        try: 
            print("Reporting")          
            if alarm:
                protocol.main('samplingsAlarm')
            else:
                protocol.main('samplings')

            print("Connection success", connectionSuccess)
            if connectionSuccess : 
                db.write('443',timestamp)
                db.write('521',b'')
                db.write('522','1')
                db.store()        
            
        except Exception as e:
            errors = str(e)
            protocol.main('dataBat')


    def prepareSleep(self,t,trig):
        print("GOING TO SLEEP FOR ")
        print(t)
        t = t+1
        #GSM pwr
        #PWR Key
        import utime
        modem.turnOff()
        machine.Pin(PmodemPWRKey, machine.Pin.IN,machine.Pin.PULL_DOWN)
        machine.Pin(PmodemPWRKey, machine.Pin.IN,machine.Pin.PULL_DOWN)
        machine.Pin(PmodemTx, machine.Pin.IN,machine.Pin.PULL_DOWN)
        machine.Pin(PmodemRx, machine.Pin.IN,machine.Pin.PULL_DOWN)
        machine.Pin(PmodemDTR, machine.Pin.IN,machine.Pin.PULL_DOWN)
        machine.Pin(Pscl, machine.Pin.IN,machine.Pin.PULL_DOWN)
        machine.Pin(Psda, machine.Pin.IN,machine.Pin.PULL_DOWN)
        machine.Pin(PperipherialPower, machine.Pin.IN,machine.Pin.PULL_DOWN)
        if trig:
                print("Triggering alarm while sleep")
                import esp32
                print("sleeping with motion trigger")
                mot = machine.Pin(Preed,machine.Pin.IN)
                if mot.value() == 1:
                    mot.irq(trigger=machine.Pin.IRQ_FALLING , wake=machine.DEEPSLEEP)
                    esp32.wake_on_ext0(pin = mot, level = esp32.WAKEUP_ALL_LOW)
                else:
                    mot.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING , wake=machine.DEEPSLEEP)
                    esp32.wake_on_ext0(pin = mot, level = esp32.WAKEUP_ANY_HIGH)
        
        
        
            
        
        
        st = self.goodNight(t*1000)


    def goodNight(self,timeS):
        

        try:
            db.store()
            print("Going to Deep Sleep")
            machine.deepsleep(timeS)
        except: 
            machine.reset()


def beep():
    pwm0 = machine.PWM(machine.Pin(27))
    pwm0.duty(500)
    pwm0.freq(5000)
    time.sleep(0.5)
    pwm0.duty(0)


db = database()
modem = sim7070()
protocol = findyIoT()