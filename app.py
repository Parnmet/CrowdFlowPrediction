#!/usr/bin/python
#-*-coding: utf-8 -*-
from flask import Flask,jsonify,request
import PredictionService
import FlowPrediction
from random import randint

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
            den = PredictionService.getNextDensity(request.args.get('ll'),5)
        elif request.args.get('time') == "10MIN":
            den = PredictionService.getNextDensity(request.args.get('ll'),10)
        elif request.args.get('time') == "15MIN":
            den = PredictionService.getNextDensity(request.args.get('ll'),15)
        else:
            den['Error'] = "'time' or 'll' mismatch"
    else:
        den['Error'] = "NO 'time' and 'll' parameter"
    return jsonify(den)

@app.route('/crowdflow/getAllPlace',methods=['GET'])
def getAllPlace():
    return jsonify(PredictionService.allPlace())

@app.route('/crowdflow/random',methods=['GET'])
def getRand():
    den = ["LOW","HIGH","MEDIUM"]
    num = randint(0,2)    
    density = {}
    density['density'] = []
    d = {}
    d['density'] = den[num]
    density['density'].append(d)
    # print(density)
    return jsonify(density)

@app.route('/crowdflow/flow',methods=['GET'])
def getFlow():
    den = {}
    if 'time' in request.args:
        if request.args.get('time') == "5MIN":
            den = FlowPrediction.getFlowPrediction(request.args.get('ll'))
            # print(den['crowdFlow'])
            # cen = [elem for elem in den['crowdFlow'] if elem['place']['lat'] == 13.745844972517325 and elem['place']['lng'] == 100.53954639826303]
            # print(cen)
            # if len(cen)>0:
            #     paragon ={} 
            #     paragon['lat'] = 13.74601377826572
            #     paragon['lng'] = 100.53440439922444
            #     paragon['name'] = "Siam Paragon (สยามพารากอน)"
            #     cen[0]['nextPlace']= []
            #     cen[0]['nextPlace'].append(paragon)

        else:
            den['Error'] = "Wrong'time' : "+request.args.get('time')
            
    else:
        den['Error'] = "NO 'time'"
    return jsonify(den)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)
    # app.run(debug=True)
    app.run(threaded=True)