import pandas as pd
import datetime
from openpyxl import Workbook
import matplotlib
import matplotlib.pyplot as plt
##import seaborn as sb
from matplotlib import colors as mcolors
matplotlib.rc('font',family='Palatino Linotype')
matplotlib.rc('font',size = 16)


colorBarMin = 1
colorBarMax = 5
xAxisSize = 16
yAxisSize = 20
titleSize = 24

CPwater = 4.185     #kJ/kgK

WESdark = '#193333'
WESorange = '#ff5900'

Chillerdata = pd.read_csv("Chillerdata.csv", sep=';', parse_dates=[0], dayfirst=True, low_memory=False, dtype='float64')                      
Chillerdata.reset_index(inplace=True)
Chillerdata.set_index(pd.DatetimeIndex(Chillerdata['Datum']), inplace=True)
Chillerdata.fillna(0)


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

##Laad weergegevens van lelystad
Weergegevens = pd.read_csv("WeergegevensLelystad.csv", sep=';', parse_dates=[0], dayfirst=True, low_memory=False, dtype='float64')
Weergegevens.reset_index(inplace=True)
Weergegevens.set_index(pd.DatetimeIndex(Weergegevens['Datum']), inplace=True)
Weergegevens = Weergegevens[(Weergegevens['Datum'] >= pd.Timestamp("10-01-2017")) & (Weergegevens['Datum'] <= pd.Timestamp("30-09-2018"))]
Weergegevens = Weergegevens.drop('Datum', axis=1)
Weergegevens['Tmin'] = Weergegevens['TN']/10
Weergegevens['Tmax'] = Weergegevens['TX']/10
Weergegevens['RHmin'] = Weergegevens['UN']/100
Weergegevens['RHmax'] = Weergegevens['UX']/100
Weergegevens_week = Weergegevens.resample('w', label='left', convention='start').mean()






def plotChiller1Data(timeinterval, size):
    df = pd.DataFrame()
    df['Chiller 1 - koelvermogen'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller1 - Flow'] = Chillerdata['Chiller1 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller1 - Tuit'] = Chillerdata['Chiller1 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller1 - COP'] = Chillerdata['Chiller1 - COP'].resample(timeinterval, label='left', convention='start').mean()

    df['Chiller1 - Tuit'] = df['Chiller1 - Tuit'].mask(lambda x: x < 0)
    df['Chiller1 - Tuit'] = df['Chiller1 - Tuit'].mask(lambda x: x > 7)
    
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x > 700)


    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    df['Tmin'] = Weergegevens['Tmin'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmax'] = Weergegevens['RHmax'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmin'] = Weergegevens['RHmin'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df['Tmax'], df['Chiller 1 - koelvermogen'], s=size, c=df['Chiller1 - Tuit'], alpha=0.5, cmap='jet')
    # Plot legend.

    cbar = plt.colorbar()
    cbar.set_label('Ijswater temperatuur '+ '(\u2103)', size=xAxisSize)
    plt.clim(2, 5)
    plt.title('Chiller 1 performance', size=titleSize)
    plt.xlabel('Buitentemperatuur  '+ '(\u2103)', size=xAxisSize)
    plt.ylabel('Gekoeld vermogen (kW)', size=yAxisSize)
    #change the marker size manually for both lines
    #lgnd.legendHandles[0]._legmarker.set_markersize(6)
    #lgnd.legendHandles[1]._legmarker.set_markersize(6)maar
    plt.show(block=False)


def plotChiller3Data(timeinterval, size):
    df = pd.DataFrame()

    df['Chiller 3 - koelvermogen'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller3 - Flow'] = Chillerdata['Chiller3 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller3 - Tuit'] = Chillerdata['Chiller3 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller3 - COP'] = Chillerdata['Chiller3 - COP'].resample(timeinterval, label='left', convention='start').mean()
    
    df['Chiller3 - Tuit'] = df['Chiller3 - Tuit'].mask(lambda x: x < 0)
    df['Chiller3 - Tuit'] = df['Chiller3 - Tuit'].mask(lambda x: x > 7)

    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x > 700)
    
    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    df['Tmin'] = Weergegevens['Tmin'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmax'] = Weergegevens['RHmax'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmin'] = Weergegevens['RHmin'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df['Tmax'], df['Chiller 3 - koelvermogen'], s=size, c=df['Chiller3 - Tuit'], alpha=0.4, cmap='jet')
    # Plot legend.
    
    plt.title('Chiller 3 performance', size=titleSize)
    plt.xlabel('Buitentemperatuur  '+ '(\u2103)', size=xAxisSize)
    plt.ylabel('Gekoeld vermogen (kW)', size=yAxisSize)
    #change the marker size manually for both lines
    #lgnd.legendHandles[0]._legmarker.set_markersize(6)
    #lgnd.legendHandles[1]._legmarker.set_markersize(6)
    cbar = plt.colorbar()
    cbar.set_label('Ijswater temperatuur '+ '(\u2103)', size=xAxisSize)
    plt.clim(2, 5)
    plt.show(block=False)


