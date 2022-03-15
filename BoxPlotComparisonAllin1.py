import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from datetime import datetime
import seaborn as sns
import scipy as sp
from scipy.stats import sem
import os
import numpy as np

def nse(predictions, targets):
    return (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))

# Soil Layers path name
VarAr=['_SOIL_W1','_SOIL_W2','_SOIL_W3','_SOIL_W4', '0_40']
VarName=['0_4','4_16','16_40','40_80','0_40']

# load the shapefile includings all basins
Shapefile="P:/2020/LCRA/BasinDelineationLKC_Jan8/SubWatershedSHP/SWAllMergedDis_NWM.shp"
gdb=gpd.read_file(Shapefile)
OnlyID_Ar=list(gdb.ProjID.str.slice(2,))
id_no_Ar=list(gdb.ProjID)
id_no_Ar=[x[2:] for x in id_no_Ar]

outdir='P:/2022/LCRA/NWM_SM/BasinAvg3/SoilComparison/'
if not os.path.exists(outdir):os.mkdir(outdir)


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


for index, var in enumerate(VarAr):
   
    for i in range(len(YrAr)):
        if var!=VarAr[-1]:
            infile1='P:/2020/LCRA/Data/NWM_FixDate/'+var+YrAr[i]+'_'+MonthAr[i]+'.csv'
            infile2='P:/2022/LCRA/NWM_SM/BasinAvg3/'+var+YrAr[i]+'_'+MonthAr[i]+'.csv'
        else:
            infile1='P:/2022/LCRA/NWM_SM/0_40layer/NWM2_0/'+YrAr[i]+'_'+MonthAr[i]+'.csv'
            infile2='P:/2022/LCRA/NWM_SM/0_40layer/NWM2_1/'+YrAr[i]+'_'+MonthAr[i]+'.csv'
        
        #Load Basin average based on NWS 2.0
        df1=pd.read_csv(infile1, parse_dates=[0], index_col=0)
        try:
            dfAll1=pd.concat([dfAll1,df1], axis=0)
        except:
            dfAll1=df1
            
        #Load Basin average based on NWS 2.1
        df2=pd.read_csv(infile2, parse_dates=[0], index_col=0)
        try:
            dfAll2=pd.concat([dfAll2,df2], axis=0)
        except:
            dfAll2=df2
            
    df1melt=pd.melt(dfAll1)
    df1melt['value']=df1melt['value']*40
    df2melt=pd.melt(dfAll2)
    df2melt['value']=df2melt['value']*40
    df1melt['source']='NWS2.0'
    df2melt['source']='NWS2.1'
    df_join=pd.concat([df1melt,df2melt], axis=0)
    VarOrd=df_join['variable'].unique()
    VarOrd.sort()
    # set categorical order
    df_join['variable'] = pd.Categorical(df_join['variable'],
                                   categories=VarOrd,
                                   ordered=True)
    # sns.set(font_scale=2)
    sns.set_theme(style="whitegrid", font_scale=2.5)
    fig = plt.figure(1,figsize= (20,28))
    sns.boxplot(x='value', y='variable', data=df_join, hue='source',showfliers = False, width=0.5)
    xlabel='Soil Moisture '+VarName[index].replace('_','-')+'-inch layer (%)'
    plt.xlabel(xlabel)
    plt.ylabel('Zone')
    plt.xlim([2,22])
    plt.legend(loc='upper right')
    # fit subplots and save fig
    fig.tight_layout()
    # fig.set_size_inches(w=11,h=7)
    fig_name = 'P:/2022/LCRA/NWM_SM/BasinAvg3/SoilComparison/Boxplot_AllIn1/'+VarName[index]+'layer.jpg'
    fig.savefig(fig_name)  
    # plt.show()
    plt.close()
    del(dfAll1, dfAll2)
