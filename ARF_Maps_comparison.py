# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 05:16:22 2022

@author: sardekani
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import random 
import matplotlib.lines as mlines

indir='P:/2021/ArizonaStorm/Regionality/lmoment/'

# Area Ar to generate map for ARF comparison in Sq Mile
AreaAr=[100, 300,1000,3000]

# Return Period Ar to generate map for ARF comparison
RP_Ar=[2,10,100]
RP_Ar=['2yr','10yr','100yr']

durationAr=['1h', '2h', '3h', '6h', '12h', '18h', '1d', '2d', '3d','5d','7d']
durationHrAr=[1,2,3,6,12,18,24,48,72,84,168]
durLabel=['1-hour', '2-hour', '3-hour', '6-hour', '12-hour', '18-hour', '1-day', '2-day', '3-day','5-day','7-day']

# To convert sq KM to sq Mile
conv=0.3861

# Load Arizona State Boundary
shp1="P:/2021/ArizonaStorm/GIS/shp/ArizonaBoundary.shp"
gdbstate=gpd.read_file(shp1)
    
#Load HUC08 file
shp='P:/2021/ArizonaStorm/GIS/shp/HUC8_ClipHUC6Arizona_HUC12Summary.shp'
HUC8_df=gpd.read_file(shp)[['HUC8','AreaSqKm', 'geometry']]
crs=HUC8_df.crs
HUC8_df.columns=['HUC08','AreaSqKm', 'geometry']

for RP in RP_Ar:
    globals()['Column_RP%s' %RP]=[RP+'_'+str(AreaAr[0])+'sqMile',RP+'_'+str(AreaAr[1])+'sqMile',RP+'_'+str(AreaAr[2])+'sqMile',RP+'_'+str(AreaAr[3])+'sqMile']

# Extract the ARF data for each duration, RP and Area and add it to HUC8 shapefile and save separately for each duration
for ind, dur in enumerate(durationAr[0:1]): 
    HUC8_ARF=HUC8_df
    # RP_dic={'1':[],'2':[],'3':[],'4':[]}
    for ind1, RP in enumerate(RP_Ar):
        ARF_dic={1:[],2:[],3:[],4:[]}
        for huc8 in HUC8_df['HUC08']:
            #Load ARF model parameters
            infile2=indir+"ARF_Model_ParaNSE/ARF_ModelParaNSE_HUC8"+str(huc8)+'_RP'+RP+"_sqmile1.csv"
            df_para=pd.read_csv(infile2)
            w=df_para.w.iloc[ind]
            b=df_para.b.iloc[ind]
            z=df_para.z.iloc[ind]
            v=df_para.v.iloc[ind]
            
            for ind2 in range(len(AreaAr)): 
                A=AreaAr[ind2]
                ARF=(1+w*(A**(z*b)/durationHrAr[ind]**b))**(-v/b)
                ARF_dic[ind2+1].append(ARF)
                
        # Write data into a data frame and then concate to shape file
        df=pd.DataFrame(ARF_dic)
        df.columns=globals()['Column_RP%s' %RP]
        HUC8_ARF=pd.concat([HUC8_ARF,df], axis=1)
    HUC8_ARF.crs=crs
    outfile='P:/2021/ArizonaStorm/GIS/shp/HUC8_dur'+dur+'_ARF.shp'
    HUC8_ARF.to_file(outfile)
        
title=['2-yr', '10-yr','100-yr']
y_label=['100 $mile^2$','300 $mile^2$','1000 $mile^2$','3000 $mile^2$']
# GEnerate map for each duration
for ind, dur in enumerate(durationAr[0:1]): 
    infile='P:/2021/ArizonaStorm/GIS/shp/HUC8_dur'+dur+'_ARF.shp'
    HUC8_ARF=gpd.read_file(infile)
    # find Max and min value
    MaxV=max(HUC8_ARF.iloc[:,5:].max())
    MinV=min(HUC8_ARF.iloc[:,5:].min())
    # create figure with array of axes
    fig, axs = plt.subplots(4, 3)
    fig.set_size_inches(15, 18)  #set it big enough for all subplots
    for i , area in enumerate(AreaAr):
        for j, RP in enumerate(RP_Ar):
            col=RP+'_'+str(area)+'sqMile'
            if (i==2) & (j==2):
                ax=HUC8_ARF.plot(ax=axs[i][j],column=col[0:10],cmap='Spectral', legend=True, vmin=MinV, vmax=MaxV)
            else:
                HUC8_ARF.plot(ax=axs[i][j],column=col[0:10],cmap='Spectral' , legend=True, vmin=MinV, vmax=MaxV)
            gdbstate.boundary.plot(ax=axs[i][j],edgecolor='black')
            axs[i][j].set_xticks([])
            axs[i][j].set_yticks([])
            
            if (i==0):
                axs[i][j].set_title(title[j], fontweight='bold', fontsize=20)
            if (j==0):
                axs[i][j].set_ylabel(y_label[i], rotation=0,fontweight='bold', fontsize=20)
                axs[i][j].yaxis.labelpad = 60

    # plt.show()
    img="P:/2021/ArizonaStorm/Regionality/Map/ARF_Compar_dur"+dur+'.jpg'
    plt.savefig(img, bbox_inches='tight')
    plt.close()   

    
    