def plotChiller4Data(timeinterval, size):
    df = pd.DataFrame()
    df['Chiller 4 - koelvermogen'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller4 - Flow'] = Chillerdata['Chiller4 - Flow'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller4 - Tuit'] = Chillerdata['Chiller4 - Tuit'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller4 - COP'] = Chillerdata['Chiller4 - COP'].resample(timeinterval, label='left', convention='start').max()
    
    df['Chiller4 - Tuit'] = df['Chiller4 - Tuit'].mask(lambda x: x < 0)
    df['Chiller4 - Tuit'] = df['Chiller4 - Tuit'].mask(lambda x: x > 7)
    
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x > 700)

    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    df['Tmin'] = Weergegevens['Tmin'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmax'] = Weergegevens['RHmax'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmin'] = Weergegevens['RHmin'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df['Tmax'], df['Chiller 4 - koelvermogen'], s=size, c=df['Chiller4 - Tuit'], alpha=0.5, cmap='jet')
    # Plot legend.
    plt.title('Chiller 4 performance', size=titleSize)
    plt.xlabel('Buitentemperatuur  '+ '(\u2103)', size=xAxisSize)
    plt.ylabel('Gekoeld vermogen (kW)', size=yAxisSize)
    #change the marker size manually for both lines
    #lgnd.legendHandles[0]._legmarker.set_markersize(6)
    #lgnd.legendHandles[1]._legmarker.set_markersize(6)
    cbar = plt.colorbar()
    cbar.set_label('Ijswater temperatuur '+ '(\u2103)', size=xAxisSize)
    plt.clim(2, 5)
    plt.show(block=False)


def plotChiller1Yeardata(timeinterval, size):
    df = pd.DataFrame()
    df['Chiller 1 - koelvermogen'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 1 - Tuit'] = Chillerdata['Chiller1 - Tuit'].resample(timeinterval, label='left', convention='start').max()
    #filter unrealistic datapoints
    df['Chiller 1 - Tuit'] = df['Chiller 1 - Tuit'].mask(lambda x: x < 0)
    df['Chiller 1 - Tuit'] = df['Chiller 1 - Tuit'].mask(lambda x: x > 7)
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x > 700)
    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()

    plt.scatter(df.index, df['Chiller 1 - koelvermogen'], s=size, c=df['Chiller 1 - Tuit'], alpha=0.5, cmap='jet')
    # Plot legend.
    plt.title('Chiller 1 - performance', size=titleSize, fontweight='bold')

    plt.ylabel('Cooled icewater (kW)', size=yAxisSize, fontweight='bold')
    cbar = plt.colorbar()
    cbar.set_label('Iicewater max. temperature (degC)', size=xAxisSize, fontweight='bold')
    plt.clim(2, 5)
    plt.show(block=False)


def plotChiller3Yeardata(timeinterval, size):
    df = pd.DataFrame()
    df['Chiller 3 - koelvermogen'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 3 - Tuit'] = Chillerdata['Chiller3 - Tuit'].resample(timeinterval, label='left', convention='start').max()
    #filter unrealistic datapoints
    df['Chiller 3 - Tuit'] = df['Chiller 3 - Tuit'].mask(lambda x: x < 0)
    df['Chiller 3 - Tuit'] = df['Chiller 3 - Tuit'].mask(lambda x: x > 7)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x > 700)
    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df.index, df['Chiller 3 - koelvermogen'], s=size, c=df['Chiller 3 - Tuit'], alpha=0.5, cmap='jet')
    # Plot legend.
    plt.title('Chiller 3 - performance', size=titleSize, fontweight='bold')

    plt.ylabel('Cooled icewater (kW)', size=yAxisSize, fontweight='bold')
    cbar = plt.colorbar()
    cbar.set_label('Iicewater max. temperature (degC)', size=xAxisSize, fontweight='bold')
    plt.clim(2, 5)
    plt.show(block=False)


