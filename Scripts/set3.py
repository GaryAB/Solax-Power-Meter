def set(inverterAddress,inverterPassword,register,value):

  import requests
  import re
  import time
  
  count = 0
  fcount = 0
  global chgReg
  global dchReg
  chgReg = 31 #Register to set charge limit
  dchReg = 39 #Register to set discharge start time

  sval = str(value)
  success = 0
  try:
      data = 'optType=ReadSetData&pwd='+inverterPassword
      x = requests.post(inverterAddress, data=data)
      x = (x.text)
      array = re.split(",",x)
      enabled = array[29]
      if int(enabled) == 0:
        return "Charge from grid disabled"
      setting = array[register-1]
      if (int(setting) == int(value)) and (register == chgReg):
        return int(setting)
      while (success == 0) and (fcount < 3):
        while (success == 0) and (count < 20):
          # connect to inverter
          data = 'optType=setReg&pwd='+inverterPassword+'&data={"num":1,"Data":[{"reg":'+str(register)+',"val":"'+sval+'"}]}'
          x = requests.post(inverterAddress, data=data)
          x = (x.text)
          if x[0:1] == "Y":
            success = 1
          count = count + 1
          time.sleep(5)
        # check setting
        if success == 1:
          data = 'optType=ReadSetData&pwd='+inverterPassword
          x = requests.post(inverterAddress, data=data)
          x = (x.text)
          y = x[1:]
          array = re.split(",",y)
          setting = array[register-1]
          if int(setting) == int(value):
            success = 1
          else:
            success = 0
        fcount = fcount + 1
        count = 0
      if success == 1:
        return int(setting) 
      else:
        return "Unable to set preload to "+sval+"%"
  except:
      
      return "Unable to set preload to "+aval+"%"
    
