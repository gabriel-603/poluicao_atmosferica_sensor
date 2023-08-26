##Substituir rede e senha do WIFI e URL do servidor


from machine import Pin, ADC
import time
import network
import urequests as requests
import json

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect('REDE', 'SENHA')

while not sta_if.isconnected():
    time.sleep(1)

mq135analog = ADC(Pin(32))
mq135analog.atten(ADC.ATTN_0DB)
mq135analog.width(ADC.WIDTH_11BIT)

mq9analog = ADC(Pin(34))
mq9analog.atten(ADC.ATTN_0DB)
mq9analog.width(ADC.WIDTH_11BIT)

url = "URL_SERVIDOR"

while True:
    sensorValue135 = mq135analog.read()
    digitalValue135 = Pin(2, Pin.IN).value()
    
    sensorValue9 = mq9analog.read()
    digitalValue9 = Pin(16, Pin.IN).value()

    data = {
        "analog_135": sensorValue135,
        "digital_135": digitalValue135,
        "analog_9": sensorValue9,
        "digital_9": digitalValue9
    }

    try:
        response = requests.post(url, json=data)
        print("Response status code:", response.status_code)
        response.close()  # Close the response to release resources
    except Exception as e:
        print("Exception:", e)

    time.sleep(30)  # Wait for the next reading
