# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 11:08:24 2022

@author: sardekani
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

linkdir="P:/2021/ArizonaStorm/BasinAvg/AORC/Conectivity/link/"
basindir="P:/2021/ArizonaStorm/BasinAvg/AORC/CSV_BasinAvg/"
Shapefile="P:/2021/ArizonaStorm/GIS/shp/SelectedHUC12_IntersAORC_EPSG4269_CorrArea.shp"
gdb=gpd.read_file(Shapefile)

# convert sq Km to sq Mile
c=0.38610216

#interconnected HUC12
filename="‪P:/2021/ArizonaStorm/BasinAvg/AORC/InterHUC12_IntersAORC_EPSG4269_CorrArea.csv"
df_agg=pd.read_csv(filename.lstrip('\u202a'))
df_agg['AreaSqMile']=df_agg.AreaSqKm*c
Area_agg=df_agg['AreaSqMile']

#HUC12s 
filename1="‪P:/2021/ArizonaStorm/BasinAvg/AORC/SelectedHUC12_IntersAORC_EPSG4269_CorrArea.csv"
df_huc12s=pd.read_csv(filename1.lstrip('\u202a'))
df_huc12s['AreaSqMile']=df_huc12s.AreaSqKm*c
Areahuc12=df_huc12s['AreaSqMile']
   
Area_agg=Area_agg[Area_agg<600]
Areahuc12=Areahuc12[Areahuc12<600]

binBoundaries = np.linspace(0,600,60)

# Generate histogram of the whole study area
plt.style.use('ggplot')
plt.rc('font', size=20) 
# plt.rcParams["figure.autolayout"] = True
fig,ax=plt.subplots(3, figsize=(24,8)) 
fig.tight_layout(w_pad=2)  
ax1 = plt.subplot(1,3,1)   
ax1.hist(Areahuc12, bins=binBoundaries, color='cornflowerblue', edgecolor="white")
ax1.set_xlim([0,300])
ax1.set_ylim([0,2000])
ax1.set_yticks([0,500,1000,1500,2000])
ax1.set_xlabel('Area ($mile^{2}$)')
ax1.set_ylabel('Count')
ax1.set_title('HUC12s')
ax2 = plt.subplot(1,3,2)  
ax2.hist(Area_agg, bins=binBoundaries, color='cornflowerblue', edgecolor="white")
ax2.set_xlim([0,300])
ax2.set_ylim([0,2000])
ax2.set_yticks([0,500,1000,1500,2000])
ax2.set_xlabel('Area ($mile^{2}$)')
ax2.set_ylabel('Count')
ax2.set_title('Aggregated HUC12s')
ax3 = plt.subplot(1,3,3)  
ax3.hist(np.append(Areahuc12,Area_agg), bins=binBoundaries, color='cornflowerblue', edgecolor="white")
ax3.set_xlim([0,300])
ax3.set_ylim([0,2000]) 
ax3.set_yticks([0,500,1000,1500,2000])  
ax3.set_xlabel('Area ($mile^{2}$)')
ax3.set_ylabel('Count')
ax3.set_title('All')
 
outfile='P:/2021/ArizonaStorm/Regionality/SomeOfPlotsForReport/AllWatershed_Histogram1.jpg'
plt.savefig(outfile)  
    
#Select all HUC12s inside HUC08=15060105
df_agg['HUC12']=df_agg.HUC12.astype('str')
df_huc12s['HUC12']=df_huc12s.HUC12.astype('str')
df_int_15060105=df_agg[df_agg.HUC12.str.slice(0,8)=='15060105']
df_huc12_15060105=df_huc12s[df_huc12s.HUC12.str.slice(0,8)=='15060105']
Area_agg_1=df_int_15060105.AreaSqKm*c
Areahuc12_1=df_huc12_15060105.AreaSqKm*c

binBoundaries = np.linspace(0,60,15)

# Generate histogram of huc12 and interconnected basins area
plt.style.use('ggplot')
plt.rc('font', size=20)
# plt.rcParams["figure.autolayout"] = True
fig, ax=plt.subplots(3, figsize=(24,8))    
fig.tight_layout(w_pad=2)
ax1 = plt.subplot(1,3,1)   
ax1.hist(Areahuc12_1, bins=binBoundaries, color='cornflowerblue', edgecolor="white")
ax1.set_xlim([0,60])
ax1.set_ylim([0,20])
ax1.set_yticks([0,5,10,15,20])
ax1.set_xlabel('Area ($mile^{2}$)')
ax1.set_ylabel('Count')
ax1.set_title('HUC12s')
ax2 = plt.subplot(1,3,2)  
ax2.hist(Area_agg_1, bins=binBoundaries, color='cornflowerblue', edgecolor="white")
ax2.set_xlim([0,60])
ax2.set_ylim([0,20])
ax2.set_yticks([0,5,10,15,20])
ax2.set_xlabel('Area ($mile^{2}$)')
ax2.set_ylabel('Count')
ax2.set_title('Aggregated HUC12s')
ax3 = plt.subplot(1,3,3)  
ax3.hist(np.append(Areahuc12_1,Area_agg_1), bins=binBoundaries, color='cornflowerblue', edgecolor="white")
ax3.set_xlim([0,60])
ax3.set_ylim([0,20]) 
ax3.set_yticks([0,5,10,15,20])
ax3.set_xlabel('Area ($mile^{2}$)')
ax3.set_ylabel('Count')
ax3.set_title('All')

outfile='P:/2021/ArizonaStorm/Regionality/SomeOfPlotsForReport/HUC15060105_Histogram.jpg'
plt.savefig(outfile)
plt.savefig(outfile, bbox_inches='tight')