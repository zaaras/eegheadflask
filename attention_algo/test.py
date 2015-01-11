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
	time = [];
	rows = cur.fetchall();

	for row in rows:
		readings.append(row[0]);
		time_stamp.append(row[1]);

	for item in readings:
		highBeta.append(int(item.split(",")[3]));
		lowBeta.append(int(item.split(",")[5]));
		highGamma.append(int(item.split(",")[2]));
		lowGamma.append(int(item.split(",")[6]));

	for item in time_stamp:
		time.append(item.split("A")[0].split("T")[1]);

	#print time;
	#pl.plot(time,highBeta,'r');
	#pl.plot(time,lowBeta,'g');
	#pl.plot(time,highGamma,'b');
	#pl.plot(time,lowGamma, 'y');
	#pl.xlim(140817,141203);
	#pl.show();

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


	#print time;
	high_beta = pl.plot(time,highBeta_new,'r',label="High Beta");
	low_beta = pl.plot(time,lowBeta_new,'g',label="Low Beta");
	high_gamma = pl.plot(time,highGamma_new,'b',label="High Gamma");
	low_gamma = pl.plot(time,lowGamma_new, 'y',label="Low Gamma");

	#pl.legend([high_beta, low_beta, high_gamma, low_gamma], ('High Beta', 'Low Beta', 'High Gamma','Low Gamma'))

	pl.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.);

#	pl.xlim(140817,141203);
	pl.show();
