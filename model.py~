#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import matplotlib.pyplot as pyplot
import numpy as np
import pylab as pl
from array import array
from  sklearn import svm


con = lite.connect('activityLog.db')
con2 = lite.connect('newdb.db')

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

			

	for i in range(1,9):
		waves[i] = standardize(waves[i]);

	aggregate = []

	for i in range(len(timeOverall)):
		tmp = 0.0;
		for j in range(1,9):
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

	for i in range(len(logTimes)):
		if ("videoDistract" in logStrings[i]):
			if("videoDoneDistract" in logStrings[i+1]):
				startIndex = getIndexTime(logTimes[i],timeOverall);
				endIndex = getIndexTime(logTimes[i+1],timeOverall);
				atten = 2;
		if ("videoStart" in logStrings[i]):
			if("videoDistract" in logStrings[i+1]):
				startIndex = getIndexTime(logTimes[i],timeOverall);
				endIndex = getIndexTime(logTimes[i+1],timeOverall);
				atten = 1;
			if("videoDone" in logStrings[i+1]):
				startIndex = getIndexTime(logTimes[i],timeOverall);
				endIndex = getIndexTime(logTimes[i+1],timeOverall);
				atten = 1;
		if ("videoEndDistract" in logStrings[i]):
			if("videoDone" in logStrings[i+1]):
				startIndex = getIndexTime(logTimes[i],timeOverall);
				endIndex = getIndexTime(logTimes[i+1],timeOverall);
				atten = 1;

		if ("videoDone" in logStrings[i]):
			if("videoStart" in logStrings[i+1]):
				startIndex = getIndexTime(logTimes[i],timeOverall);
				endIndex = getIndexTime(logTimes[i+1],timeOverall);
				atten = 2;

		if(startIndex!=0):	
			sections.append([startIndex,endIndex,atten]);


	compensate = 0;
	index = 19;
	maxIndex = 0;


	for i in range(len(sections)):

		startIndex = sections[i][0];
		endIndex = sections[i][1];
		maxIndex = sections[len(sections)-1][1];
		
		target.append(sections[i][2]);

	index = 0;
	sampleCount = 0;
	while index+20<len(aggregate):
		betaSamples.append([])
		for i in range(0,20):
			betaSamples[sampleCount].append(aggregate[index+i])
		sampleCount += 1;
		index=index+20;


	target = [];
	for i in range (len(betaSamples)):
		if(len(betaSamples[i])<20):
			del betaSamples[i]
			break;
		
		for k in range(len(betaSamples[i])):
			index = i*20 + k
			for j in range(len(sections)):
				if(index >= sections[j][0] and index <= sections[j][1]):
					break;

			target.append(sections[j][2]);
			break;		
									

	index =0 ;
	print(len(betaSamples));
	print((target));
	clf = svm.SVC(gamma=0.001, C=100);
	clf.fit(betaSamples,target);

	from sklearn.externals import joblib
	joblib.dump(clf,'model.pkl');
	
	# target tells svm which waves are grouped so [1,1,1,3] means first 3 are grouped last one is from another group
	#print clf.predict(betaSamples[1])
