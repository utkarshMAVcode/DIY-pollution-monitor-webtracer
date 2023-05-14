import base64
import json
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__, static_folder='Static')
app.secret_key = 'RcGi3pdL'
degree_sign = u'\N{DEGREE SIGN}'

readings_df = pd.read_csv("D:\Code\_Code\Python Code\EPICS\Analysis\Sensor_Readings.csv")

@app.route('/images/<path:filename>')
def serve_image(filename):
    images_directory = 'D:\Code\_Code\Python Code\EPICS\Analysis'
    
    return send_from_directory(images_directory, filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_string = request.form['input_string']

        try:
            decoded_data = int.from_bytes(base64.b64decode(input_string), 'big')
            retrieved_number = int(bin(decoded_data)[2:].zfill(48), 2)

            temperature = (str(retrieved_number)[0:2] + '.' + str(retrieved_number)[2] + f'{degree_sign}C')
            humidity = (str(retrieved_number)[3:5] + '.' + str(retrieved_number)[5] + "%")
            gas1 = (str(retrieved_number)[6:8] + str(retrieved_number)[8] + " ppm")
            gas2 = (str(retrieved_number)[9:11] + str(retrieved_number)[11] + " ppm")

            session['temperature'] = temperature
            session['humidity'] = humidity
            session['gas1'] = gas1
            session['gas2'] = gas2

            return redirect(url_for('index'))
        except (UnicodeDecodeError, ValueError, IndexError):
            error_message = "Invalid input string. Please enter a valid Base64 encoded string."
            return render_template('index.html', error_message=error_message)

    temperature = session.get('temperature')
    humidity = session.get('humidity')
    gas1 = session.get('gas1')
    gas2 = session.get('gas2')

    return render_template('index.html', temperature=temperature, humidity=humidity, gas1=gas1, gas2=gas2)

@app.route('/analysis')
def analysis():
    temperature = session.get('temperature')
    humidity = session.get('humidity')
    gas1 = session.get('gas1')
    gas2 = session.get('gas2')

    return render_template('analysis.html', temperature=temperature, humidity=humidity, gas1=gas1, gas2=gas2)

@app.route('/save-readings', methods=['POST'])
def save_readings():

    global readings_df

    temperature = session.get('temperature') or request.form.get('temperature')
    humidity = session.get('humidity') or request.form.get('humidity')
    gas1 = session.get('gas1') or request.form.get('gas1')
    gas2 = session.get('gas2') or request.form.get('gas2')
    date = datetime.now()
    current_date = date.strftime("%d/%m %H:%M")

    new_reading = [temperature, humidity, gas1, gas2, current_date]

    readings_df.loc[len(readings_df)] = new_reading
    readings_df.to_csv("D:\Code\_Code\Python Code\EPICS\Analysis\Sensor_Readings.csv", index=False)

    temp_list = list(map(lambda x:float(x[0:-2]), readings_df['Temperature']))
    hum_list = list(map(lambda x:float(x[0:-1]), readings_df['Humidity']))
    gas1_list = list(map(lambda x:float(x[0:-4]), readings_df['Gas1']))
    gas2_list = list(map(lambda x:float(x[0:-4]), readings_df['Gas2']))
    date_list = list(map(lambda x:str(x), readings_df['Date']))

    plt.plot(date_list, temp_list)
    plt.ylim(10, 50)
    plt.xlabel("Date")  
    plt.ylabel(f"Temperature({degree_sign}C)")  
    plt.title("Temperature Readings")  
    plt.savefig("D:\Code\_Code\Python Code\EPICS\Analysis\\temperature_plot")
    plt.clf()

    plt.plot(date_list, hum_list)
    plt.ylim(20, 50)
    plt.xlabel("Date") 
    plt.ylabel("Humidity(%)") 
    plt.title("Humidity Readings") 
    plt.savefig("D:\Code\_Code\Python Code\EPICS\Analysis\\humidity_plot")
    plt.clf()

    plt.plot(date_list, gas1_list)
    plt.ylim(0, 999)
    plt.xlabel("Date")
    plt.ylabel("Propane (ppm)") 
    plt.title("Propane Readings")
    plt.axhline(y = 300, color = 'r', linestyle = '-')
    plt.savefig("D:\Code\_Code\Python Code\EPICS\Analysis\\gas1_plot")
    plt.clf()

    plt.plot(date_list, gas2_list)
    plt.ylim(0, 999)
    plt.xlabel("Date") 
    plt.ylabel("Carbon Monoxide (ppm)")
    plt.title("CO Readings")
    plt.axhline(y = 350, color = 'r', linestyle = '-') 
    plt.savefig("D:\Code\_Code\Python Code\EPICS\Analysis\\gas2_plot")
    plt.clf()

    response = {'message': 'Readings saved successfully'}

    session.pop('temperature', None)
    session.pop('humidity', None)
    session.pop('gas1', None)
    session.pop('gas2', None)

    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
