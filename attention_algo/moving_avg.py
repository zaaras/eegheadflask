#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import matplotlib.pyplot as pyplot
import numpy as np
import pylab as pl


#    str += signalStr + "," + ep.delta + "," + ep.highAlpha
#                                                        + "," + ep.highBeta + "," + ep.lowAlpha + ","
#                                                        + ep.lowBeta + "," + ep.lowGamma + ","
#                                                        + ep.midGamma + "," + ep.theta + "," + attention
#                                                        + "," + meditation;


con = lite.connect('activity_log.db')

def average(wave,time_stamps, window) :
	avg_wave = [];
	avg_wave_time = [];
	size = len(wave);
	times = size/window;
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

with con:    
	cur = con.cursor();    
	cur.execute("SELECT * FROM readings_table");
	rows = cur.fetchall();

	logsQuery = con.cursor();    

	readings = [];
	time_stamp = [];

	highAlpha = [];
	lowAlpha = [];

	highBeta = [];
	lowBeta = [];
	highGamma = [];
	lowGamma = [];
	timeHAlpha = [];
	timeLAlpha = [];
	timeHBeta = [];
	timeLBeta = [];
	timeHGamma = [];
	timeLGamma = [];
	quality = [];
	qualityTime = [];
	logStrings = [];
	logTimes = [];
	attention_native = [];
	timeAttentionNative = [];

	logsQuery.execute("SELECT * FROM activity_table");
	logs = logsQuery.fetchall();

	# logs[0] is the index
	# logs[1] is the text
	# logs[2] is the time_stamp
	

	for log in logs:
		logStrings.append(log[1])
		logTimes.append(int(log[2].split("A")[0].split("T")[1]))

	for row in rows:
		tmp = int(row[0].split(",")[0]);
		quality.append(tmp);
		qualityTime.append(int(row[1].split("A")[0].split("T")[1]));

		#change later, currently being sent as string
		if(row[0].split(",")[9] not in 'null'):
			attention_native.append(int(row[0].split(",")[9]));
			timeAttentionNative.append(int(row[1].split("A")[0].split("T")[1]));

		tmp = int(row[0].split(",")[2]);
		if(not(tmp>20000000)):
			highAlpha.append(tmp);
			timeHAlpha.append(int(row[1].split("A")[0].split("T")[1]));


		tmp = int(row[0].split(",")[2]);
		if(not(tmp>20000000)):
			lowAlpha.append(tmp);
			timeLAlpha.append(int(row[1].split("A")[0].split("T")[1]));

		
		tmp = int(row[0].split(",")[3]);
		if(not(tmp>20000000)):
			highBeta.append(tmp);
			timeHBeta.append(int(row[1].split("A")[0].split("T")[1]));

		tmp = int(row[0].split(",")[5]);
		if(not(tmp>20000000)):
			lowBeta.append(tmp);
			timeLBeta.append(int(row[1].split("A")[0].split("T")[1]));

		tmp = int(row[0].split(",")[2]);
		if(not(tmp>20000000)):
			highGamma.append(tmp);
			timeHGamma.append(int(row[1].split("A")[0].split("T")[1]));

		tmp = int(row[0].split(",")[6]);
		if(not(tmp>20000000)):
			lowGamma.append(tmp);
			timeLGamma.append(int(row[1].split("A")[0].split("T")[1]));

	mean = np.mean(highAlpha);
	std = np.std(highAlpha);
	highAlpha_new=[];
	for num in highAlpha:
		highAlpha_new.append((num-mean)/std);

	mean = np.mean(lowAlpha);
	std = np.std(lowAlpha);
	lowAlpha_new=[];
	for num in lowAlpha:
		lowAlpha_new.append((num-mean)/std);


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

	highBetaOverAlpha = [];
	for i in range(0, min(len(highAlpha_new),len(highBeta_new))):
		highBetaOverAlpha.append(highAlpha_new[i]/highBeta_new[i]);

	lowBetaOverAlpha = [];
	for i in range(0,min(len(lowAlpha_new),len(lowBeta_new))):
		lowBetaOverAlpha.append(lowAlpha_new[i]/lowBeta_new[i]);

#--------------------------------------------
	y_av = average(highGamma_new,timeHGamma, 10);
	mean = np.mean(y_av[0]);
	attentionhg = [];

	for i in range(len(y_av[1])):
		if (y_av[0])[i] > mean:
			attentionhg.append(1);
		else:
			attentionhg.append(0);
#---------------------------------------------
	y_av = average(lowGamma_new,timeLGamma, 10);
	mean = np.mean(y_av[0]);
	attentionlg = [];

	for i in range(len(y_av[1])):
		if (y_av[0])[i] > mean:
			attentionlg.append(1); #(y_av[1])[i]
		else:
			attentionlg.append(0);
