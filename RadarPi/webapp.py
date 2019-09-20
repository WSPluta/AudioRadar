#!/usr/bin/python3

import waveGenerator
import recordAudio
import cwProcessing
from playSound import playSound
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
@app.route("/radarpi.html")
def home():
    return render_template('radarpi.html')

@app.route("/cwNT.html")
def cwNT():
    return render_template('cwNT.html')

@app.route("/cwT.html")
def cwT():
    return render_template('cwT.html')

@app.route("/pulsedopplerNT.html")
def pulsedopplerNT():
    return render_template('pulsedopplerNT.html')

@app.route('/pulsedopplerT.html')
def pulsedopplerT():
    return render_template('pulsedopplerT.html')
    
@app.route('/results.html',methods = ['POST', 'GET'])
def results():
   if request.method == 'POST':
      results = request.form       
      mode = request.form['mode']
      
      if mode == 'Continuous Non-Technical':
          
          duration = float(request.form["duration"])
          
          waveGenerator.waveGenerator(duration)
          name = '8000Hz.wave' 
          playSound(name)
          Rx_Signal = recordAudio.recordAudio(duration*1.2)

          cwProcessing.cwProcessing(Rx_Signal)
          
          return render_template("results.html",results = results)
      
      elif mode == 'Continuous Technical':
          
          frequency = float(request.form["frequency"])
          duration = float(request.form["duration"])
          
          waveGenerator.waveGenerator(duration, frequency)
          name = str(int(frequency)) + 'Hz.wave'
          playSound(name)
          
          return render_template("results.html",results = results)
      
      elif mode == 'Pulse Doppler Non-Technical':
          
          rangeU = float(request.form["rangeU"])
          
          Tx_Signal, Tx_p = waveGenerator.pulseTrainGenerator(rangeU)
          
          name = 'Chirp 8000Hz.wave'

          playSound(name)
          
          return render_template("results.html",results = results)
      
      elif mode == 'Pulse Doppler Technical':
          
          rangeU = request.form["rangeU"]
          resolution = request.form["resolution"]
          frequency = request.form["frequency"]
          bandwidth = request.form["bandwidth"]
          pulses = request.form["pulses"]
          
          Tx_Signal, Tx_p = waveGenerator.pulseTrainGenerator(rangeU,resolution,frequency,bandwidth,pulses)
          
          name = 'Chirp ' + str(int(frequency)) + 'Hz.wave'
          
          playSound(name)
          
          return render_template("results.html",results = results)
          
      else:
          
          return render_template("none.html")
          
      
          
      



if __name__ == "__main__":
    app.run(host='RadarPi.local', port=8080, debug=True)#host='0.0.0.0'
