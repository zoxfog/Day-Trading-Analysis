#!/usr/bin/env python
# coding: utf-8

# ## Financial Data
# 
# * This python file includes a class for financial data extraction from Yahoo Finance.
# 

# In[8]:


import yfinance as yf
import pandas as pd
import datetime
import numpy as np


# In[14]:



#class for getting specific financial data of a given financial instrument
class financialData:

    def __init__(self, name):
        self.Instrument = name
        
    #get an assets volume of a given day
    def getVolume(self,date):
        date_end = date + datetime.timedelta(days=1)
        date_end = date_end.strftime('%Y-%m-%d')
        date_start = date_end
        
        period_data = yf.download(self.Instrument, start = date_start, end = date_end, interval = "1D" )
        volume  = period_data['Volume'][0]
        return volume
    
       
    #get an assets gap percentage of a given day         
    def getGap(self,date):
        
        #collect the data
        date_end = date + datetime.timedelta(days=1)
        date_start = date 
        period_data = yf.download(self.Instrument, start = date_start, end = date_end, interval = "1D" )
        
        while len(period_data)<2:
            date_start -= datetime.timedelta(days=1) 
            period_data = yf.download(self.Instrument, start = date_start, end = date_end, interval = "1D" )

        #calculate gap percent
        gap =period_data['Open'][1] - period_data['Close'][0]
        gap_percent = gap/period_data['Close'][0]*100
        
        return gap_percent
    
    # get the percent change until a given date from a given period trailing back
    def percentChange(self,date,period):
        date_end = date + datetime.timedelta(days=1)
        date_start = date - datetime.timedelta(days=period)
        period_data = yf.download(self.Instrument, start = date_start, end = date_end, interval = "1D" )
        
        #calculate the price change
        change =period_data['Open'].iloc[-1] - period_data['Close'][0]
        change_percent = change/period_data['Close'][0]*100
        return change_percent
    
    #get an assets relative volume
    def relativeVolume(self,date):
        three_month_period = 89
        date_end = date + datetime.timedelta(days=1)
        date_start = date - datetime.timedelta(days=three_month_period)
        
        #get the trailing 90 day trailing volume and the given days volume
        period_data = yf.download(self.Instrument, start = date_start, end = date, interval = "1D" )
        date_volume = self.getVolume(date)
        
        #calculate the price change
        rv =date_volume/period_data['Volume'].mean()
        return rv