#------------------------------------------------
	y_av = average(highBeta_new,timeHBeta, 10);
	mean = np.mean(y_av[0]);
	attentionhb = [];

	for i in range(len(y_av[1])):
		if (y_av[0])[i] > mean:
			attentionhb.append((y_av[0])[i]);
		else:
			attentionhb.append(0);
#-------------------------------------------------
	y_av = average(lowBeta_new,timeLBeta, 10);
	mean = np.mean(y_av[0]);
	attentionlb = [];

	for i in range(len(y_av[1])):
		if (y_av[0])[i] > mean:
			attentionlb.append((y_av[0])[i]);
		else:
			attentionlb.append(0);

	aggregate = []
	# change to max
	#for i in range(min([len(attentionlb),len(attentionhb),len(attentionhg),len(attentionlg)])):
	#	aggregate.append((attentionlb[i] + attentionhb[i] + attentionhg[i] + attentionlg[i]));

	for i in range(min([len(attentionhb),len(attentionlb)])):
		aggregate.append(attentionhb[i]+attentionlb[i]);

	pl.subplot(9,1,1)
	signal_quality = pl.plot(qualityTime,quality,'b',label="Signal Quality");
	
	avg_attention = average(attention_native, timeAttentionNative, 10);
	pl.subplot(9,1,2);
	attention = pl.plot(avg_attention[1],avg_attention[0],'r',label="Native Attention");
	#attention = pl.plot(timeAttentionNative,attention_native,'r',label="Native Attention");
	pl.legend();	
	count = 0;
	for time in logTimes:
		pl.annotate(logStrings[count], xy=(time,0), xytext=(-10,10),
			textcoords = 'offset points', ha = 'center', va = 'bottom')
		count += 1;
		pl.axvline(time,ymin=0,ymax=max(y_av[0]), linewidth=1)



	pl.subplot(9,1,3);
	count = 0;
	for time in logTimes:
		pl.annotate(logStrings[count], xy=(time,0), xytext=(-10,10),
			textcoords = 'offset points', ha = 'center', va = 'bottom')
		count += 1;
		pl.axvline(time,ymin=0,ymax=max(y_av[0]), linewidth=1)


	avg_highGamma = average(highGamma_new,timeHGamma, 10);
	aggregate_atten = pl.plot(avg_highGamma[1],aggregate,'r',label="Aggregate");
	pl.legend();	

	pl.subplot(9,1,4);
	high_gamma = pl.plot(avg_highGamma[1],avg_highGamma[0],'r',label="High Gamma");
	pl.legend();

	avg_lowGamma = average(lowGamma_new,timeLGamma, 10);
	pl.subplot(9,1,5);
	low_gamma = pl.plot(avg_lowGamma[1],avg_lowGamma[0],'r',label="Low Gamma");
	#y_av = movingaverage(highGamma, 500)
	#high_gamma = pl.plot(timeHGamma,y_av,'b',label="High Gamma");
	pl.legend();
	
	avg_highBeta = average(highBeta_new,timeHBeta, 10);
	pl.subplot(9,1,6);
	#y_av = movingaverage(highBeta,500);
	high_beta = pl.plot(avg_highBeta[1],avg_highBeta[0],'r',label="High Beta");
	pl.legend();	

	avg_lowBeta = average(lowBeta_new,timeLBeta, 10);
	pl.subplot(9,1,7);
	#y_av = movingaverage(lowBeta, 500)
	#low_beta = pl.plot(timeLBeta,y_av,'g',label="Low Beta");
	low_beta = pl.plot(avg_lowBeta[1],avg_lowBeta[0],'r',label="Low Beta");
	pl.legend();


	avg_highBetaOverAlpha = average(highBetaOverAlpha,timeHBeta, 10);
	pl.subplot(9,1,8);
	#y_av = movingaverage(lowBeta, 500)
	#low_beta = pl.plot(timeLBeta,y_av,'g',label="Low Beta");
	low_beta = pl.plot(avg_highBetaOverAlpha[1],avg_highBetaOverAlpha[0],'r',label="High beta over alpha");
	pl.legend();

	avg_lowBetaOverAlpha = average(lowBetaOverAlpha,timeLBeta, 10);
	pl.subplot(9,1,9);
	#y_av = movingaverage(lowBeta, 500)
	#low_beta = pl.plot(timeLBeta,y_av,'g',label="Low Beta");
	low_beta = pl.plot(avg_lowBetaOverAlpha[1],avg_lowBetaOverAlpha[0],'r',label="low beta over alpha");
	pl.legend();
		
	pl.show();
