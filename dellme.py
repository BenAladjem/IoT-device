import ubinascii
import utime
import json

# Converting GPS report to base64

#t = "20221114101637"
#t = (t[0:4], t[4:6], t[6:8], t[8:10], t[10:12], t[12:14])
#print(t)

#res = {'255': '23.289744', '258': '', '256': '621.057', '257': '20221114101637', '254': '42.675474'}

res = [' 1', '1', '20221114101637.000', '42.675474', '23.289744', '621.057', '', '', '1', '', '500.0', '500.0', '500.0', '', '3', '', '5683.3', '189.4\r\n\r\nOK\r\n']
#gps_dict = {}
#gps_dict["254"] = res[3]
#gps_dict["255"] = res[4]
#gps_dict["256"] = res[5]
#gps_dict["257"] = res[2].split(".")[0]
#gps_dict["258"] = res[6]


            
t = res[2].split(".")[0]
t = (int(t[0:4]), int(t[4:6]), int(t[6:8]), int(t[8:10]), int(t[10:12]), int(t[12:14]), 0, 0)

timestamp = str(utime.mktime(t) + 946684800)

loc_data = {}
loc_data[timestamp] = [float(res[3]), float(res[4]), float(res[5])]
print(loc_data)

locJSON = json.dumps(loc_data)
loc64 = ubinascii.b2a_base64(locJSON)
loc64 = loc64.decode("utf-8")
loc64 = loc64.replace("\n", "")
print(loc64)
                