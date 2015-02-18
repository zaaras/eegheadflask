#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import matplotlib.pyplot as pyplot
import numpy as np
import pylab as pl
from array import array
from  sklearn import svm


con = lite.connect('test.db')

def average(wave,time_stamps, window) :
	avg_wave = [];
	avg_wave_time = [];
	size = len(wave);
	times = size/window;
	#print size;
	#print times;
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
		
def movingaverage(interval, window_size):
   	window= np.ones(int(window_size))/float(window_size)
   	return np.convolve(interval, window, 'same')


def standardize(wave):
	mean = np.mean(wave);
	std = np.std(wave);

	#print wave
	newWave=[];
	for value in wave:
		newWave.append((value-mean)/std);

	return newWave;

def getIndexTime(timefun, period):

	for i in range(len(period)):
		if(timefun<=period[i]):
			return i;

	return -1;


with con:    
	cur = con.cursor();    
	cur.execute("SELECT * FROM readings_table");
	rows = cur.fetchall();
	logsQuery = con.cursor();    

	timeOverall = []
	logStrings = [];
	logTimes = [];

	waves = [];

	samples = [];

	logsQuery.execute("SELECT * FROM activity_table");
	logs = logsQuery.fetchall();

	# logs[0] is the index
	# logs[1] is the text
	# logs[2] is the time_stamp
	
	attention_native = [];
	for i in range(0,15):
		waves.append([]);

	for log in logs:
		logStrings.append(log[1])
		logTimes.append(int(log[2].split("A")[0].split("T")[1]))

	for row in rows:
		skip = 0 
		for i in range(1,9):
			tmp = float(row[0].split(",")[i]);
			if(tmp>1400000.0):
				skip = 1

		if(skip==0):
			for i in range(1,9):
				tmp = float(row[0].split(",")[i]);
				waves[i].append(tmp);
			
			#quality.append(int(row[0].split(",")[0]));
			#delta.append(int(row[0].split(",")[1]));
			#highAlpha.append(int(row[0].split(",")[2]));
			#highBeta.append(int(row[0].split(",")[3]));
			#lowAlpha.append(int(row[0].split(",")[4]));
			#lowBeta.append(int(row[0].split(",")[5]));
			#lowGamma.append(int(row[0].split(",")[6]));
			#highGamma.append(int(row[0].split(",")[7]));
			#theta.append(int(row[0].split(",")[8]));
		
			timeOverall.append(int(row[1].split("A")[0].split("T")[1]));

			

	for i in range(1,8):
		waves[i] = standardize(waves[i]);

	aggregate = []

	attention_native = waves[9];
	print waves[9];
	for i in range(len(timeOverall)):
		tmp = 0.0;
		for j in range(1,8):
			tmp += waves[j][i]
		aggregate.append(waves[5][i]);


	sampleCount = 0;
	sampleIndexes = [];
	betaSamples = [];
	target = [];
	sections = [];
	maxSection = 0;
	startIndex=0;
	endIndex=0;
	atten = 0;

	betaSamples.append([])
	compensate = 0;
	print len(aggregate);
	for i in range(len(aggregate)):
		betaSamples[sampleCount].append(aggregate[i])
		if(i%20==0 and i!=0):
			print "enter";
			sampleCount += 1;
			betaSamples.append([])


	print (len(attention_native));
	print (len(timeOverall));
	#pl.plot(timeOverall,attention_native,'r');
			
	from sklearn.externals import joblib
	clf = joblib.load('model.pkl') 	


	for i in range(len(betaSamples)):
		if(len(betaSamples[i])>20):
			del betaSamples[i][20];

	print (len(betaSamples[0]));	
	# target tells svm which waves are grouped so [1,1,1,3] means first 3 are grouped last one is from another group
	for i in range(len(betaSamples)):
		print clf.predict(betaSamples[1])

	#pl.show();
