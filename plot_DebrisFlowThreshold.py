# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 10:50:45 2020

@author: sardekani
"""
import pandas as pd
import numpy as np
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly
import sys 
sys.path.append("//westfolsom/Office/Python/WEST_Python_FunctionAug2019");
import BasicFunction_py3 as BF
import matplotlib.pyplot as plt
import math

indir = 'P:/2020/Meyers Nave/GIS/Raster/'
duration = [5, 10, 15, 30, 60]

RainRateAr = []
for i in range(len(duration)):
    TiffFile = indir + 'spas1721_' + str(duration[i]) +'min_mask_allWatershed.tif'
    dataset = gdal.Open(TiffFile, GA_ReadOnly) 
    rb = dataset.GetRasterBand(1)
    RainRate = rb.ReadAsArray()
    RainRate = RainRate.flatten()
    RainRate = RainRate[[RainRate>=0]]
    RainRate = RainRate *60/duration[i]  # convert tot rain to in/hr
    RainRateAr.append(RainRate)


DurationAr = np.repeat(duration, len(RainRateAr[0])) 
DurationAr = DurationAr/60    #min to hr
RainRateArFlat = np.concatenate( RainRateAr, axis=0 )
RainRateArFlat_mm_per_hr = RainRateArFlat * 25.4  #in to mm

x = np.arange(0.06, 1.2, 0.05)
y_upper = 11.6 *x**(-0.7)
y_lower = 6.5 *x**(-0.7)

fig=plt.figure(1)
fig.set_figheight(8)
fig.set_figwidth(12)
plt.loglog(DurationAr, RainRateArFlat_mm_per_hr, '+', label = 'GARR pixel rain rate over the Montecito sub-watersheds upstream from the inundated area'  )
plt.loglog(x,y_upper, '--', label = 'Debris-flow threshold: I = 11.6 D$^{-0.7}$')
plt.loglog(x,y_lower, '--',  label = 'Lower-bound threshold: I = 6.5 D$^{-0.7}$')
plt.xlim([10**-1*0.6,10**0*1.1])
#plt.ylim([10**-1*0.6,10**0*1.1])
plt.xlabel('Precipitation Duration (h)', fontweight = 'bold', fontsize=11)
plt.ylabel('Rain Rate (mm/h)', fontweight = 'bold', fontsize=11)

plt.text(duration[0]/60, 110, "5 min", ha='center')
plt.text(duration[1]/60, 110, "10 min", ha='center')
plt.text(duration[2]/60, 110, "15 min", ha='center')
plt.text(duration[3]/60, 110, "30 min", ha='center')
plt.text(duration[4]/60, 110, "60 min", ha='center')

plt.text(duration[0]/60, 109,"-", rotation=90, ha='center')
plt.text(duration[1]/60, 109,"-", rotation=90, ha='center')
plt.text(duration[2]/60, 109,"-", rotation=90, ha='center')
plt.text(duration[3]/60, 109,"-", rotation=90, ha='center')
plt.text(duration[4]/60, 109,"-", rotation=90, ha='center')

plt.text(1.2, 60,"(mm/h)", rotation=90, ha='center', fontweight = 'bold')
plt.text(1.1, 6,"- ")
plt.text(1.1, 7,"- ")
plt.text(1.1, 8,"- ")
plt.text(1.1, 9,"- ")
plt.text(1.1, 10,"- 10")
plt.text(1.1, 20,"- ")
plt.text(1.1, 30,"- ")
plt.text(1.1,40,"- ")
plt.text(1.1, 50,"- 50")
plt.text(1.1,60,"- ")
plt.text(1.1,70,"- ")
plt.text(1.1,80,"- ")
plt.text(1.1,90,"- ")
plt.text(1.1, 100,"- 100")

plt.legend(loc='lower left', fontsize=11)

#plt.show()
img_path = '‪P:/2020/Meyers Nave/GIS/Figure/DebrisThreshold_Keaton_mm_per_hr.jpg'
plt.savefig(img_path.strip('\u202a'))  





# Plot for rain rate in in/hr 
# the following code is not good
x = np.arange(0.06, 1.2, 0.05)
y_upper = 1.2 *x**(-0.7)     #Convert x unit to in
y_lower = 0.67 *x**(-0.7)


fig=plt.figure(1)
fig.set_figheight(8)
fig.set_figwidth(12)
plt.loglog(DurationAr, RainRateArFlat, '+', label = 'Calculated from GARR pixels in the Monetecito inundated watersheds'  )
plt.loglog(x,y_upper, '--', label = 'Debris-flow threshold: I = 111.65 D$^{-0.7}$')
plt.loglog(x,y_lower, '--',  label = 'Lower-bound threshold: I = 62.56 D$^{-0.7}$')
plt.xlim([10**-1*0.6,10**0*1.1])
#plt.ylim([10**-1*0.6,10**0*1.1])
plt.xlabel('Precipitation Duration (h)', fontweight = 'bold')
plt.ylabel('Rain Rate (in/h)', fontweight = 'bold')

plt.text(duration[0]/60, 110, "5 min", ha='center')
plt.text(duration[1]/60, 110, "10 min", ha='center')
plt.text(duration[2]/60, 110, "15 min", ha='center')
plt.text(duration[3]/60, 110, "30 min", ha='center')
plt.text(duration[4]/60, 110, "60 min", ha='center')

plt.text(duration[0]/60, 106,"-", rotation=90, ha='center')

plt.legend(loc='lower left')

#plt.show()
img_path = '‪P:/2020/Meyers Nave/GIS/Figure/DebrisThreshold_Keaton_in_per_hr.jpg'
plt.savefig(img_path.strip('\u202a'))  
