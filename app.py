from flask import Flask, Response, render_template, request, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
import serial.tools.list_ports
import time
from flask import Flask, Response, render_template, request, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lh = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wellplate_syringe')
def wellplate_syringe():
    return render_template('wellplate_syringe.html')


@app.route('/control_panel')
def control_panel():

    ports = serial.tools.list_ports.comports()

    print([port.name for port in ports])

    ports_serialized = [{'name': port.name, 'description': port.description} for port in ports]
    print(ports_serialized)

    try:
        selected_port = lh.port.replace('/dev/', '')
    except:
        selected_port = ''

    print(selected_port)

    context = {
        'ports': ports_serialized,
        'selected_port': selected_port,
    }
    
    return render_template('control_panel.html', context=context)


def send_gcode(command):
    print(command)

    lh.write(str.encode(command)) 
    time.sleep(0.5)

    while True:
        line = lh.readline()
        print(line)

        if line == b'ok\n':
            return jsonify({'success': 'ok'})
        
        else:
            print('timeout')
            return jsonify({'error': 'timeout reached'})



@app.route('/select_port', methods=['POST'])
def select_port():
    global lh

    port = request.args.get('port')

    print(port)

    lh_port = [p.device for p in serial.tools.list_ports.comports() if p.name == port][0]

    lh = serial.Serial(lh_port, 115200, timeout=0.5)
    time.sleep(1)
    send_gcode('$$\r\n')

    #Step idle delay (ms)
    send_gcode('$1=10\r\n')
    #Steps per mm
    send_gcode('$100=4.9736\r\n')
    send_gcode('$101=79.578\r\n')
    send_gcode('$102=100\r\n')
    send_gcode('$103=40\r\n')
    #Max rate (mm/min)
    send_gcode('$110=2000\r\n')
    send_gcode('$111=2000\r\n')
    send_gcode('$112=200\r\n')
    send_gcode('$113=1000\r\n')
    #Acceleration (mm/s^2)
    send_gcode('$120=100\r\n')
    send_gcode('$121=100\r\n')
    send_gcode('$122=10\r\n')
    send_gcode('$123=200\r\n')
    send_gcode('G21\r\n')

    return jsonify({'success': 'ok'})


@app.route('/move', methods=['POST'])
def move():
    axis = request.args.get('axis')
    direction = request.args.get('direction')
    distance = request.args.get('distance')

    command = f"G91\r\nG0 {axis}{direction}{distance}\r\nG90\r\n"

    return send_gcode(command)


@app.route('/set_home', methods=['POST'])
def set_home():

    command = f"G92 X0 Y0 Z0 A0\r\n"

    return send_gcode(command)


def syringe_wellplate_run(syringe_volume, well_data_list):
    if syringe_volume == 1:
        syringe_mm_per_µl = 0.01393
    elif syringe_volume == 3:
        syringe_mm_per_μl = 0.00424
    for i, row in enumerate(well_data_list):
        y = - i * 9
        for j, well in enumerate(row):
            if well['volume'] != '':
                x = j * 9
                volume = float(well['volume'])
                flowrate = float(well['flowrate'])
                stepper_rate = syringe_mm_per_μl * 1000 * flowrate
                stepper_distance = volume * syringe_mm_per_μl
                send_gcode(f'$113={stepper_rate}\r\n')
                send_gcode(f"G0 X{x} Y{y} Z10\r\n")
                send_gcode(f"G0 X{x} Y{y} Z0\r\n")
                send_gcode(f"G0 X{x} Y{y} Z0 A-{stepper_distance}\r\n")
                send_gcode(f"G0 X{x} Y{y} Z10\r\n")


@app.route('/syringe_wellplate_start_run', methods=['POST'])
def syringe_wellplate_start_run():
    json_payload = request.json

    syringe_volume = float(json_payload['syringe_volume'])
    well_data_list = json_payload['well_data_list']
    syringe_wellplate_run(syringe_volume, well_data_list)


    return jsonify({'success': 'ok'})

