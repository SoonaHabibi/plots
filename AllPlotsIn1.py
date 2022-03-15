# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 07:16:23 2022

Comparison plot for zone 0-40

@author: sardekani
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import geopandas as gpd
import pandas as pd
import numpy as np
from datetime import datetime
import contextily as ctx
import scipy as sp
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable 


def nse(predictions, targets):
    return (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))

direc='P:/2022/LCRA/NWM_SM/0_40layer/'
shp='P:/2022/LCRA/GIS/shp/NewZonesUpdated.shp'
gdb= gpd.read_file(shp) 
gdb = gdb.to_crs(epsg=3857)  

OnlyID_Ar=list(gdb.ProjID.str.slice(2,))
id_no_Ar=list(gdb.ProjID)
id_no_Ar=[x[2:] for x in id_no_Ar]
"""
*****NOTE******
Only data until the end of 2018 have been compared since basin avg values for NWS 2.0 aren't correct/available
"""
d1=datetime(1993,3,1)
d2=datetime(2019,1,1)
date_range=pd.date_range(start=d1,end=d2,freq='1M')
MonthAr=['%02d' % x.month for x in date_range]
YrAr=[str(x.year) for x in date_range]
YrStr=[str(y) for y in list(range(1993,2019))]

monStrAr=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Load All data and create conitues time series
# del(dfAll1, dfAll2)
for j in range(len(YrAr)):
    infile1=direc+'NWM2_0/'+YrAr[j]+'_'+MonthAr[j]+'.csv'
    df1=pd.read_csv(infile1, parse_dates=[0], index_col=0)
    try:
        dfAll1=pd.concat([dfAll1,df1], axis=0)
    except:
        dfAll1=df1
        
    #Load Basin average based on NWS 2.1
    infile2=direc+'NWM2_1/'+YrAr[j]+'_'+MonthAr[j]+'.csv'
    df2=pd.read_csv(infile2, parse_dates=[0], index_col=0)
    try:
        dfAll2=pd.concat([dfAll2,df2], axis=0)
    except:
        dfAll2=df2

#join the nws2.0 and NWS2.1
dfAll_j=pd.merge(dfAll1,dfAll2, left_index=True, right_index=True) 

dfAll1['source']='NWS2.0'    
dfAll2['source']='NWS2.1'
dfAll_c=pd.concat([dfAll1,dfAll2],axis=0)  
dfAll_c['Month']=dfAll_c.index.strftime('%B')
dfAll_c['Month']=dfAll_c['Month'].str.slice(0,3)
# set categorical order
dfAll_c['Month'] = pd.Categorical(dfAll_c['Month'],
                               categories=monStrAr,
                               ordered=True)

dfAll_c['year']=dfAll_c.index.year
#get the maximum and minimum for each year
df_max=dfAll_c.groupby(['year']).max()
df_min=dfAll_c.groupby(['year']).min()

#Get MaxAll and MinAll
maxS=max(dfAll_c.iloc[:,:-3].max())+0.1
minS=max(min(dfAll_c.iloc[:,:-3].min())-0.1, 0)
    
