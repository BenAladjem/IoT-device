import json
import ubinascii
import time
'''
2021-12-30 10:43:49 Input Type: gpsArray Text: IMEI=865456054799968&bat=77&GPSArray=eyIxNjQwODUzODE4IjogWzQyLjY3NDgxLCAyMy4yODk3OCwgMC4wXX0=&er=12.03_&

locations[loc["Timestamp"]] = [loc["Lat"],loc["Lon”],loc[“Speed"]]
locJSON  = json.dumps(locations)
lo = ubinascii.b2a_base64(locJSON)
locationString = lo.decode("utf-8")
locationString = locationString.replace("\n","")
message = "IMEI="+str(higps.imei)+'&bat='+batPercent+'&GPSArray='+locationString

'''

# timestamp = modem.sendHiGPS('/t/')
{"1640853818": [42.67481, 23.28978, 0.0]}

loc = {"1668175234": [42.67481, 23.28978, 0.0]}
#print(loc)
locJSON = json.dumps(loc)
print(locJSON)
loc64 = ubinascii.b2a_base64(locJSON)
loc64 = loc64.decode("utf-8")
loc64 = loc64.replace("\n", "")
print(loc64)

#eyIyMDIyMTExMTEzMTE0OSI6IFs0Mi42NzQ4MSwgMjMuMjg5NzgsIDAuMF19

print(time.time())

