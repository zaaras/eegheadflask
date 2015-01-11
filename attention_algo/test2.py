#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import matplotlib.pyplot as pyplot
import numpy as np
import pylab as pl

con = lite.connect('activityLog_new.db')

with con:    

	cur = con.cursor();    
	cur.execute("SELECT * FROM readings_table");

	readings = [];
	time_stamp = [];
	highBeta = [];
	lowBeta = [];
	highGamma = [];
	lowGamma = [];
	timeHBeta = [];
	timeLBeta = [];
	timeHGamma = [];
	timeLGamma = [];
	rows = cur.fetchall();

	for row in rows:
		tmp = int(row[0].split(",")[3]);
		if(not(tmp>14000000)):
			highBeta.append(tmp);
			timeHBeta.append(int(row[1].split("A")[0].split("T")[1]));
		tmp = int(row[0].split(",")[5]);
		if(not(tmp>14000000)):
			lowBeta.append(tmp);
			timeLBeta.append(int(row[1].split("A")[0].split("T")[1]));
		tmp = int(row[0].split(",")[2]);
		if(not(tmp>14000000)):
			highGamma.append(tmp);
			timeHGamma.append(int(row[1].split("A")[0].split("T")[1]));
		tmp = int(row[0].split(",")[6]);
		if(not(tmp>14000000)):
			lowGamma.append(tmp);
			timeLGamma.append(int(row[1].split("A")[0].split("T")[1]));

	mean = np.mean(highBeta);
	std = np.std(highBeta);

	highBeta_new=[];
	for num in highBeta:
		highBeta_new.append((num-mean)/std);

	mean = np.mean(lowBeta);
	std = np.std(lowBeta);

	lowBeta_new=[];
	for num in lowBeta:
		lowBeta_new.append((num-mean)/std);

	mean = np.mean(highGamma);
	std = np.std(highGamma);

	highGamma_new=[];
	for num in highGamma:
		highGamma_new.append((num-mean)/std);
	
	lowGamma_new=[];
	mean = np.mean(lowGamma);
	std = np.std(lowGamma);

	lowGamma_new=[];
	for num in lowGamma:
		lowGamma_new.append((num-mean)/std);


	def movingaverage(interval, window_size):
    		window= np.ones(int(window_size))/float(window_size)
    		return np.convolve(interval, window, 'same')


	av = [];
	mean_Gamma = np.mean(highGamma);
	for item in highGamma:
		if item > mean:
			av.append(1);
		else:
			av.append(0);


	y_av = movingaverage(highGamma, 100)
	mean = np.mean(y_av);
	attention = [];

	for i in range(len(y_av)):
		if y_av[i] > mean*1.20:
			attention.append(timeHGamma[i]);
		else:
			attention.append(0);

	print attention;

	#print time;
	pl.subplot(4,1,1);
	y_av = movingaverage(highBeta,100);
	high_beta = pl.plot(timeHBeta,y_av,'r',label="High Beta");
	pl.legend();	
	#pl.xlim(131118,141203);
	
	pl.subplot(4,1,2);
	y_av = movingaverage(lowBeta, 100)
	low_beta = pl.plot(timeLBeta,y_av,'g',label="Low Beta");
	pl.legend();
	#pl.xlim(140817,141203);
	pl.subplot(4,1,3);
	y_av = movingaverage(highGamma, 100)
	high_gamma = pl.plot(timeHGamma,y_av,'b',label="High Gamma");
	pl.legend();
	#pl.xlim(140817,141203);
	pl.subplot(4,1,4);
	y_av = movingaverage(lowGamma, 100)
	low_gamma = pl.plot(timeLGamma,y_av, 'y',label="Low Gamma");
	pl.legend();
	#pl.xlim(140817,141203);
	pl.show();
