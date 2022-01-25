
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:09:17 2021

This Code generate homoginity map for each duration

@author: sardekani
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import os

Flag=0     # 0 means based on HUC12, 1: based on grid data
origin=['huc12','grid']
direc1="P:/2021/ArizonaStorm/Regionality/lmoment/huc12/"
shp1="P:/2021/ArizonaStorm/GIS/shp/ArizonaBoundary.shp"
shp2="P:/2021/ArizonaStorm/GIS/shp/HUC8All.shp"
shp3="P:/2021/ArizonaStorm/GIS/shp/HUC8_overlabArizona.shp"

gdbstate=gpd.read_file(shp1)
if not os.path.exists(shp3): 
    gdbstate=gpd.read_file(shp1)
    gdbHuc8=gpd.read_file(shp2)
    HUC8_inte=gpd.clip(gdbHuc8,gdbstate,keep_geom_type=True)
    HUC8_overlab=gdbHuc8[gdbHuc8['HUC8'].isin(list(HUC8_inte.HUC8))]
    HUC8_overlab.to_file(shp3)
else: 
    HUC8_overlab=gpd.read_file(shp3)
    
    
durationAr= ['1h', '2h', '3h', '6h', '12h', '18h', '1d', '2d', '3d','5d','7d']
irow=[0,0,0,1,1,1,2,2,2,3,3,3]
icol=[0,1,2,0,1,2,0,1,2,0,1,2]

for i in durationAr:
    infile=direc1+i+"/"+i+"_heteroginity.csv"
    df=pd.read_csv(infile).iloc[:,0:2]
    col='H1_'+i
    df.columns=['HUC8',col]
    df['HUC8']=df['HUC8'].apply(str)
    HUC8_overlab=HUC8_overlab.merge(df, on='HUC8')

# Save the gdb into a new shape file
shp4="P:/2021/ArizonaStorm/GIS/shp/HUC8_jeteroginity.shp"
HUC8_overlab.to_file(shp4)

# create figure with array of axes
fig, axs = plt.subplots(4, 3)
fig.set_size_inches(12, 18)  #set it big enough for all subplots
cmap=colors.ListedColormap(['lightskyblue', 'limegreen', 'tomato'])

for i in range(11):
    print(icol[i], irow[i])
    col='H1_'+durationAr[i]
    col2=durationAr[i]
    # HUC8_overlab[col2]='1. H<=1'
    # HUC8_overlab.loc[HUC8_overlab[col]>1,col2]='2. 1<H<=2'
    # HUC8_overlab.loc[HUC8_overlab[col]>2,col2]='3. H>2'
    HUC8_overlab[col2]='1. Homogeneous'
    HUC8_overlab.loc[HUC8_overlab[col]>1,col2]='2. Likely Heterogeneous'
    HUC8_overlab.loc[HUC8_overlab[col]>2,col2]='3. Heterogeneous'
    if ((icol[i]==1)&(irow[i]==3)):
        HUC8_overlab.plot(ax=axs[irow[i]][icol[i]], column=col2,edgecolor='grey',cmap=cmap,legend=True,legend_kwds={'loc': 'center left', 'bbox_to_anchor':(1.2,0.5),'fontsize': 14})
    else:
        HUC8_overlab.plot(ax=axs[irow[i]][icol[i]], column=col2,edgecolor='grey',cmap=cmap)
    gdbstate.boundary.plot(ax=axs[irow[i]][icol[i]],edgecolor='black')
    axs[irow[i]][icol[i]].set_axis_off()
    axs[irow[i]][icol[i]].set_title(durationAr[i],fontsize=14)

# Remove the last plot
fig.delaxes(axs[3,2])
img="P:/2021/ArizonaStorm/Regionality/lmoment/huc12/HeteroginityMap2.jpg"
plt.savefig(img, dpi=200)
