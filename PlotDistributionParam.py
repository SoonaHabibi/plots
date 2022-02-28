# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 06:03:29 2022

@author: sardekani
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.linear_model import LinearRegression
import seaborn as sns
import scipy as sp

# flag=0 area in km^2 is interested if flag=1 area in mile^2 is interested
flag=1

durationAr=['1h', '2h', '3h', '6h', '12h', '18h', '1d', '2d', '3d','5d','7d']
RP=[2,5,10,25,50,100,200,500,1000]
distAr=['gev','glo','gno','gpa','pe3']
dist=distAr[0]

if flag==1:
    xlabel='Watershed Area ($mile^2$)'
    c=0.3861
    pname='_mile'
    col_A='AreaSqMile'
elif flag==0:
    xlabel='Watershed Area ($Km^2$)'
    c=1
    pname=''
    col_A='AreaSqKm'
#Load HUC08 file
# HUC8_df=pd.read_csv("P:/2021/ArizonaStorm/BasinAvg/HUC12/ListHUC8.csv")
shp='P:/2021/ArizonaStorm/GIS/shp/HUC8_ClipHUC6Arizona_HUC12Summary.shp'
HUC8_df=gpd.read_file(shp)[['HUC8','AreaSqKm']]
HUC8_df.columns=['HUC08','AreaSqKm']


# distribution parameter directory for HUC12 and interconnected HUC12
indir='P:/2021/ArizonaStorm/Regionality/lmoment/'

# load area table for interconnected huc12 and huc12s
indir1='P:/2021/ArizonaStorm/BasinAvg/AORC/'
filename1=indir1+'InterHUC12_IntersAORC_EPSG4269_CorrArea.csv'
inthuc12_area=pd.read_csv(filename1)
inthuc12_area=inthuc12_area[['HUC12', 'SumUpAreaSqKm']]
# change the column name to be consistent with huc12 area table
inthuc12_area.columns=['huc12', 'AreaSqKm']
filename2=indir1+'SelectedHUC12_IntersAORC_EPSG4269_CorrArea.csv'
huc12_area=pd.read_csv(filename2)[['HUC12', 'AreaSqKm']]
huc12_area.columns=['huc12', 'AreaSqKm']

