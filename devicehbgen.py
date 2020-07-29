import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests

#provide your ibm watson device credentials
organization= "Organization_id"
deviceType= "Device_type"
deviceId="ID"
authMethod= "Aunthentication_method"
authToken= "Authentication_token"

#initialize GPIO
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='poweron':
                print("device is on")
        elif i=='poweroff':
                print("device is off")

def myCommandCallback(cmd):
        print("Command received: %s" %cmd.data)
        print(type(cmd.data))

try:
    deviceOptions={"org":organization, "type":deviceType, "id": deviceId,
                   "auth-method":authMethod, "auth-token":authToken}
    deviceCli=ibmiotf.device.Client(deviceOptions)
    
except Exception as e:
    print("Caught exception connecting device: %s"  %str(e))
    sys.exit()

deviceCli.connect()

while True:
    temp=random.randint(97, 101)
    rate=random.randint(60,101)
    pressure= 120/80
    #send temperature and heart rate to IBM Watson

    data={'Temperature': temp, 'Heart_Rate':rate, 'Blood_Pressure':pressure}

    def myOnPublishCallback():     #a function
            print ("Published Temperature = %s F" % temp, "Heart Rate = %s bpm" % rate, "Blood Pressure = %s mmHg" % pressure, "to IBM Watson")

    success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)

    if (temp>100):
        x=requests.get("https://www.fast2sms.com/dev/bulk?authorization=&sender_id=FSTSMS&message=Alert!%20Your%20temperature%20has%20exceeded%20above%20the%20average%20level.%20Kindly%20take%20medication!&language=english&route=p&numbers=xxxxxxxxxx")
        print(x.text)

    if (rate>100 | rate==60):
        y=requests.get("https://www.fast2sms.com/dev/bulk?authorization=&sender_id=FSTSMS&message=Alert!%20Your%20Pulse%20rate%20is%20changing%20rapidly.%20Kindly%20stay%20calm!&language=english&route=p&numbers=xxxxxxxxxx")
        print(y.text)


    if not success:
        print("Not connected to IoTF")
    time.sleep(2)
        
    deviceCli.commandCallback = myCommandCallback

#disconnect the device and application from the cloud
deviceCli.disconnect()
