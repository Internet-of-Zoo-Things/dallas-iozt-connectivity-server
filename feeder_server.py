from flask import Flask
from flask import request
from flask import abort

import serial
import time

app = Flask(__name__)

@app.route('/feed/<int:feeder_id>', methods=['POST'])
def send_feed(feeder_id):
    #run_time = time.time() + food_wt_lbs*5.0 + 2 #Use Calibration Equation Here or on Arduino

    run_time = request.json['runtime']

    #Replace with Format strings
    print("Starting feed for "+str(run_time)+" seconds on feeder "+str(feeder_id)+".")

    try:
        ser = serial.Serial('/dev/ttyS0', 115200, timeout=5, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        time.sleep(1)
        ser.write(str.encode("AT+ADDRESS=10\r\n"))
        time.sleep(1)
        ser.write(str.encode("AT+NETWORKID=5\r\n"))
        time.sleep(1)
        ser.write(str.encode("AT+MODE=1\r\n"))
        time.sleep(1)
        ser.write(str.encode("AT+BAND=915000000\r\n"))
        time.sleep(1)
        ser.write(str.encode("AT+PARAMETER=10,7,1,7\r\n"))
        time.sleep(5)

        msg = "AT+SEND=20, " + str(len(str(run_time)))+", " +str(run_time)+ "\n"
        count = 15
        time_loop = time.time() + 15.0 #transmission time or ACK needed
        while time.time() <= time_loop:
            ser.write(str.encode(msg))
            time.sleep(1)
            line = ser.readline()
            if len(line) == 28:
               print("Communication Received: " + line.decode('utf-8'))
               print("Ending Feed - Starting 30 sec  buffer")
               time.sleep(30)
               break
            line=''
    except serial.serialutil.SerialException:
        abort(500)

    #Replace with Format strings
    return('Success! Fed for '+str(run_time)+" seconds on feeder "+str(feeder_id)+".")
