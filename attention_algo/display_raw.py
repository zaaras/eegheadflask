#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import matplotlib.pyplot as pyplot
import numpy as np
import pylab as pl

con = lite.connect('/home/umar/Downloads/activityLog.db')


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
	high_beta = pl.plot(time,highBeta,'r',label="High Beta");
	low_beta = pl.plot(time,lowBeta,'g',label="Low Beta");
	high_gamma = pl.plot(time,highGamma,'b',label="High Gamma");
	low_gamma = pl.plot(time,lowGamma, 'y',label="Low Gamma");


	pl.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.);

	pl.show();
