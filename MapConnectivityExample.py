# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 06:13:46 2022

@author: sardekani
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

linkdir="P:/2021/ArizonaStorm/BasinAvg/AORC/Conectivity/link/"
basindir="P:/2021/ArizonaStorm/BasinAvg/AORC/CSV_BasinAvg/"
Shapefile="P:/2021/ArizonaStorm/GIS/shp/SelectedHUC12_IntersAORC_EPSG4269_CorrArea.shp"
gdb=gpd.read_file(Shapefile)

#Select all HUC12s inside HUC08=15060105
gdb_HUC8=gdb[gdb.HUC12.str.slice(0,8)=='15060105']

TestIdAr=['150601050203','150601050206','150601050305','150601050403']

# subplot axis row and columns
irow=[0,0,1,1]
icol=[0,1,0,1,]
# Subplots name
n=['(a)','(b)','(c)','(d)']
# create figure with array of axes
fig, axs = plt.subplots(2, 2)
fig.set_size_inches(13.3, 16.3)  #set it big enough for all subplots
for i in range(len(TestIdAr)):
    TestID=TestIdAr[i]
    gdb_huc12=gdb[gdb.HUC12==TestID]
    file=linkdir+TestID+'SubW.csv'
    df=pd.read_csv(file)
    df['HUC12'] = df['HUC12'].astype(str)
    gdbAgg=gdb[gdb.HUC12.isin(df.HUC12)]

    gdbAgg.plot(ax=axs[irow[i]][icol[i]],color='skyblue')
    gdb_huc12.plot(ax=axs[irow[i]][icol[i]],hatch='\\\\\\\\',color='skyblue')
    gdb_HUC8.plot(ax=axs[irow[i]][icol[i]],facecolor="none", edgecolor="Black" )
    # tit='Connected HUC12s Upstream of '+TestID
    # axs[irow[i]][icol[i]].set_title(tit)
    # Add legend
    l='HUC '+TestID
    patch1 = mpatches.Patch(facecolor='skyblue', edgecolor='black',hatch='\\\\\\\\', label=l)
    patch2 = mpatches.Patch(facecolor='skyblue', edgecolor='black', label='Connected HUC12s')
    axs[irow[i]][icol[i]].legend(loc='lower right',handles=[patch1,patch2], fontsize=14)
    # Add text to maps
    axs[irow[i]][icol[i]].text(-111.48,34.37,n[i],fontsize=17,fontweight='bold')
    
img='P:/2021/ArizonaStorm/GIS/Map_Figure/Connectivity.jpg'
plt.savefig(img, dpi=200)