for i in id_no_Ar:
    col1=i+'_x'
    col2=i+'_y'
       
    # Plot figure with subplots of different sizes
    fig = plt.figure(1,figsize= (15,22))
    plt.rc('font', size=15) 
    # set up subplot grid
    gridspec.GridSpec(4,2)

    # small subplot1
    ax1=plt.subplot2grid((4,2), (0,0), colspan=1, rowspan=1)
    ax1.axes.yaxis.set_visible(False)
    ax1.axes.xaxis.set_visible(False)    
    ax1.annotate("Zone: "+i, xy=(-10920000, 3795000),fontsize=16, fontweight='bold')#, backgroundcolor = "white", alpha = 0.8)
    gdb.plot(facecolor='lightgray', edgecolor="black", ax=ax1, vmin=5, vmax=95, alpha=1)
    gdb[gdb['ProjID']=='SW'+i].plot(facecolor='salmon', edgecolor="black", ax=ax1, vmin=5, vmax=95, alpha=1)
    ctx.add_basemap(ax1)

    # small subplot 1
    ax2=plt.subplot2grid((4,2), (0,1))
    # get the correlation and p-value of regression line
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(dfAll_j[col1],dfAll_j[col2])
    # NSE
    NSE= nse(dfAll_j[col2], dfAll_j[col1])

    # Get the min and max values for x and y limit value
    # maxS=max(dfAll_j[col1].max(),dfAll_j[col2].max())+0.1
    # minS=max(min(dfAll_j[col1].min(),dfAll_j[col2].min())-0.1, 0)
    ax2.text(0.05, 0.9, 'NSE={:.2f}'.format(NSE),transform=ax2.transAxes, fontweight='bold')
    ax2.text(0.05, 0.8, 'SE={:.4f}'.format(std_err),transform=ax2.transAxes, fontweight='bold')
    ax2.text(0.05, 0.7, 'r={:.2f}'.format(r_value),transform=ax2.transAxes, fontweight='bold')
    ax2.set_xlim([minS, maxS])
    ax2.set_ylim([minS, maxS])
    ax2.plot([0,maxS],[0,maxS], color='r')
    sns.scatterplot(data=dfAll_j,x=col1,y=col2, s=8)
    ax2.set_xlabel('NWS 2.0')
    ax2.set_ylabel('NWS 2.1')
    ax2.set_title("Soil Moisture 0-40-inch layer (%)")
    
    # large subplot 1 (wettest year timeseries)
    wetyr=df_max[[i]].idxmax().values[0]
    dfAll_Wet=dfAll_c[dfAll_c['year']==wetyr]
    dfAll_Wet['Date']=dfAll_Wet.index
    ax3=plt.subplot2grid((4,2), (1,0), colspan=2, rowspan=1)
    sns.scatterplot(x='Date', y=i,data=dfAll_Wet, hue='source', ax=ax3)
    ax3.set_ylim([minS, maxS])
    ax3.set_title('Year: '+str(wetyr))
    ax3.set_ylabel("Soil Moisture 0-40-inch layer (%)")
    ax3.legend(loc='upper right')

    
    # large subplot 2 (driest year timeseries)
    dryyr=df_min[[i]].idxmin().values[0]
    dfAll_dry=dfAll_c[dfAll_c['year']==dryyr]
    dfAll_dry['Date']=dfAll_dry.index
    ax4=plt.subplot2grid((4,2), (2,0), colspan=2, rowspan=1)
    sns.scatterplot(x='Date', y=i,data=dfAll_dry, hue='source', ax=ax4)
    ax4.set_ylim([minS, maxS])
    # ax4.set_xlim([dfAll_dry['Date'].min(),dfAll_dry['Date'].max()])
    ax4.set_title('Year: '+str(dryyr))
    ax4.set_ylabel("Soil Moisture 0-40-inch layer (%)")
    ax4.legend(loc=(0.85,0.82))
    
    
    # small subplot 3
    ax5=plt.subplot2grid((4,2), (3,0))
    sns.distplot(dfAll1[i], label='NWS2.0')
    sns.distplot(dfAll2[i],label='NWS2.1')
    # ax5.xticks (rotation= 90)
    ax5.set_xlabel('Soil Moisture 0-40-inch layer (%)')
    ax5.set_ylabel('Count')
    ax5.legend(loc='upper right')  #
    ax5.set_xlim([minS, maxS])
    
    # small subplot 3
    ax6=plt.subplot2grid((4,2), (3,1))
    sns.boxplot(x='Month', y=i, hue='source', data=dfAll_c)
    ax6.set_ylabel('Soil Moisture 0-40-inch layer (%)')
    ax6.set_ylim([minS, maxS])
    plt.xticks (rotation= 45)
    ax6.legend(loc='best')
    

    # set the spacing between subplots
    plt.subplots_adjust(wspace=0.4, 
                        hspace=0.4)
    
    # fit subplots and save fig
    fig.tight_layout()
    # fig.set_size_inches(w=11,h=7)
    fig_name = 'P:/2022/LCRA/NWM_SM/BasinAvg3/SoilComparison/AllPlotin1/'+i+'_v2.jpg'
    fig.savefig(fig_name)    
        
    