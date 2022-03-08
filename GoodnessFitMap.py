# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 05:39:20 2022

Codes generate grids goodness of fit maps for different dstribution and duration
1. Read goodness of fit for each grid, create a matrix of z value
2. replace |z|<1.64 with zeros and |z|>1.64 with 1  (0 mean acceptable goodness of fit)
3. write the matrix into a tif file for each distribution and duration
4. Generate summary table of portion of grids with nonacceptable goodness of fit
5. Generate maps

@author: sardekani
"""

import pandas as pd
import os 
import numpy as np
from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import mpl_toolkits as mpl
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import geopandas as gpd
import sys
sys.path.append("C:/Users/SARDEKANI/Documents/GitHub/DARF/");
import BasicFunction_py3 as BF
import copy



# Read a sample AORC file
AORC='P:/2021/ArizonaStorm/Data/AORC/Tif/Tot1YrPr_1979MM_F.tif'
dataset=gdal.Open(AORC)
band=dataset.GetRasterBand(1)                
rain=band.ReadAsArray()
ncol=dataset.RasterXSize 
nrow=dataset.RasterYSize
proj=dataset.GetProjection()
gt=dataset.GetGeoTransform()

# Generate zero matrix of size nrow X Ncol
# directory contains goodness of fit
direc='P:/2021/ArizonaStorm/REgionality/lmoment/grid/'

# duration and distribution array
durationAr=['1h', '2h', '3h', '6h', '12h', '18h', '1d', '2d', '3d','5d','7d']
distAr=['glo','gev','gno', 'pe3', 'gpa']

# Create a matirx of 0 and 1 for each duration and distribution
# 1 represents grid with abs goodness of fit larger than 1.64

TotFail=[]
for dur in durationAr:
    # Generate zero matrix of size nrow X Ncol
    mat_glo=np.zeros((nrow,ncol))
    mat_gev=np.zeros((nrow,ncol))
    mat_gno=np.zeros((nrow,ncol))
    mat_pe3=np.zeros((nrow,ncol))
    mat_gpa=np.zeros((nrow,ncol))
    # Read goodness of fit
    infile=direc+dur+'_allGrids_GoodnessFit.csv'
    df=pd.read_csv(infile, index_col=0)
    df[(df<1.64)&(df>-1.64)]=0
    df[df!=0]=1
    # Convert index to column
    df.reset_index(inplace=True)
    # to split into multiple columns by delimiter
    df[['col','row']]=df['this.sta'].str.split('_', expand=True)
    df['row']=df['row'].apply(lambda x: int(x[3:]))
    df['col']=df['col'].apply(lambda x: int(x[3:]))
    for i in range(len(df)):
        col=df.col.iloc[i]
        row=df.row.iloc[i]
        mat_glo[row,col]=df.glo.iloc[i]
        mat_gev[row,col]=df.gev.iloc[i]
        mat_gno[row,col]=df.gno.iloc[i]
        mat_pe3[row,col]=df.pe3.iloc[i]
        mat_gpa[row,col]=df.gpa.iloc[i]
        
    
    # write matrix into a tif file for visualization
    for dist in distAr:
        TotFail.append(sum(globals()['mat_%s' % dist].flatten()))
        # FileName=direc+dur+'_'+dist+'_goodnessfit_matrix.tif'
        # BF.CreateMatrixFileFloat(FileName,globals()['mat_%s' % dist], ncol, nrow, gt, proj)
        
TotFailAr=np.array(TotFail).reshape(11,5)
PorFailAr=TotFailAr/len(globals()['mat_%s' % dist].flatten())
#portion of grids with nonacceptable goodness of fit
df_gf_summ=pd.DataFrame(PorFailAr, columns=distAr, index=durationAr)
outcsv="P:/2021/ArizonaStorm/Regionality/goodnessFitSummary.csv"
df_gf_summ.to_csv(outcsv)


# Generate Map 
irow=[0,0,1,1,2,2]
icol=[0,1,0,1,0,1]
irow=[0,0,0,1,1,1]
icol=[0,1,2,0,1,2]
textAr=['(a)','(b)','(c)','(d)','(e)']
textAr=['GLO','GEV','GNO', 'PE3', 'GPA']
BB=[30,39,-115,-107]
StateShp='P:/2021/ArizonaStorm/GIS/shp/ArizonaBoundary'
Huc8Shp='P:/2021/ArizonaStorm/GIS/shp/HUC8_ClipHUC6Arizona_HUC12Summary'
for dur in durationAr:
    # create figure with array of axes
    fig, axs = plt.subplots(2, 3)
    fig.set_size_inches(18, 11)  #set it big enough for all subplots
    # cmap=colors.ListedColormap(['lightskyblue', 'limegreen', 'tomato'])

    for i, dist in enumerate(distAr):
        TifFile=direc+dur+'_'+dist+'_goodnessfit_matrix.tif'
        gdata = gdal.Open(TifFile)
        geo = gdata.GetGeoTransform()
        data = gdata.ReadAsArray()
        
        xres = geo[1]
        yres = geo[5]
        xmin = geo[0] + xres * 0.5
        xmax = geo[0] + (xres * gdata.RasterXSize) - xres * 0.5
        ymin = geo[3] + (yres * gdata.RasterYSize) + yres * 0.5
        ymax = geo[3] - yres * 0.5
        
        # A good LCC projection for USA plots
        m = Basemap(ax=axs[irow[i]][icol[i]],llcrnrlon=BB[2]-2,llcrnrlat=BB[0]-2,urcrnrlon=BB[3]+2,urcrnrlat=BB[1]+2,
                    projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
        
        # This just plots the shapefile -- it has already been clipped
        m.readshapefile(StateShp,'STATE_NAME',drawbounds=True, color='blue',linewidth=1.5)
        m.readshapefile(Huc8Shp,'HUC8',drawbounds=True, color='darkgray',linewidth=1.5)
        
        x,y = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
        x,y = m(x,y)
        
        # cmap = plt.get_cmap('rainbow')
        cmap = copy.copy(plt.cm.get_cmap("rainbow"))
        cmap.set_under('white')
        
        eps = np.spacing(0.0)
        m.pcolormesh( x,y, data.T, cmap=cmap, vmin=eps)
        
        # Place text to upper left corner
        axs[irow[i]][icol[i]].annotate(textAr[i], xy=(0.1, 0.9), xycoords='axes fraction',fontsize=18, fontweight='bold')
        
        # Title
        title='distribution: '+dist+' - duration: '+dur+' - Goodness of fit'
        # axs[irow[i]][icol[i]].set_title(title)
    
    # Add legend
    State_patch = mpatches.Patch(facecolor='white', edgecolor='blue', label='Arizona Boundary')
    HUC8_patch= mpatches.Patch(facecolor='white', edgecolor='darkgray', label='HUC08')
    axs[irow[i]][icol[i]].legend(loc='upper center', bbox_to_anchor=(1.45, 1), handles=[State_patch,HUC8_patch], fontsize=18)

    fig.delaxes(axs[1,2])
    # plt.show()
    img="P:/2021/ArizonaStorm/Regionality/Map/GoodnessofFit_"+dur+"_memo.jpg"
    plt.savefig(img,bbox_inches='tight', dpi=200)

            