def plotChiller4Yeardata(timeinterval, size):
    df = pd.DataFrame()
    df['Chiller 4 - koelvermogen'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller 4 - Tuit'] = Chillerdata['Chiller4 - Tuit'].resample(timeinterval, label='left', convention='start').max()
    #filter unrealistic datapoints
    df['Chiller 4 - Tuit'] = df['Chiller 4 - Tuit'].mask(lambda x: x < 0)
    df['Chiller 4 - Tuit'] = df['Chiller 4 - Tuit'].mask(lambda x: x > 7)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x > 700)
    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df.index, df['Chiller 4 - koelvermogen'], s=size, c=df['Chiller 4 - Tuit'], alpha=0.5, cmap='jet')
    # Plot legend.
    plt.title('Chiller 4 - performance', size=titleSize, fontweight='bold')

    plt.ylabel('Cooled icewater (kW)', size=yAxisSize, fontweight='bold')
    cbar = plt.colorbar()
    cbar.set_label('Iicewater max. temperature (degC)', size=xAxisSize, fontweight='bold')
    plt.clim(2, 5)
    plt.show(block=False)

    
def plotChiller1YeardataBuitentemp(timeinterval, size):
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    df['Chiller 1 - koelvermogen'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 1 - Tuit'] = Chillerdata['Chiller1 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df2['Tmax'] = Weergegevens['Tmax'].resample('w', label='left', convention='start').mean()
    #filter unrealistic datapoints
    df['Chiller 1 - Tuit'] = df['Chiller 1 - Tuit'].mask(lambda x: x < 0)
    df['Chiller 1 - Tuit'] = df['Chiller 1 - Tuit'].mask(lambda x: x > 7)
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x > 700)
    fig, ax = plt.subplots()
    plt.scatter(df.index, df['Chiller 1 - koelvermogen'], s=size, c=df['Chiller 1 - Tuit'], alpha=0.5, cmap='jet')
    ax2 = ax.twinx()
    ax2.plot(df2.index, df2['Tmax'])

    # Plot legend.
    plt.title('Chiller 1', size=titleSize)
    plt.xlabel('Datum', size=xAxisSize)
    ax.set_ylabel('Gekoeld vermogen (kW)', size=yAxisSize)
    ax2.set_ylabel('Buitentemperatuur ' + '(\u2103)', size=yAxisSize)
    cbar = plt.colorbar()
    cbar.set_label('Ijswater temperatuur (degC)', size=xAxisSize)
    plt.clim(2, 5)
    plt.show(block=False)
    
def plotChiller3YeardataBuitentemp(timeinterval, size):
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    df['Chiller 3 - koelvermogen'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 3 - Tuit'] = Chillerdata['Chiller3 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df2['Tmax'] = Weergegevens['Tmax'].resample('w', label='left', convention='start').mean()
    #filter unrealistic datapoints
    df['Chiller 3 - Tuit'] = df['Chiller 3 - Tuit'].mask(lambda x: x < 0)
    df['Chiller 3 - Tuit'] = df['Chiller 3 - Tuit'].mask(lambda x: x > 7)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x > 700)
    fig, ax = plt.subplots()
    plt.scatter(df.index, df['Chiller 3 - koelvermogen'], s=size, c=df['Chiller 3 - Tuit'], alpha=0.5, cmap='jet')
    ax2 = ax.twinx()
    ax2.plot(df2.index, df2['Tmax'])

    # Plot legend.
    plt.title('Chiller 3', size=titleSize)
    plt.xlabel('Datum', size=xAxisSize)
    ax.set_ylabel('Gekoeld vermogen (kW)', size=yAxisSize)
    ax2.set_ylabel('Buitentemperatuur ' + '(\u2103)', size=yAxisSize)
    cbar = plt.colorbar()
    cbar.set_label('Ijswater temperatuur '+ '(\u2103)', size=xAxisSize)
    plt.clim(2, 5)
    plt.show(block=False)
    
