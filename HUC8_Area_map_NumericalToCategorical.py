# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 13:48:17 2022

@author: sardekani
"""

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib import colors
import matplotlib.patches as mpatches


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
HUC8_df['AreaSqMile']=HUC8_df['AreaSqKm']*conv
HUC8_df['AreaFlag']= pd.cut(HUC8_df['AreaSqMile'], bins=[ 0,100, 300, 1000, 3000, float('Inf')], labels=['<100', '<300', '<1000','<3000','>3000'])



cmap=colors.ListedColormap(['red', 'red', 'peachpuff','darkseagreen','powderblue'])

fig, ax = plt.subplots(1, 1, figsize=(12, 15))
ax=HUC8_df.plot(column='AreaFlag',edgecolor='grey',cmap=cmap, legend=True)
gdbstate.boundary.plot(ax=ax,edgecolor='black', alpha=0.7)
# Add legend
p1 = mpatches.Patch(facecolor='red', edgecolor='grey', label='100-300')
p2 = mpatches.Patch(facecolor='peachpuff', edgecolor='grey', label='300-1000')
p3 = mpatches.Patch(facecolor='darkseagreen', edgecolor='grey', label='1000-3000')
p4 = mpatches.Patch(facecolor='powderblue', edgecolor='grey', label='>3000')

plt.legend(loc='upper left', title='$\\bf{Area (mile^2)}$',bbox_to_anchor=(1, 1), handles=[p1,p2,p3,p4], title_fontsize=12,fontsize=12)
outfile="P:/2021/ArizonaStorm/Regionality/Map/HUC08Area.jpg"
plt.savefig(outfile, bbox_inches='tight', dpi=300)