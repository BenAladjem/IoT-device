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



log = []
spase = "                |"
log_empty_row  = "".join([spase]*4)
em_row = [spase]*4
log_1_row = "".join(["Main            |", "Command         |", "Modem           |", "DataBase        |"])
log.append(log_1_row)
log.append(log_empty_row)

empty_question = "/input.php?IMEI=865456054799968"

#def recogn_name(command):  in Commands
d = {
         "#User=":"User",
             "#+":"Phones",
         "*MODE-":"Mode",
        "*MODE?$":"ModeQ",
         "*GPRS$": "Gprs",
          "*GSM$": "Eng",
         "*ENG$" : "Eng",
         "*GET," : "Get",
         "*SET," : "Set"
        }



default_report_type  = {
        "No report":"0",
        "GPS possition by SMS":"1",
        "Battery by GPRS":"2",
        "GPS and Battery by GPRS":"3",
        "Bluetooth by GPRS":"4",
        "GPS possition by SMS and GPRS":"5",
        "GSM information by GPRS":"6",
        "Battery by WiFi":"7"
        }

commands_dict = {
        "200":"imei",
        "217":"",
        "218":"",
        "219":"",
        "220":"firmware_version",
        "221":"",
        "222":"",
        "223":".get_dataBat",
        "224":"",
        "225":"current_time",
        "227":"",
        "228":"",
        "229":"",
        "312":"get_settings",
        "565":"report_type"
        
        }


parameters = ["GNSS run status = ", "Fix status = ", "UTC date & Time = ",
              "Latitude = ", "Longitude = ", "MSL Altitude = ", "Speed Over Ground = ",
              "Course Over Ground = ", "Fix Mode = ", "Reserved1 = ", "HDOP = ",
                "PDOP = ", "VDOP = ", "Reserved2 = ", "G NSS Satellites in View = ",
              "Reserved3 = ", "HPA = ", "VPA = "
              ]



#Database

params = {
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
        
report_type = {
            "gps": ["200", "254", "255", "256", "257", "258"],
            "batt": ["200", "223"],
            "imei" :["200"],
            "eng" : ["200"]
            }