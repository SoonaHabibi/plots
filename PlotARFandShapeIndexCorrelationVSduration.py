# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 07:51:26 2022

@author: sardekani
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 06:24:18 2022

@author: sardekani
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import random 
import matplotlib.lines as mlines
import seaborn as sns
import scipy as sp

indir='P:/2021/ArizonaStorm/Regionality/lmoment/'

# Area Ar to generate map for ARF comparison in Sq Mile
AreaAr=[100, 300,1000,2000]

# Return Period Ar to generate map for ARF comparison
RP_Ar=[2,10,100]
RP_Ar=['2yr','10yr','100yr']

durationAr=['1h', '2h', '3h', '6h', '12h', '18h', '1d', '2d', '3d','5d','7d']
durationHrAr=[1,2,3,6,12,18,24,48,72,84,168]
durLabel=['1-hour', '2-hour', '3-hour', '6-hour', '12-hour', '18-hour', '1-day', '2-day', '3-day','5-day','7-day']

# To convert sq KM to sq Mile
conv=0.3861
     
title=['2-yr', '10-yr','100-yr']
y_label=['100 $mile^2$','300 $mile^2$','1000 $mile^2$','2000 $mile^2$']

# List of keys
keys = ["RP2_A100", "RP2_A300", "RP2_A1000", "RP2_A2000", "RP10_A100", "RP10_A300", "RP10_A1000", "RP10_A2000","RP100_A100", "RP100_A300", "RP100_A1000", "RP100_A2000"]

for i in range(12):
    globals()['Cor_ind%s' %str(i)]=[]
    globals()['P_ind%s' %str(i)]=[]
# create correlation dictionary
CorDict = dict.fromkeys(keys, [])

# create correlation dictionary
P_Dict = dict.fromkeys(keys, [])

# GEnerate map for each duration
for ind, dur in enumerate(durationAr): 
    infile='P:/2021/ArizonaStorm/GIS/shp/HUC8_dur'+dur+'_ARF_v2.shp'
    gdb=gpd.read_file(infile)
    HUC8_ARF=gdb.to_crs('epsg:2868')
    # A/l^2 
    HUC8_ARF['Al2']=HUC8_ARF.area/HUC8_ARF.length/HUC8_ARF.length

    HUC8_ARF['AreaSqMile']=HUC8_ARF['AreaSqKm']*conv

    keyInd=0
    # fig, axs = plt.subplots(4, 3)
    # fig.set_size_inches(15, 18)  #set it big enough for all subplots
    for i , area in enumerate(AreaAr):
        for j, RP in enumerate(RP_Ar):
            col=RP+'_'+str(area)+'sqMile'
            # Since shapefile columns name can't be longer than 10 in length
            col=col[0:10]
            HUC8_ARF.loc[HUC8_ARF['AreaSqMile']<area,col]=np.nan
            # corelation and p-value
            df=HUC8_ARF[['Al2',col]].dropna()
            key1='RP'+RP[:-2]+'_A'+str(area)
            print(key1)
            r, p = sp.stats.pearsonr(df['Al2'],df[col])
            globals()['P_ind%s' %keyInd].append(round(p,2))
            globals()['Cor_ind%s' %keyInd].append(round(r,2))
            keyInd+=1

# write correlation and p-values into a dataframe
Cor=[]
P=[]
for i in range(12): 
    Cor.append(globals()['Cor_ind%s' %str(i)])
    P.append(globals()['P_ind%s' %str(i)])
CorAr=np.array(Cor)
PAr=np.array(P)
df_Cor=pd.DataFrame(CorAr.T,columns=keys)
df_P=pd.DataFrame(PAr.T,columns=keys)
df_P['duration']=durLabel
df_Cor['duration']=durLabel
df_P['duration1']=list(np.arange(11))
df_Cor['duration1']=list(np.arange(11))

