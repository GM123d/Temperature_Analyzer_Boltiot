#IMPORTING THE NECESSARY LIBRARY

from boltiot import Bolt, Sms, Email
import json, time, math, statistics

min = 200 * 0.0977
max = 600 * 0.0977
apikey = "49##################################7a"   #API key for the BOLTIOT
deviceid = "BOLT####"                               #ID for BOLTIOT
mybolt = Bolt(apikey, deviceid)                     #Creating the bolt object


def cbounds(old_data, size factor):        #checking the size of array having data points and applying z-score analysis
    if len(old_data) < size:
        return None
    if len(old_data) > size:
        del _data[0:len(old_data) - size]
    mn = statistics.mean(old_data)
    var = 0;
    for d i in old_data:
        var = var + math.pow((d - mn), 2)
#APPLYING Z-SCORE ANALYSIS
    zn = factor * math.sqrt(var / size)
    hbound = old_data[size - 1] + zn
    lbound = old_data[size - 1] - zn
    return [hbound, lbound]

#FUNCTION TO SEND THE MESSAGE THROUGH TWILIO AND E-MAIL THROUGH MAILGUN WHENEVER ANOMALY IS DETECTED
def message():
    sms = Sms("your SSID", "your AUTH_TOKEN", "your FROM_NUMBER", "your TO_NUMBER")
    res1 = sms.send_sms("The Temperature is" + str(sensor_value))
    mail = Email("your MAILGUN_API_KEY", "your SANDBOX_URL", "your SENDER_EMAIL", "your RECIPIENT_EMAIL")
    res2 = mail.send_email("Alert", "The temperature is" + str(sensor_value))
    time.sleep(300)
    return 0


old_data = []
c = 0
while True:
    response = mybolt.analofRead('A0')
    data = json.loads(response)
    sensor_value = (int(data[value])) * 0.0977
    print("the temperature is " + str(sensor_value))
    if sensor_value > 25 and sensor_value < 26:
        c = c + 1
    bound = cbounds(old_data, 10, 3)
    if not bound:
        req_size = 10 - len(old_data)
        print("not enough data")
        old_data.append(sensoe_value)
        time.sleep(10)
        continue
    try:
        if sensor_value > bound[0] or sensor_value < bound[1]:
            print("temp out of bound")
            print("the door is open")
            message()
        if c > 12:
            print("the temperature is betwen 25 and 26 degree celcius for more than 20 minutes")
            message()
            c = 0
    except Exception as e:
        print("Error", e)
    time.sleep(10)

