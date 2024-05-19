#!/usr/bin/env python

import rospy
from diagnostic_msgs.msg import DiagnosticArray
from flask import Flask, render_template, jsonify
from multiprocessing import Process, Manager
import math

app = Flask(__name__)

# Function to convert radians to degrees
def radians_to_degrees(value):
    return value * (180.0 / math.pi)

# Function to store diagnostics data in a shared list
def diagnostics_callback(msg, diagnostics_data):
    diagnostics_data[:] = []  # Clear the list
    for status in msg.status:
        values = {}
        for value in status.values:
            key = value.key
            val = value.value
            # Convert specific fields from radians to degrees
             
            if key in ["Position", "Goal"]:
                try:
                    val = radians_to_degrees(float(val))
                except ValueError:
                    pass  # In case the value is not a valid float
            values[key] = val
        entry = {
            "name": status.name,
            "message": status.message,
            "hardware_id": status.hardware_id,
            "values": {value.key: value.value for value in status.values}
        }
        diagnostics_data.append(entry)

@app.route('/')
def index():
    return render_template('indexcold.html')

@app.route('/data')
def data():
    diagnostics_data = app.config['diagnostics_data']
    # Ensure all data is JSON serializable
    extracted_values = []
    for entry in diagnostics_data:
        extracted_values.append({
            "name": entry["name"],
            "message": entry["message"],
            "hardware_id": entry["hardware_id"],
            "values": {str(k): str(v) for k, v in entry["values"].items()}
        })
    sorted_keys = sorted({key for entry in diagnostics_data for key in entry["values"].keys()})
    return jsonify(extracted_values=extracted_values, sorted_keys=sorted_keys)

def run_flask_app(diagnostics_data):
    global app
    app.config['diagnostics_data'] = diagnostics_data
    app.run(host='0.0.0.0', port=5000, debug=True)

def ros_main(diagnostics_data):
    rospy.init_node('diagnostics_listener', anonymous=True)
    rospy.Subscriber('/diagnostics', DiagnosticArray, diagnostics_callback, diagnostics_data)
    rospy.spin()

if __name__ == '__main__':
    manager = Manager()
    diagnostics_data = manager.list()
    
    # Start Flask app in a separate process
    flask_process = Process(target=run_flask_app, args=(diagnostics_data,))
    flask_process.start()
    
    # Run ROS node in the main process
    ros_main(diagnostics_data)
    
    # Ensure Flask process is terminated when ROS node stops
    flask_process.join()