#get the min and and max values 
maxCor=max(df_Cor.iloc[:,:-2].max())
minCor=min(df_Cor.iloc[:,:-2].min())
maxP=max(df_P.iloc[:,:-2].max())
minP=min(df_P.iloc[:,:-2].min())

# generate subplot of correlation versus duration
plt.style.use('seaborn-white')
fig, axs = plt.subplots(4, 3)
fig.set_size_inches(15, 18)
for i , area in enumerate(AreaAr):
    for j, RP in enumerate(RP_Ar):
        col='RP'+RP[:-2]+'_A'+str(area)
        ax=sns.scatterplot(ax=axs[i][j],x='duration',y=col, data=df_Cor, color='royalblue')
        ax.set_ylim([minCor, maxCor])
        ax.set(xlabel=None)
        ax.set(ylabel=None)
        
        if i!=3:
            ax.set(xticklabels=[])
        if (i==0):
            ax.set_title(title[j], fontweight='bold', fontsize=20)
            ax.xaxis.labelpad = 50
        if (j==2):
            ax.set_ylabel(y_label[i], rotation=0,fontweight='bold', fontsize=20)
            ax.yaxis.labelpad = -333
        else:
            ax.set(ylabel=None)
        # ax2 = plt.twinx()
        # sns.scatterplot(ax=axs[i][j],x='duration1',y=col, data=df_P, color='red')
        # ax.set(xlabel=None)
        # ax.set(ylabel=None)
plt.setp(axs[3,0].get_xticklabels(), rotation=90)
plt.setp(axs[3,1].get_xticklabels(), rotation=90)
plt.setp(axs[3,2].get_xticklabels(), rotation=90)
fig.text(0.5, 0.04, 'Duration', ha='center', fontsize=20, fontweight='bold')
fig.text(0.07, 0.5, 'Correlation', va='center', rotation='vertical', fontsize=20, fontweight='bold')        
        
outfile="P:/2021/ArizonaStorm/Regionality/Map/CorrelationVsDuration_DARfVsShapeIndex2.jpg"
plt.savefig(outfile, bbox_inches='tight')
    
# generate subplot of pvalue versus duration
plt.style.use('seaborn')
fig, axs = plt.subplots(4, 3)
fig.set_size_inches(15, 18)
for i , area in enumerate(AreaAr):
    for j, RP in enumerate(RP_Ar):
        col='RP'+RP[:-2]+'_A'+str(area)
        ax=sns.scatterplot(ax=axs[i][j],x='duration',y=col, data=df_P, color='royalblue')
        ax.set_ylim([minP, maxP])
        ax.set(xlabel=None)
        ax.set(ylabel=None)
        
        if i!=3:
            ax.set(xticklabels=[])
        if (i==0):
            ax.set_title(title[j], fontweight='bold', fontsize=20)
            ax.xaxis.labelpad = 50
        if (j==2):
            ax.set_ylabel(y_label[i], rotation=0,fontweight='bold', fontsize=20)
            ax.yaxis.labelpad = -333
        else:
            ax.set(ylabel=None)
        # ax2 = plt.twinx()
        # sns.scatterplot(ax=axs[i][j],x='duration1',y=col, data=df_P, color='red')
        # ax.set(xlabel=None)
        # ax.set(ylabel=None)
plt.setp(axs[3,0].get_xticklabels(), rotation=90)
plt.setp(axs[3,1].get_xticklabels(), rotation=90)
plt.setp(axs[3,2].get_xticklabels(), rotation=90)
fig.text(0.5, 0.04, 'Duration', ha='center', fontsize=20, fontweight='bold')
fig.text(0.07, 0.5, 'P-value', va='center', rotation='vertical', fontsize=20, fontweight='bold')        
        
outfile="P:/2021/ArizonaStorm/Regionality/Map/PvalueVsDuration_DARfVsShapeIndex2.jpg"
plt.savefig(outfile, bbox_inches='tight')
    
      