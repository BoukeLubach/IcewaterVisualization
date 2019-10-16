import pandas as pd
import datetime
from openpyxl import Workbook
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rc('font',family='Palatino Linotype')
matplotlib.rc('font',size = 14)
CPwater = 4.185     #kJ/kgK

WESdark = '#193333'
WESorange = '#ff5900'


Chillerdata = pd.read_csv("Chillerdata.csv", sep=';', parse_dates=[0], dayfirst=True, low_memory=False, dtype='float64')
                        
Chillerdata.reset_index(inplace=True)
Chillerdata.set_index(pd.DatetimeIndex(Chillerdata['Datum']), inplace=True)
Chillerdata.fillna(0)


#Filter koelcapaciteit (tussen -200 en +1000 kW)
Chillerdata['Chiller1 - COP'] = Chillerdata['Chiller 1 - koelvermogen']/Chillerdata['Chiller 1 - Elektriciteit']
Chillerdata['Chiller3 - COP'] = Chillerdata['Chiller 3 - koelvermogen']/Chillerdata['Chiller 3 - Elektriciteit']
Chillerdata['Chiller4 - COP'] = Chillerdata['Chiller 4 - koelvermogen']/Chillerdata['Chiller 4 - Elektriciteit']

##Filter unreasonable COP's 
Chillerdata['Chiller1 - COP'] = Chillerdata['Chiller1 - COP'].mask(lambda x: x < -4)
Chillerdata['Chiller1 - COP'] = Chillerdata['Chiller1 - COP'].mask(lambda x: x > 20)
Chillerdata['Chiller3 - COP'] = Chillerdata['Chiller3 - COP'].mask(lambda x: x < -4)
Chillerdata['Chiller3 - COP'] = Chillerdata['Chiller3 - COP'].mask(lambda x: x > 20)
Chillerdata['Chiller4 - COP'] = Chillerdata['Chiller4 - COP'].mask(lambda x: x < -4)
Chillerdata['Chiller4 - COP'] = Chillerdata['Chiller4 - COP'].mask(lambda x: x > 20)

#Middel over uur, dag en week
Chillerdata_hour = Chillerdata.resample('H', label='left', convention='start').mean()
Chillerdata_day = Chillerdata.resample('D', label='left', convention='start').mean()
Chillerdata_week = Chillerdata.resample('w', label='left', convention='start').mean()

def plotHistogramKoelvraag(timeinterval, bins):
    df = pd.DataFrame()
    df['Chiller 1 - koeling'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller 3 - koeling'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller 4 - koeling'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()
    
    df['Chiller 1 - koeling'] = df['Chiller 1 - koeling'].mask(lambda x: x < 0)
    df['Chiller 1 - koeling'] = df['Chiller 1 - koeling'].mask(lambda x: x > 700)
    df['Chiller 3 - koeling'] = df['Chiller 3 - koeling'].mask(lambda x: x < 0)
    df['Chiller 3 - koeling'] = df['Chiller 3 - koeling'].mask(lambda x: x > 700)
    df['Chiller 4 - koeling'] = df['Chiller 4 - koeling'].mask(lambda x: x < 0)
    df['Chiller 4 - koeling'] = df['Chiller 4 - koeling'].mask(lambda x: x > 700)

    ax = df.hist(bins=bins, rwidth=0.9, color='orange', grid=False, layout=(3,1), range=(0,700))
##    ax.xlabel('Gekoeld vermogen (kW)')
    dx0 = ax[0]
    for x in dx0:
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        x.set_ylabel('hours/year', size=16)

        x.set_ylim(0,2000)
                     
    dx1 = ax[1]
    for x in dx1:
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        x.set_ylabel('hours/year', size=16)

        x.set_ylim(0,2000)
    dx2 = ax[2]
    for x in dx2:
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        x.set_ylabel('hours/year', size=16)
        
        x.set_ylim(0,2000)
    plt.show(block=False)
    
def plotHistogramTotaleKoelvraag(timeinterval, bins):
    df = pd.DataFrame()

##    df['Chiller 1 - koeling'] = df['Chiller 1 - koeling'].mask(lambda x: x < 0)
##    df['Chiller 1 - koeling'] = df['Chiller 1 - koeling'].mask(lambda x: x > 700)
##    df['Chiller 3 - koeling'] = df['Chiller 3 - koeling'].mask(lambda x: x < 0)
##    df['Chiller 3 - koeling'] = df['Chiller 3 - koeling'].mask(lambda x: x > 700)
##    df['Chiller 4 - koeling'] = df['Chiller 4 - koeling'].mask(lambda x: x < 0)
##    df['Chiller 4 - koeling'] = df['Chiller 4 - koeling'].mask(lambda x: x > 700)

    df['koeling totaal'] = Chillerdata['Chiller 1 - koelvermogen']+Chillerdata['Chiller 3 - koelvermogen']+Chillerdata['Chiller 4 - koelvermogen']

    df['koeling totaal'] = df['koeling totaal'].resample(timeinterval, label='left', convention='start').max()
    ax = df['koeling totaal'].hist(bins=bins, rwidth=0.9, color='orange', grid=False)
##    ax.spines['right'].set_visible(False)
##    ax.spines['top'].set_visible(False)
##    ax.spines['left'].set_visible(False)
    ax.set_title('Combined cooling requirement', size = 24)
    ax.set_ylabel('hours/year', size=20)
    ax.set_xlim(0,2100)
    ax.set_xlabel('Cooled power (kW)', size=20)
##
    plt.show(block=False)




def plotHistogramFlow(timeinterval, bins):
    df = pd.DataFrame()
    df['Chiller 1 - flow'] = Chillerdata['Chiller1 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 3 - flow'] = Chillerdata['Chiller3 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 4 - flow'] = Chillerdata['Chiller4 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    
    ax = df.hist(bins=bins, rwidth=0.9, color='orange', grid=False, layout=(3,1), range=(0,350))
    
##    ax.xlabel('Icewater flow(m3/h)')
    dx0 = ax[0]
    for x in dx0:
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        x.set_ylabel('uren/jaar', size=16)

        x.set_ylim(0,2000)
                     
    dx1 = ax[1]
    for x in dx1:
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        x.set_ylabel('uren/jaar', size=16)

        x.set_ylim(0,2000)
    dx2 = ax[2]
    for x in dx2:
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)
        x.set_ylabel('uren/jaar', size=16)
        
        x.set_ylim(0,2000)
    plt.show(block=False)
    

def plotHistogramWaterflowTotal(timeinterval, bins):
    df = pd.DataFrame()
    df['Chiller 1 - flow'] = Chillerdata['Chiller1 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 3 - flow'] = Chillerdata['Chiller3 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 4 - flow'] = Chillerdata['Chiller4 - Flow'].resample(timeinterval, label='left', convention='start').mean()


    df['flow totaal'] = df['Chiller 1 - flow']+df['Chiller 3 - flow']+df['Chiller 4 - flow']
    ax = df['flow totaal'].hist(bins=bins, rwidth=0.9, color='orange', grid=False)
    ax.set_title('Combined icewater flow', size = 24, fontweight = 'bold')
    ax.set_ylabel('hours/year', size=20, fontweight = 'bold')
    ax.set_xlim(0,1000)
    ax.set_xlabel('Flow (m3/h)')
##
    plt.show(block=False)
