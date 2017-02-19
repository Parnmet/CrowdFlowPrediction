#!/usr/bin/python
#-*-coding: utf-8 -*-
from flask import Flask,jsonify,request
import PredictionService

app = Flask(__name__)

@app.route('/')
def index():
    return "Crowd Flow Prediction"

@app.route('/crowdflow/density',methods=['GET'])
def getDensity():
    den = {}
    if 'time' in request.args and 'll' in request.args:
        if request.args.get('time') == "NOW":
            den = PredictionService.getCurrentDensity(request.args.get('ll'))
        elif request.args.get('time') == "5MIN":
            den = PredictionService.getNextDensity(request.args.get('ll'))
    else:
        den['Error'] = "NO 'time' and 'll' parameter"
    return jsonify(den)

@app.route('/crowdflow/getAllPlace',methods=['GET'])
def getAllPlace():
    return jsonify(PredictionService.allPlace())

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)
    app.run(debug=True)