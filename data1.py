class Database(object):
    def __init__(self):

        import btree
        import uos
        #import utime
        
        
        self.newdata = False

        # key = higpsID
        # param[0] = Allowed operations - R (read), W (read-write), E (execute)
        # param[1] = Type: 1 - number, 0 - string, 2 - boolean, 9 - function
        # param[2] = Storage: 0 - file system, 1 - RAM, 2 - Function
        # param[3] = Path = 0 - default / function name
        # param[4] = Default value

        Database.params = {
            "52": ["E", 9, 2, "update()", "0", "E"],
            "53": ["R", 1, 1, 0, "0", "R"],
            "54": ["R", 1, 1, 0, "0", "R"],
            "55": ["E", 9, 2, "downloadUpdate()", "0", "E"],
            "200": ["R", 1, 0, 0, "0", "R"],
            "217": ["R", 0, 1, 0, "findy IoT", "R"],
            "218": ["R", 0, 1, 0, "q-wm-01", "R"],
            "219": ["R", 9, 2, "serialNumber()", "0", "R"],
            "220": ["R", 0, 1, 0, "2", "R"],
            "221": ["E", 9, 2, "restart()", "0", "E"],
            "222": ["E", 9, 2, "factoryReset()", "0", "E"],
            "223": ["R", 2, 0, 0, "0", "R"],
            "224": ["R", 2, 1, 0, "0", "R"],
            "225": ["R", 5, 0, 0, "0", "R"],
            "227": ["R", 0, 1, 0, "waterMeter", "R"],
            "228": ["R", 0, 1, 0, "1", "R"],
            "229": ["R", 0, 1, 0, "2", "R"],
            "312": ["E", 9, 2, "get_settings()", "0", "E"],
            "519": ["R", 2, 0, 0, "0", "R"],
            "254": ["R", 2, 0, 0, "0.00", "R"],
            "255": ["R", 2, 0, 0, "0", "R"],
            "256": ["R", 2, 0, 0, "0", "R"],
            "257": ["R", 5, 0, 0, "0", "R"],
            "258": ["R", 2, 0, 0, "0", "R"],
            "309": ["R", 2, 0, 0, "0", "R"],
            "201": ["W", 1, 0, 0, "300", "W"],
            "202": ["W", 1, 0, 0, "50", "W"],
            "564": ["W", 1, 0, 0, "0", "W"],
            "565": ["W", 1, 0, 0, "gps", "W"]
        }
        
        Database.report_type = {
            "gps": ["200", "254", "255", "256", "257", "258"],
            "batt": ["200", "223"],
            "imei" :["200"],
            "eng" : ["200"]
            }

        try:
            f = open("mydb", "r + b")
        except:
            f = open("mydb", "w + b")
            print("File")

        db = btree.open(f)
        self.data = {}

        for key in db:
            self.data[key] = db[key]

        db.flush()
        db.close()
        f.close()

    def getParameterData(self, uri):  # this is copy
        try:
            return self.params[uri]
        except:
            return False
        
    # връща лист от параметрите за ключ     
    def getParameterByHiGPS(self, higpsId):
        print("in get parameter by HiGPS")
        print(higpsId)
        try:
            return self.params[higpsId]
        except:
            return False
        
    def initDefaults(self, imei):
        import os
        import utime
        #import modem6
        if len(self.data) > 0:
            os.remove("mydb")
            print("old db removed")
            utime.sleep(5)
            machine.reset()
        else:
            print("no previous db")
            
        n = 0
        #imei = '2111111111111'
        
        while n < 3 and len(imei) != 15: # 'n'  е ако не вземе ИМЕИ от първият път
            #imei = modem.getImei()
            n += 1
            
        self.newdata = True
        for higpsID in self.params:
            if self.params[higpsID][4] != None and self.params[higpsID][2] == 0:
                if higpsID == '200':
                    self.write(higpsID, imei)
                else:
                    self.write(higpsID, self.params[higpsID][4])
                    
    def write_value(self, pos, value):
        self.write(pos, value)
        
                        

    def read(self, property, echo=True):  # copy
        import btree
        try:
            if type(property) == str:
                property = str.encode(property)
            if echo:
                print("Reading " + str(property) + " = " + str(self.data[property]))
                return self.data[property]
        except:
            return False

    def write(self, property, value):  # copy
        self.newdata = True
        try:
            if type(value) == int:
                value = str(value)
            if type(value) == str:
                value = str.encode(value)
            if type(property) == str:
                property = str.encode(property)
            print("Writing " + str(property) + " = " + str(value))
            
            
            self.data[property] = value

            return True
        except:
            return False

    def store(self):  # copy   Dava Exception
        if self.newdata == False:
            print("No data to write")
            return True

        try:
            import btree
            print("Database store started")
            try:
                f = open("mydb", "r + b")
            except OSError:
                f = open("mydb", "w + b")
            db = btree.open(f)
            for key in self.data:
                print("key " + str(key))
                print("params " + str(key.decode('utf-8')))
                print("params2 " + str(self.params[key.decode('utf-8')][2]))
                if self.params[key.decode('utf-8')][2] == 0:
                    print("key params == 0 ")
                    db[key] = self.data[key]

            db.flush()
            db.close()
            f.close()
            print("Database store completed")
            self.newdata = False
            return True


        except Exception as e:
            print("Failed writing in database ", e)
            self.newdata = False
            return False
        
    def get_report(self):
        inst = Database() # инстанцията за доклада да се изкара в main метода,
                          #за да може да взема инфо(показатели) не само от data, а и от паметта, от датчици и др
        type_report = inst.read("565").decode("utf-8")
        result = []
        print(type_report)
        if type_report == "gps":
            for el in self.report_type["gps"]:
                r = inst.read(el).decode("utf-8")
                result.append(r)
                
        elif type_report == "batt":
            for el in self.report_type["batt"]:
                r = inst.read(el).decode("utf-8")
                result.append(r)
        elif type_report == "imei":
            for el in self.report_type["imei"]:
                r = inst.read(el).decode("utf-8")
                result.append(r)
        else:
            return "Bad command"
        
        return result
        
    


#d = Database()

'''

for key in d.data:
    print(key)
    d.read(key)
    
'''



