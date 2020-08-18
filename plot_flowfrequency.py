# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:59:23 2020

@author: sardekani
"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as font_manager
import numpy as np

# Path for the input flood frequency data, containing all the gages
infile1 = '//westfolsom/Projects/2019/USACE Omaha/Platte_River/chapter7/Gage_FloodFrequency.csv'
# Path for the input data, distance of each gage from the Mouth of Platte River
infile2 = '//westfolsom/Projects/2019/USACE Omaha/Platte_River/chapter7/Gage_distance_frequency.csv'
# Path for the exceedance Interval 
infile3 = '//westfolsom/Projects/2019/USACE Omaha/Platte_River/chapter7/Gage_FloodFrequencyProbability.csv'

# read csv files
df1 = pd.read_csv(infile1, header = 0)
df2 = pd.read_csv(infile2, header = 0)
df4 = pd.read_csv(infile3, header = 0)

dis = df2.iloc[:,1]
yr2 = df1.iloc[:,8]
yr5 = df1.iloc[:,7]
yr10 = df1.iloc[:,6]
yr25 = df1.iloc[:,5]
yr50 = df1.iloc[:,4]
yr100 = df1.iloc[:,3]
yr200 = df1.iloc[:,2]
yr500 = df1.iloc[:,1]

#
# plot   
#

# Define the font format for the axis label
font = FontProperties()
font.set_family('serif')
font.set_name('Times New Roman')
font.set_size(14)
font.set_weight('bold')

font2 = FontProperties()
font2.set_family('serif')
font2.set_name('Times New Roman')
font2.set_size(14)

font2 = FontProperties()
font2.set_family('serif')
font2.set_name('Times New Roman')
font2.set_size(13)

fig=plt.figure(1)
# Define the dimension of the plot
fig.set_figheight(8)
fig.set_figwidth(15)
    
ax = plt.subplot(111)
ax.set_yscale('log')
ax.set_xlim(300,150)
ax.set_ylim(1000,1000000) 
ax.set_ylabel('Flow (cfs)', fontproperties=font)
ax.set_xlabel('Distance Upstream from Mouth of Platte River (miles)', fontproperties=font)
# Add grid to the plot
ax.grid(True, color='lightgray', which = 'both')

# Add thousand comma to the y axis values
ax.get_yaxis().set_major_formatter(
matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax.plot(dis, yr2, '-bo', label='2-yr')
ax.plot(dis, yr5, '-ro', label='5-yr')
ax.plot(dis, yr10, '-go', label='10-yr')
ax.plot(dis, yr25, '-co', label='25-yr')
ax.plot(dis, yr50, '-yo', label='50-yr')
ax.plot(dis, yr100, '-mo', label='100-yr')
ax.plot(dis, yr200, linestyle='-', marker='o', color='sienna', label='200-yr')
ax.plot(dis, yr500, linestyle='-', marker='o', color='lime', label='500-yr')
ax.legend(loc='upper right', prop=font2)

ax.text(dis[0], 1000000, "- PR near Brady", rotation=90, fontproperties=font2)
ax.text(dis[1], 1000000, "- PR near Cozad", ha='center', rotation=90, fontproperties=font2)
ax.text(dis[2], 1000000, "- PR near Overton", ha='center', rotation=90, fontproperties=font2)
ax.text(dis[3], 1000000, "- PR near Odessa", ha='center', rotation=90, fontproperties=font2)
ax.text(dis[4], 1000000, "- PR near Kearney", ha='center', rotation=90, fontproperties=font2)
ax.text(dis[5], 1000000, "- PR near Grand Island ", ha='center', rotation=90, fontproperties=font2)

#plt.show()
img_path = '//westfolsom/Projects/2019/USACE Omaha/Platte_River/chapter7/PeakFlowFreq.jpg'
plt.savefig(img_path)  

##
## To plot frequency curve
##
#station_name = df1.iloc[:,0]
#flow1 = df4.iloc[:,2]
#flow2 = df4.iloc[:,3]
#flow3 = df4.iloc[:,4]
#flow4 = df4.iloc[:,5]
#flow5 = df4.iloc[:,6]
#flow6 = df4.iloc[:,7]
#returnp = df4.iloc[:,0]
#exc_prob = df4.iloc[:,1]
#
#fig=plt.figure(1)
## Define the dimension of the plot
#fig.set_figheight(10)
#fig.set_figwidth(8)
#    
#ax1 = plt.subplot(111)
#ax1.set_yscale('log')
#ax1.set_xscale('log')
#ax1.set_xlim(1,500)
#ax1.set_ylim(100,100000) 
#ax1.set_ylabel('Flow (cfs)', fontproperties=font)
#ax1.set_xlabel('Distance Upstream from Mouth of Platte River (miles)', fontproperties=font)
## Add grid to the plot
#ax1.grid(True, color='lightgray', which = 'both')

# Add thousand comma to the y axis values
ax1.get_yaxis().set_major_formatter(
matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax1.plot(returnp, flow1, '-bo', label=station_name[0])
ax1.plot(returnp, flow2, '-ro', label=station_name[1])
ax1.plot(returnp, flow3, '-go', label=station_name[2])
ax1.plot(returnp, flow4, '-co', label=station_name[3])
ax1.plot(returnp, flow5, '-yo', label=station_name[4])
ax1.plot(returnp, flow6, '-mo', label=station_name[5])

ax1.legend(loc='upper right', prop=font1)

#
# 0.5 mile Interpolation
#
xvals = np.arange(max(dis), min(dis)-0.5, -0.5)
yr2_Ar = np.round(np.interp(xvals,  dis.values[::-1], yr2.values[::-1]),-1)
yr5_Ar = np.round(np.interp(xvals,  dis.values[::-1], yr5.values[::-1]),-1)
yr10_Ar = np.round(np.interp(xvals, dis.values[::-1], yr10.values[::-1]),-1)
yr25_Ar = np.round(np.interp(xvals, dis.values[::-1], yr25.values[::-1]),-1)
yr50_Ar = np.round(np.interp(xvals, dis.values[::-1], yr50.values[::-1]),-1)
yr100_Ar = np.round(np.interp(xvals, dis.values[::-1], yr100.values[::-1]),-1)
yr200_Ar = np.round(np.interp(xvals, dis.values[::-1], yr200.values[::-1]),-1)
yr500_Ar = np.round(np.interp(xvals, dis.values[::-1], yr500.values[::-1]),-1)


df3=pd.DataFrame([xvals[::-1],yr2_Ar[::-1], yr5_Ar[::-1], yr10_Ar[::-1], yr25_Ar[::-1], yr50_Ar[::-1], yr100_Ar[::-1], yr200_Ar[::-1], yr500_Ar[::-1]]).transpose()
df3.columns = ['River Mile','2-yr', '5-yr', '10-yr', '25-yr', '50-yr', '100-yr', '200-yr', '500-yr']
CSVoutput='//westfolsom/Projects/2019/USACE Omaha/Platte_River/chapter7/flowfreq0point5mile2.csv'
df3.to_csv(CSVoutput, index=False)