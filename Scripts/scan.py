import socket
import requests
from requests import get

#main Start
def ipScan(From, To, inverterPassword):
    ip_range = ipRange(From, To)
    for ip in ip_range:
        bip = isOpen(ip,80,inverterPassword)
        #print(ip)
        if bip != None:
            return bip
            break

#Check If Port Is Open
def isOpen(ip, port, inverterPassword):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        fip = 'http://' + ip
        #print(ip)
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            data = {
             'optType': 'ReadRealTimeData',
             'pwd': inverterPassword,
            }
            x = requests.post(fip, data=data, timeout=5)
            x = (x.text)
            if x[7:17] == inverterPassword:
                #print ('Found')
                return ip
                      
        except Exception as e:
                #print(e)
                pass 
        #finally:
                #s.close()

##Range Ip Function ipRange
def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   #print (start)
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []

   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))

   return ip_range
   pass

