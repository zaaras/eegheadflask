from flask import Flask, url_for
from flask import json
from flask import request
from sklearn.externals import joblib

import numpy as np
import sys
import matplotlib.pyplot as pyplot
import pylab as pl

app = Flask(__name__)

delta = [];
high_alpha = [];
high_beta = [];
low_alpha = [];
low_beta = [];
low_gamma = [];
mid_gamma = [];
theta = [];
time = [];
attention_native = [];
meditation_native = [];
waves = [];

@app.route('/')
def api_root():
	return 'Welcome'


@app.route('/post_test', methods = ['POST'])
def api_post_test():
	data = request.get_json()
	print data
	return json.jsonify({'received_text': data['text']})


@app.route('/post_waves', methods = ['POST'])
def api_post_waves():
	data = request.get_json()
	data2 = json.dumps(data)
	data2 = json.loads(data2)
	for d in data2:
		time.append(d[0])
		delta.append((d[1])['wave0'])
		high_alpha.append((d[1])['wave1'])
		high_beta.append((d[1])['wave2'])
		low_alpha.append((d[1])['wave3'])
		low_beta.append((d[1])['wave4'])
		low_gamma.append((d[1])['wave5'])
		mid_gamma.append((d[1])['wave6'])
		theta.append((d[1])['wave7'])
		attention_native.append((d[1])['attention'])
		meditation_native.append((d[1])['meditation'])


	waves.append(delta)
	waves.append(high_alpha)
	waves.append(high_beta)
	waves.append(low_alpha)
	waves.append(low_beta)
	waves.append(low_gamma)
	waves.append(mid_gamma)
	waves.append(theta)

	remove_outliers()
	standardize(waves)
	aggregate = [];
	aggregate.append(waves[2]);

	#average(waves)
	#aggregate(waves)

	sampleCount = 0;
	betaSamples = [];
	
	betaSamples.append([])
	print len(aggregate);
	for i in range(len(aggregate)):
		betaSamples[sampleCount].append(aggregate[i])
		if(i%20==0 and i!=0):
			sampleCount += 1;
			betaSamples.append([])


	print (len(attention_native));
	#pl.plot(timeOverall,attention_native,'r');
			
	clf = joblib.load('model.pkl') 	


	for i in range(len(betaSamples)):
		if(len(betaSamples[i])>20):
			del betaSamples[i][20];

	print (len(betaSamples[0]));	
	# target tells svm which waves are grouped so [1,1,1,3] means first 3 are grouped last one is from another group
	for i in range(len(betaSamples)):
		print clf.predict(betaSamples[1])


	print data
	return json.dumps(data)

@app.route('/get_results', methods = ['GET'])
def api_get_results():
	return time


def remove_outliers():
	outliers = []
	for wave in waves:
		for i in range (0,(len(wave)-1)):
			if (wave[i] > 1400000):
				del time[i]
				outliers.append(i)

	for outlier in outliers:
		for wave in waves:
			del wave[outlier]

	return


def standardize(wave):
	mean = np.mean(wave);
	std = np.std(wave);

	#print wave
	newWave=[];
	for value in wave:
		newWave.append((value-mean)/std);

	return newWave;

def average(wave,time_stamps, window) :
        avg_wave = [];
        avg_wave_time = [];
        size = len(wave);
        times = size/window;
        print size;
        print times;
        i = 0;
        j=0;
        count = 0;
        sum = 0;
        for j in range(times):
                avg_wave_time.append(time_stamps[(i+i+window)/2]);
                while(count<window):
                        sum = sum + wave[i];
                        i=i+1;
                        count = count +1;
                avg_wave.append(sum/window);
                sum = 0;
                count = 0;

        return [avg_wave, avg_wave_time];

if __name__ == '__main__':
	app.debug = True
	app.run()
