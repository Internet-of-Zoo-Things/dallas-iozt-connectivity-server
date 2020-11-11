from flask import Flask
import serial
import time

app = Flask(__name__)

@app.route('/feed/<float:food_wt_lbs>')
def send_feed(food_wt_lbs):
    #time_run = time.time() + food_wt_lbs*5.0 + 2 #Use Calibration Equation Here or on Arduino
    time_run = food_wt_lbs
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=5, parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
    time.sleep(1)

    ser.write(str.encode("AT+ADDRESS=25\r\n"))
    serial_payload = (ser.readline())[:-2]
    print("Address set?", serial_payload.decode(encoding="utf-8"))
    time.sleep(1)
    ser.write(str.encode("AT+NETWORKID=6\r\n"))
#     ser.write(str.encode("AT+BAND=915000000"))
#     ser.write(str.encode("AT+ADDRESS="))
    time.sleep(1)
    ser.write(str.encode("AT?\r\n"))
    serial_payload = (ser.readline())[:-2]
    print("Module responding?", serial_payload.decode(encoding="utf-8"))
    time_loop = time.time() + 5.0 #transmission time
    while(1):# time.time() <= time_loop:
        msg = "AT+SEND=116, " + str(len(str(time_run)))+", " +str(time_run)+ "\n"
        ser.write(str.encode("AT+SEND=0, 4, hiii\r\n"))
        print(msg)
        
        # line = ser.readline().decode('utf-8')
        #print(line)
    return('Feed'+str(food_wt_lbs))