def plotChiller4YeardataBuitentemp(timeinterval, size):
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    df['Chiller 4 - koelvermogen'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 4 - Tuit'] = Chillerdata['Chiller4 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df2['Tmax'] = Weergegevens['Tmax'].resample('w', label='left', convention='start').mean()
    #filter unrealistic datapoints
    df['Chiller 4 - Tuit'] = df['Chiller 4 - Tuit'].mask(lambda x: x < 0)
    df['Chiller 4 - Tuit'] = df['Chiller 4 - Tuit'].mask(lambda x: x > 7)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x > 700)
    fig, ax = plt.subplots()
    plt.scatter(df.index, df['Chiller 4 - koelvermogen'], s=size, c=df['Chiller 4 - Tuit'], alpha=0.5, cmap='jet')
    ax2 = ax.twinx()
    ax2.plot(df2.index, df2['Tmax'])

    # Plot legend.
    plt.title('Chiller 4', size=titleSize)
    plt.xlabel('Datum', size=xAxisSize)
    ax.set_ylabel('Gekoeld vermogen (kW)', size=yAxisSize)
    ax2.set_ylabel('Buitentemperatuur ' + '(\u2103)', size=yAxisSize)
    cbar = plt.colorbar()
    cbar.set_label('Ijswater temperatuur '+ '(\u2103)', size=xAxisSize)
    plt.clim(2, 5)
    plt.show(block=False)
    
def plotChillerComparison(timeinterval, size):
    df = pd.DataFrame()

    df['Chiller 1 - koelvermogen'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller 3 - koelvermogen'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller 4 - koelvermogen'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').max()

    df['Chiller1'] = Chillerdata['Chiller1 - COP'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller3'] = Chillerdata['Chiller3 - COP'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller4'] = Chillerdata['Chiller4 - COP'].resample(timeinterval, label='left', convention='start').mean()


    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x > 700)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x > 700)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x > 700)

    plt.scatter(df['Chiller 1 - koelvermogen'], df['Chiller1'], s=size, c='orange', alpha=0.5)
    plt.scatter(df['Chiller 3 - koelvermogen'], df['Chiller3'], s=size, c='Darkblue', alpha=0.5)
    plt.scatter(df['Chiller 4 - koelvermogen'], df['Chiller4'], s=size, c='Crimson', alpha=0.5)
    plt.ylim(0,5)
    plt.xlim(0, 900)
    plt.title('Chiller COP comparison',size=20, fontweight='bold')
    plt.ylabel('COP', size=16, fontweight='bold')
    
    plt.xlabel('Cooled capacity (kW)', size=16, fontweight='bold')
    plt.tick_params(direction='out', length=6, width=2, labelsize=12)
    lgnd = plt.legend(loc="upper right", numpoints=3, fontsize=12)
    plt.show(block=False)

def plotChiller4Flow(timeinterval, size):
    df = pd.DataFrame()
##    df['Chiller 1 - Flow'] = Chillerdata['Chiller1 - Flow'].resample(timeinterval, label='left', convention='start').mean()
##    df['Chiller 3 - Flow'] = Chillerdata['Chiller3 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 4 - Flow'] = Chillerdata['Chiller4 - Flow'].resample(timeinterval, label='left', convention='start').max()
    df['Chiller 4 - Tuit'] = Chillerdata['Chiller4 - Tuit'].resample(timeinterval, label='left', convention='start').max()

##    plt.scatter(df['Chiller 1 - Flow'].index, df['Chiller 1 - Flow'],s=size, c='orange', alpha=0.5)
##    plt.scatter(df['Chiller 3 - Flow'].index, df['Chiller 3 - Flow'],s=size, c='Darkblue', alpha=0.5)
    plt.scatter(df['Chiller 4 - Flow'].index, df['Chiller 4 - Flow'],s=size, c='Crimson', alpha=0.5)
##    plt.scatter(df['Chiller 1 - Flow'].index, df['Chiller 1 - Flow'], s=size, color=WESgreen, alpha=0.5)
##     plt.scatter(df.index, df['RHmax'], s=size, c='Crimson', alpha=0.5)
##     plt.scatter(df.index, df['RHmin'], s=size, c='Darkblue', alpha=0.5)
    plt.title('Chiller 4 ', size=titleSize, fontweight='bold')
    plt.ylabel('Icewater flow (m3/h)', size=yAxisSize, fontweight='bold')
##    cbar = plt.colorbar()
##    cbar.set_label('Icewater max. temperature (d egC)', size=xAxisSize, fontweight='bold')
    plt.clim(2, 5)
    plt.show(block=False)
##plotChiller4Temp('1d')
##plotChiller1Temp('2d')


