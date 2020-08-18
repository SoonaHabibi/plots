# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:20:47 2019

@author: sardekani
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime

dir = "//westfolsom/projects/2019/USACE Omaha/Platte_River/DegreeDay/"
input = dir + 'GrandIsland/PeakDate_GrandIsland.csv'
outdir = dir + 'FloodReason/'
if not os.path.exists(outdir): os.mkdir(outdir)

df = pd.read_csv(input)                         # Date that Annual peak flow is occuring in snow season              
#df['PeakDate'] = df['PeakDate'].apply(lambda x:datetime.strptime(x, "%m/%d/%Y"))

for i in range(len(df)):                            # read and save the rows for date that annual maximum flow occured 
    yr = df['Year'][i]
    date = df['PeakDate'][i]
    infile = dir + "USW00014935_AFDD/alldata_" + str(yr) + ".csv"
    df2 = pd.read_csv(infile)    
    ind = df2['DATE'].index[df2['DATE']==date][0]
    df_new = df2.iloc[ind-35:ind+21]
    output = outdir + str(yr) +'_GrandIsland.csv'
    df_new.to_csv(output, index=False)
    df_new['DATE'] = df_new['DATE'].apply(lambda x:datetime.strptime(x, '%m/%d/%Y'))  #   .strftime('%d_%b'))
    df_new['FLOW PER-AVER'] = df_new['FLOW PER-AVER'].apply(lambda x:int(x))


# plot    
    fig=plt.figure(1)
    fig.set_figheight(15)
    fig.set_figwidth(8)

# vertical dash line at maximum flow
    ind = df_new['FLOW PER-AVER'].index[df_new['FLOW PER-AVER']==max(df_new['FLOW PER-AVER'])][0]
    PeakT_Ar = np.array([df_new['DATE'][ind], df_new['DATE'][ind]]) 
    
    maxPre = max(max(df_new['PRCP']), max(df_new['SNOW']))    # max of snowfall and rainfall
    minPre = min(min(df_new['PRCP']), min(df_new['SNOW']))    # min of snowfall and rainfall
    AFDD_vline = np.array([min(df_new['AFDD']),max(df_new['AFDD'])*1.2])    # y1 and y2 for vertical dash line
    PRCP_vline = np.array([min(df_new['PRCP']),maxPre*1.2])
    flow_vline = np.array([min(df_new['FLOW PER-AVER']),max(df_new['FLOW PER-AVER'])*1.2])
    
    ax1 = plt.subplot(311)
    ax1.plot(df_new['DATE'], df_new['AFDD'], color='blue')
    ax1.plot(PeakT_Ar,AFDD_vline, '--', color='green')
    ax1.set(ylabel='AFDD ($^\circ$F-days)')
    # make these tick labels invisible
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.set_xlim(min(df_new['DATE']),max(df_new['DATE']))
    ax1.set_ylim(min(df_new['AFDD']),max(df_new['AFDD'])*1.2) 
    ax1.grid(True)
    
    ax2 = plt.subplot(312, sharex=ax1)
    ax2.plot(df_new['DATE'], df_new['PRCP'], color='blue')
    ax2.plot(df_new['DATE'], df_new['SNOW'], color='coral')
    ax2.plot(PeakT_Ar,PRCP_vline, '--',color='green')
    ax2.set(ylabel='Depth (in)')
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax2.set_xlim(min(df_new['DATE']), max(df_new['DATE']))
    ax2.set_ylim(minPre, maxPre*1.2)
    ax2.grid(True)  
    ax2.legend(['Incremental Rainfall','Snow'])
    
    ax3 = plt.subplot(313, sharex=ax1)
    ax3.plot(df_new['DATE'], df_new['FLOW PER-AVER'], color='blue')
    ax3.plot(PeakT_Ar,flow_vline, '--',color='green')
    ax3.set(ylabel='Daily Average Flow (cfs)')
    ax3.set(xlabel=str(yr))
    ax3.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b')) 
    ax3.set_xlim(min(df_new['DATE']),max(df_new['DATE']))
    ax3.set_ylim(min(df_new['FLOW PER-AVER']),max(df_new['FLOW PER-AVER'])*1.2)
    ax3.grid(True)
#    plt.show()
    
    img_path = outdir + str(yr) + '_PeakFlow.jpg'
    plt.savefig(img_path)   
