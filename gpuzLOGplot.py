#!/usr/bin/python
#Plots data from the GPU-Z log file

import sys
import os.path
import numpy as np
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt


#PRINT HEADER
print('*\n*\n*\n*')
print('********PLot GPU-Z sensor log files data********')


#GET INPUT FILE
if len(sys.argv) > 1:
	fileName = sys.argv[1]
else: 
	fileName	= "GPU-Z Sensor Log.txt"
	print('please provide a log file or rename input file to: \''+str(fileName)+'\'')

if not os.path.isfile(fileName):
	print('input file does not exist')
	sys.exit()
	









#READ FILE

file 		= open(fileName,'r')


#Get syntax from header
rawHeader 		= file.readline()
curv_descriptor	= rawHeader.split(',')
curv_descriptor	= curv_descriptor[1:-1] #remove the Date descriptor

#Get timing info
rawTime			= np.loadtxt(file, dtype=str, delimiter=',', usecols=0)
file.close() 	# resets the file iterator to begin of file
dates			= []
for step in rawTime:
	dates.append(	datetime.strptime(step,'%Y-%m-%d %H:%M:%S.%f ') 	) #might have to adjust formating for days/monts <10 (zero padding in log file?!)

#Get data
file			= open(fileName,'r')
rawData 		= np.loadtxt(file, skiprows=1, delimiter=',', usecols=range(1,len(curv_descriptor)+1)		)	

file.close()


#DEFINE CONSTANTS
nCurves			= len(curv_descriptor)
nSteps			= len(rawTime)
T_dt			= dates[-1] - dates[0]		
T_sec			= T_dt.total_seconds()

#PRINT INFO 
print('found '+str(nCurves) + ' quantities to plot')
print(str(nSteps)+' time steps were recorded over a total timespan of '+str(T_sec)+' seconds')
print('estimates delta T='+str(T_sec/float(nSteps))+' seconds')










#SET UP PLOTTING ARRAYS
time 			= np.zeros(nSteps)
for t in range(1,nSteps):
	delta		= dates[t] - dates[0]
	time[t]		= delta.total_seconds()

data			= np.reshape(rawData,(nSteps,nCurves) )

xlabel = 'time [s]'

##GENERATE THE PLOTS
for i in range(nCurves):
	xmax	= time[np.argmax(rawData[:,i])]
	ymax	= rawData[:,i].max()
	
	plt.plot(time, rawData[:,i],'+-',markersize=1, linewidth=.1 )
	plt.annotate('max val', xy=(xmax, ymax), xytext=(xmax, ymax+5), arrowprops=dict(facecolor='black', shrink=0.01))
	plt.title(curv_descriptor[i])
	plt.xlabel(xlabel)
	plt.show()
