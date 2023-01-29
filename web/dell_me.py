ent = b'GET /?led=off HTTP/1.1\r\nHost: 192.168.1.105\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Linux; Android 11; 2201117PG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nReferer: http://192.168.1.105/?led=on\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: bg-BG,bg;q=0.9,en;q=0.8\r\n\r\n'

#req = 'GET /?led=on HTTP/1.1\r\nHost: 192.168.1.105\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nReferer: http://192.168.1.105/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: bg-BG,bg;q=0.9,en;q=0.8\r\n\r\n'

r = 'GET /?led=on HTTP/1.1\r\nHost: 192.168.1.105\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nReferer: http://192.168.1.105/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: bg-BG,bg;q=0.9,en;q=0.8\r\n\r\n'
req = 'GET /?pin=ON1 HTTP/1.1\r\nHost: 192.168.1.105\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Linux; Android 11; 2201117PG Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.85 Mobile Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nX-Requested-With: appinventor.ai_rffsantos16.ESP8266_Controller\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-GB,en-US;q=0.9,en;q=0.8\r\n\r\n'

#request = ent.recv(1024)
#request = str(request)
#print("reg -> ",req.find('/?led=on' or '/?pin=ON1'))
print("pin -> ", req.find('/?pin=ON1'))

#led_on = req.find('/?led=on') or pin.find('/?pin=ON1')
#print(led_on)
if '/?led=on' or '/?pin=ON1' in req:
    print("LED ON")
    led_on = "1"
if '/?led=off' or '/?pin=OFF1' in req:
    print("LED OFF")
    led_on = "0"
    