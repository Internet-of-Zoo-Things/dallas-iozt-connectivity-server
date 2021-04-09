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

        ser.write(str.encode("AT?\r\n"))
        serial_payload = (ser.readline())[:-2]
        print("Module responding?", serial_payload.decode(encoding="utf-8"))
        time_loop = time.time() + 5.0 #transmission time or ACK needed
        while time.time() <= time_loop:
            #Or replace with AT+SEND=feeder_id
            msg = "AT+SEND=20, " + str(len(str(run_time)))+", " +str(run_time)+ "\n"
            ser.write(str.encode(msg))
    except serial.serialutil.SerialException:
        abort(500)

    #Replace with Format strings
    return('Success! Fed for '+str(run_time)+" seconds on feeder "+str(feeder_id)+".")