for dur in durationAr:
    # Load distribution parameters
    file_p_inthuc12=indir+'interHUC12BasedOnBasinAvgAMP/'+dur+'_allHUC12s_'+dist+'_param.csv'
    file_p_huc12=indir+'HUC12BasedOnBasinAvgAMP/'+dur+'_allHUC12s_'+dist+'_param.csv'
    para_inthuc12=pd.read_csv(file_p_inthuc12)
    para_huc12=pd.read_csv(file_p_huc12)
    para_inthuc12['watershed']='interconnected huc12'
    para_huc12['watershed']='huc12'
    # merge area
    para_inthuc12=pd.merge(para_inthuc12, inthuc12_area, on='huc12')
    para_huc12=pd.merge(para_huc12, huc12_area, on='huc12')
    
    R_dic={'R_Xi':[],'R_alpha':[],'R_k':[]}
    for row in range(len(HUC8_df)):
        huc8=HUC8_df.HUC08.iloc[row]
        area_huc8=HUC8_df.AreaSqKm.iloc[row]
        infile="P:/2021/ArizonaStorm/BasinAvg/HUC12/HUC12in"+str(huc8)+".csv"
        huc12_l=pd.read_csv(infile)
        huc12_l.columns=['huc12','huc8']
        # Select huc 12 inside huc8
        sel_p_huc12=pd.merge(huc12_l, para_huc12, on='huc12')
        sel_p_interhuc12=pd.merge(huc12_l, para_inthuc12, on='huc12')
        print(len(sel_p_huc12),len(sel_p_interhuc12))
        # join huc12 and interconnected huc12
        all_watershed=pd.concat([sel_p_huc12,sel_p_interhuc12], axis=0)
        all_watershed['AreaSqMile']=all_watershed['AreaSqKm']*c
        # Generate Distribution parameter scatter plot for all units (3x1)
        plt.style.use('ggplot')
        plt.rc('font', size=17) 
        fig, axes=plt.subplots(1,3)
        fig.set_figheight(5)
        fig.set_figwidth(16)
        fig.tight_layout()         
        
        r, p = sp.stats.pearsonr(all_watershed[col_A],all_watershed['xi'])
        R_dic['R_Xi'].append(r)
        ax1=sns.regplot(x=col_A, y='xi', data=all_watershed, ax=axes[0], color='royalblue')
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(chr(958))
        yl=(all_watershed['xi'].max()-all_watershed['xi'].min())*0.8+all_watershed['xi'].min()
        xl=(all_watershed[col_A].max()-all_watershed[col_A].min())*0.8+all_watershed[col_A].min()
        ax1.text(xl, yl, 'r={:.2f}'.format(r))  #,transform=ax1.transAxes
        
        r1, p1 = sp.stats.pearsonr(all_watershed[col_A],all_watershed['alpha'])
        R_dic['R_alpha'].append(r1)
        ax2=sns.regplot(x=col_A, y='alpha', data=all_watershed, ax=axes[1], color='royalblue')
        ax2.set_xlabel(xlabel)
        ax2.set_ylabel(chr(945))
        yl=(all_watershed['alpha'].max()-all_watershed['alpha'].min())*0.8+all_watershed['alpha'].min()
        xl=(all_watershed[col_A].max()-all_watershed[col_A].min())*0.8+all_watershed[col_A].min()
        ax2.text(xl, yl, 'r={:.2f}'.format(r1))
        
        r2, p2 = sp.stats.pearsonr(all_watershed[col_A],all_watershed['k'])
        R_dic['R_k'].append(r2)
        ax3=sns.regplot(x=col_A, y='k', data=all_watershed, ax=axes[2], color='royalblue')
        ax3.set_xlabel(xlabel)
        ax3.set_ylabel(chr(954))
        yl=(all_watershed['k'].max()-all_watershed['k'].min())*0.8+all_watershed['k'].min()
        xl=(all_watershed[col_A].max()-all_watershed[col_A].min())*0.8+all_watershed[col_A].min()
        ax3.text(xl, yl, 'r={:.2f}'.format(r2))
        
        plt.subplots_adjust(hspace=0.45,wspace=0.3)
        
        img=indir+'Plots/'+dist+'_DistParameters/'+dur+'_HUC08_'+str(huc8)+pname+'_1by3.jpg'
        plt.savefig(img, bbox_inches='tight')
        plt.close()    
        
        outfile=indir+'Plots/'+dist+'_DistParameters/Rsummary_'+dur+'_AllHUC08.csv'
        df_out=pd.DataFrame(R_dic)
        df_out.to_csv(outfile, index=False)
        
        df_dummy=df_out
        df_dummy[df_out<0]=-1
        df_dummy[df_out==0]=0
        df_dummy[df_out>0]=1
        
        df_summ=df_dummy.value_counts()
        df_summ.columns='count'
        outfile2=indir+'Plots/'+dist+'_DistParameters/Rsummary_valueCounts_'+dur+'_AllHUC08.csv'
        df_summ.to_csv(outfile2)
        print(dur, df_summ)
        
        # # generate Distribution parameter scatter plot for all units, only HUC12s and only aggregated HUC12 (3x1) 
        # fig=plt.figure(9)
        # fig.set_figheight(14)
        # fig.set_figwidth(16)
        # fig.tight_layout() 
        
        # title='HUC08: '+str(huc8)+ ' ('+str(area_huc8)+'$Km^2$) - Duration: '+dur
        # fig.suptitle(title, fontsize=18)
        
        # ax1 = plt.subplot(3,3,1)
        # ax1.scatter(all_watershed.AreaSqKm*c, all_watershed.xi,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(958),fontweight = 'bold')
        
        # ax2 = plt.subplot(3,3,2)
        # ax2.scatter(all_watershed.AreaSqKm*c, all_watershed.alpha,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(945),fontweight = 'bold')
        # plt.title('HUC12 and interconnected HUC12',fontweight = 'bold', fontsize=20)
        
        # ax3 = plt.subplot(3,3,3)
        # ax3.scatter(all_watershed.AreaSqKm*c, all_watershed.k,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(954),fontweight = 'bold')

        # ax4 = plt.subplot(3,3,4)
        # ax4.scatter(sel_p_huc12.AreaSqKm, sel_p_huc12.xi,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(958),fontweight = 'bold')
        
        # ax5 = plt.subplot(3,3,5)
        # ax5.scatter(sel_p_huc12.AreaSqKm, sel_p_huc12.alpha,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(945),fontweight = 'bold')
        # plt.title('only HUC12',fontweight = 'bold', fontsize=20)
        
        # ax6 = plt.subplot(3,3,6)
        # ax6.scatter(sel_p_huc12.AreaSqKm, sel_p_huc12.k,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(954),fontweight = 'bold')
        
        # ax7 = plt.subplot(3,3,7)
        # ax7.scatter(sel_p_interhuc12.AreaSqKm, sel_p_interhuc12.xi,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(958),fontweight = 'bold')
        
        # ax8 = plt.subplot(3,3,8)
        # ax8.scatter(sel_p_interhuc12.AreaSqKm, sel_p_interhuc12.alpha,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(945),fontweight = 'bold')
        # plt.title('only interconnected HUC12',fontweight = 'bold', fontsize=20)
        
        # ax9 = plt.subplot(3,3,9)
        # ax9.scatter(sel_p_interhuc12.AreaSqKm, sel_p_interhuc12.k,marker='+')
        # plt.xlabel(xlabel,fontweight = 'bold')
        # plt.ylabel(chr(954),fontweight = 'bold')

        # plt.subplots_adjust(hspace=0.45,wspace=0.45)

        # img=indir+'Plots/'+dist+'_DistParameters/'+dur+'_HUC08_'+str(huc8)+pname+'.jpg'
        # plt.savefig(img)
        # plt.close()    