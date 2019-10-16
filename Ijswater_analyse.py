import pandas as pd
import datetime
from openpyxl import Workbook
import matplotlib.pyplot as plt

CPwater = 4.185     #kJ/kgK

WESdark = 'orange'
WESorange = 'darkgreen'

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

#Middel over uur, dag en week
Chillerdata_hour = Chillerdata.resample('H', label='left', convention='start').mean()
Chillerdata_day = Chillerdata.resample('D', label='left', convention='start').mean()
Chillerdata_week = Chillerdata.resample('w', label='left', convention='start').mean()


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



##Plot COP and Maximum daily temperature
def plotCOP():
    fig, ax1 = plt.subplots()
    ax1.plot(Chillerdata_week.index, Chillerdata_week['Chiller1 - COP'])
    ax1.plot(Chillerdata_week.index, Chillerdata_week['Chiller3 - COP'])
    ax1.plot(Chillerdata_week.index, Chillerdata_week['Chiller4 - COP'])
    ax2 = ax1.twinx()

    ax2.plot(Weergegevens_week.index, Weergegevens_week['Tmax'], color = 'Red')
    plt.show(block=False)

##Plot Koelvraag (kW) en max dagtemperatuur
def plotKoelvraag(timeinterval):

    df = pd.DataFrame()
    df['Chiller 1 - koelvermogen'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
##    df['Chiller 3 - koelvermogen'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
##    df['Chiller 4 - koelvermogen'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()   
##    df['Tbuiten'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Chiller 1 - koelvermogen'], color='Darkblue')
##    ax.plot(df.index, df['Chiller 3 - koelvermogen'], color='Lightblue')
##    ax.plot(df.index, df['Chiller 4 - koelvermogen'], color='Orange')
##    ax.plot(df.index, df['Chiller 1 - koelvermogen']+df['Chiller 3 - koelvermogen']+df['Chiller 4 - koelvermogen'])
    ax.set_title('Koelvraag chiller 1')
    ax.set_ylabel('Totale koelvraag (kW)')
    plt.ylim(bottom=0)
    ax2 = ax.twinx()

##    ax2.plot(df.index, df['Tbuiten'], color = 'Red')
##    ax2.set_ylabel('Buitentemperatuur')
    plt.show(block=False)




def plotChiller1Temp(timeinterval):
    df1 = pd.DataFrame()
    df1['Chiller1 - Flow'] = Chillerdata['Chiller1 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df1['Chiller1 - Tuit'] = Chillerdata['Chiller1 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df1['Chiller1 - Tin'] = Chillerdata['Chiller1 - Tin'].resample(timeinterval, label='left', convention='start').mean()
    df1['Tbuiten'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    fig, ax = plt.subplots()
    ax.plot(df1.index, df1['Chiller1 - Tuit'], color='Darkblue')
    ax.plot(df1.index, df1['Chiller1 - Tin'], color='Lightblue')
    ax.tick_params(axis='y', colors='Darkblue')


    ax2 = ax.twinx()
    ax2.plot(df1.index, df1['Tbuiten'], color='Orange')
    ax2.tick_params(axis='y', colors='Orange')
    plt.show(block=False)

def plotChiller3Temp(timeinterval):
    df2 = pd.DataFrame()
    df2['Chiller3 - Flow'] = Chillerdata['Chiller3 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df2['Chiller3 - Tuit'] = Chillerdata['Chiller3 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df2['Chiller3 - Tin'] = Chillerdata['Chiller3 - Tin'].resample(timeinterval, label='left', convention='start').mean()
    df2['Tbuiten'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    fig, ax = plt.subplots()
    ax.plot(df2.index, df2['Chiller3 - Tuit'], color='Darkblue')
    ax.plot(df2.index, df2['Chiller3 - Tin'], color='Lightblue')
    ax.tick_params(axis='y', colors='Darkblue')


    ax2 = ax.twinx()
    ax2.plot(df2.index, df2['Tbuiten'], color='Orange')
    ax2.tick_params(axis='y', colors='Orange')
    plt.show(block=False)



def plotChiller4Temp(timeinterval):
    df4 = pd.DataFrame()
    df4['Chiller4 - Flow'] = Chillerdata['Chiller4 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df4['Chiller4 - Tuit'] = Chillerdata['Chiller4 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df4['Chiller4 - Tin'] = Chillerdata['Chiller4 - Tin'].resample(timeinterval, label='left', convention='start').mean()
    df4['Tbuiten'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    fig, ax = plt.subplots()
    ax.plot(df4.index, df4['Chiller4 - Tuit'], color='Darkblue')
    ax.plot(df4.index, df4['Chiller4 - Tin'], color='Lightblue')
    ax.tick_params(axis='y', colors='Darkblue')


    ax2 = ax.twinx()
    ax2.plot(df4.index, df4['Tbuiten'], color='Orange')
    ax2.tick_params(axis='y', colors='Orange')
    plt.show(block=False)


def plotChiller1Data(timeinterval, size):
    df = pd.DataFrame()
    df['Chiller 1 - koelvermogen'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller1 - Flow'] = Chillerdata['Chiller1 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller1 - Tuit'] = Chillerdata['Chiller1 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x > 700)

    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    df['Tmin'] = Weergegevens['Tmin'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmax'] = Weergegevens['RHmax'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmin'] = Weergegevens['RHmin'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df['Chiller1 - Flow'], df['Chiller 1 - koelvermogen'], s=size, c=df['Tmax'], alpha=0.5)
    plt.show(block=False)


def plotChiller1Data(timeinterval, size):
    df = pd.DataFrame()

    df['Chiller 3 - koelvermogen'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller3 - Flow'] = Chillerdata['Chiller3 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller3 - Tuit'] = Chillerdata['Chiller3 - Tuit'].resample(timeinterval, label='left', convention='start').mean()

    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x > 700)
    
    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    df['Tmin'] = Weergegevens['Tmin'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmax'] = Weergegevens['RHmax'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmin'] = Weergegevens['RHmin'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df['Chiller3 - Flow'], df['Chiller 3 - koelvermogen'], s=size, c=df['Tmax'], alpha=0.5)
    plt.show(block=False)


def plotChiller1Data(timeinterval, size):
    df = pd.DataFrame()
    df['Chiller 4 - koelvermogen'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller4 - Flow'] = Chillerdata['Chiller4 - Flow'].resample(timeinterval, label='left', convention='start').mean()
    df['Chiller4 - Tuit'] = Chillerdata['Chiller4 - Tuit'].resample(timeinterval, label='left', convention='start').mean()
        
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x < 0)
    df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x > 700)

    df['Tmax'] = Weergegevens['Tmax'].resample(timeinterval, label='left', convention='start').mean()
    df['Tmin'] = Weergegevens['Tmin'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmax'] = Weergegevens['RHmax'].resample(timeinterval, label='left', convention='start').mean()
    df['RHmin'] = Weergegevens['RHmin'].resample(timeinterval, label='left', convention='start').mean()
    
    plt.scatter(df['Chiller4 - Flow'], df['Chiller 4 - koelvermogen'], s=size, c=df['Tmax'], alpha=0.5)
    plt.show(block=False)


def plotChillerTotalData(timeinterval, size):
     df['Chiller 1 - koelvermogen'] = Chillerdata['Chiller 1 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
     df['Chiller 3 - koelvermogen'] = Chillerdata['Chiller 3 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()
     df['Chiller 4 - koelvermogen'] = Chillerdata['Chiller 4 - koelvermogen'].resample(timeinterval, label='left', convention='start').mean()

     df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x < 0)
     df['Chiller 1 - koelvermogen'] = df['Chiller 1 - koelvermogen'].mask(lambda x: x > 700)
     df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x < 0)
     df['Chiller 3 - koelvermogen'] = df['Chiller 3 - koelvermogen'].mask(lambda x: x > 700)
     df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x < 0)
     df['Chiller 4 - koelvermogen'] = df['Chiller 4 - koelvermogen'].mask(lambda x: x > 700)
     
     df['koelvermogen totaal'] = df['Chiller 1 - koelvermogen']+df['Chiller 3 - koelvermogen']+df['Chiller 4 - koelvermogen']
    

##plotChiller4Temp('1d')
##plotChiller1Temp('2d')


