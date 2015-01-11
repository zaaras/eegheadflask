from flask import Flask, url_for
from flask import json
from flask import request

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
	#standardize(waves)
	#average(waves)
	#aggregate(waves)

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
