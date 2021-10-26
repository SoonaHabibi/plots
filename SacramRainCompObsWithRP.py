# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 13:38:23 2021
Objective of the scprit:
    Compare rain gauge observation at four different location with 4 different frequency curves for\
    Sacrament rainfall on Oct 24th 2021.
The code:
    1. Convert Gauge dataframe to a shapefile
    2. Read raster files and extract the value of pixels where the gauges are in
    3. Generate a figure with 4 subplots (2x2)
        

@author: sardekani
"""

import pandas as pd
from osgeo import gdal
import geopandas 
import matplotlib.pyplot as plt   

direc='F:/SacramentoRain20211024/'
in_csv=direc+'gauge1.csv'

RP=[2,5,10,25,50,100,200,500]
Duration='1day'

Reference=['SacManual','Updated','UpdatedWithClimChange', 'NOAA14','Observation']

df=pd.read_csv(in_csv)
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Lon, df.Lat))
gdf.crs = 'epsg:4267'
gdf.to_file('F:/SacramentoRain20211024/gauge.shp')

R1={df['Location'][0]:[],df['Location'][1]:[],df['Location'][2]:[],df['Location'][3]:[],\
    df['Location'][4]:[],df['Location'][5]:[]}
R2={df['Location'][0]:[],df['Location'][1]:[],df['Location'][2]:[],df['Location'][3]:[],\
    df['Location'][4]:[],df['Location'][5]:[]}
R3={df['Location'][0]:[],df['Location'][1]:[],df['Location'][2]:[],df['Location'][3]:[],\
    df['Location'][4]:[],df['Location'][5]:[]}
R4={df['Location'][0]:[],df['Location'][1]:[],df['Location'][2]:[],df['Location'][3]:[],\
    df['Location'][4]:[],df['Location'][5]:[]}


for i in RP:
    p1=direc+Reference[0]+'/SacMan_1dayRP_'+str(i)+'.tiff'
    p2=direc+Reference[1]+'/Upd_1dayRP_'+str(i)+'.tiff'
    p3=direc+Reference[2]+'/Upd_1dayRP_'+str(i)+'_CC.tiff'
    p4=direc+Reference[3]+'/NA14_1dayRP_'+str(i)+'.asc'
    
    dataset1=gdal.Open(p1) 
    band1=dataset1.GetRasterBand(1)                
    rain1=band1.ReadAsArray()
    gt1=dataset1.GetGeoTransform()
    
    dataset2=gdal.Open(p2) 
    band2=dataset2.GetRasterBand(1)                
    rain2=band2.ReadAsArray()
    gt2=dataset2.GetGeoTransform()
    
    dataset3=gdal.Open(p3) 
    band3=dataset3.GetRasterBand(1)                
    rain3=band3.ReadAsArray()
    gt3=dataset3.GetGeoTransform()
    
    dataset4=gdal.Open(p4) 
    band4=dataset4.GetRasterBand(1)                
    rain4=band4.ReadAsArray()
    gt4=dataset4.GetGeoTransform()
    
    for j in range(len(df)):
        lat=df['Lat'].iloc[j]
        lon=df['Lon'].iloc[j]
        
        row1=int((lat-gt1[3])//gt1[5])
        col1=int((lon-gt1[0])//gt1[1])
        R1[df['Location'][j]].append(rain1[row1,col1])
        
        row2=int((lat-gt2[3])//gt2[5])
        col2=int((lon-gt2[0])//gt2[1])
        R2[df['Location'][j]].append(rain2[row2,col2])
        
        row3=int((lat-gt3[3])//gt3[5])
        col3=int((lon-gt3[0])//gt3[1])
        R3[df['Location'][j]].append(rain3[row3,col3])
        
        row4=int((lat-gt4[3])//gt4[5])
        col4=int((lon-gt4[0])//gt4[1])
        R4[df['Location'][j]].append(rain4[row4,col4]/1000)
        
fig=plt.figure(4)
fig.set_figheight(12)
fig.set_figwidth(12)

ax1 = plt.subplot(2,2,1)
ax1.plot(RP,R1['Folsom'],'-bo')
ax1.plot(RP,R2['Folsom'],'-go')
ax1.plot(RP,R3['Folsom'],'-mo')
ax1.plot(RP,R4['Folsom'],'-yo')
ax1.plot([0,1000],[df['precip(in)'][0],df['precip(in)'][0]],'r')
ax1.legend(Reference)
plt.xscale('log')
plt.title('Folsom',fontweight = 'bold')
ax2 = plt.subplot(2,2,2)
ax2.plot(RP,R1['Roseville3'],'-bo')
ax2.plot(RP,R2['Roseville3'],'-go')
ax2.plot(RP,R3['Roseville3'],'-mo')
ax2.plot(RP,R4['Roseville3'],'-yo')
ax2.plot([0,1000],[df['precip(in)'][3],df['precip(in)'][3]],'r')
plt.xscale('log')
plt.title('Roseville',fontweight = 'bold')
ax3 = plt.subplot(2,2,3)
ax3.plot(RP,R1['Sacramento'],'-bo')
ax3.plot(RP,R2['Sacramento'],'-go')
ax3.plot(RP,R3['Sacramento'],'-mo')
ax3.plot(RP,R4['Sacramento'],'-yo')
ax3.plot([0,1000],[df['precip(in)'][4],df['precip(in)'][4]],'r')
plt.xscale('log')
plt.title('Sacramento',fontweight = 'bold')
ax4 = plt.subplot(2,2,4)
ax4.plot(RP,R1['South Sacramento'],'-bo')
ax4.plot(RP,R2['South Sacramento'],'-go')
ax4.plot(RP,R3['South Sacramento'],'-mo')
ax4.plot(RP,R4['South Sacramento'],'-yo')
ax4.plot([0,1000],[df['precip(in)'][5],df['precip(in)'][5]],'r')
plt.xscale('log')
plt.title('South Sacramento',fontweight = 'bold')
fig.text(0.5, 0.04, 'Return Period', ha='center',fontweight = 'bold', fontsize=14)
fig.text(0.04, 0.5, 'Rain-24hr (inches)', va='center', rotation='vertical',fontweight = 'bold', fontsize=14)
# plt.show()
img=direc+'plot.jpg'
plt.savefig(img)
plt.close()    
    