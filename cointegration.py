from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint
import numpy as np
import pandas as pd
from pandas import *

class Cointegration:
    "the class encapsulating cointegration opes on two stocks."
    __chn_stock
    chn_stock_name
    chn_stock_code
    __usa_stock
    usa_stock_name 
    usa_stock_code

    __usa_value
    __chn_value
    
    def __init__(self, stock_chn, stock_usa):
        self.__chn_stock = stock_chn
        self.__usa_stock = stock_chn
        chn_val = list()
        usa_val = list()
        for (date, value) in __chn_stock.items():
            chn_val.append(value)
        self.__chn_value = chn_val
        for (date, value) in __usa_stock.items():
            usa_val.append(value)
        self.__usa_value = usa_val
    
    def setChn(self, stock_chn):
        self.__chn_stock = stock_chn

    def setUsa(self, stock_usa):
        self.__usa_stock = stock_usa
    
    def getChn(self):
        return self.__chn_stock
    def getUsa(self):
        return self.__usa_stock
    
    def __testSingleStationarity(data):
        adftest = adfuller(data)
        result = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])
        for key,value in adftest[4].items():
            result['Critical Value (%s)'%key] = value
        return result

    def testsSationarity(): 
        chn_val = self.__chn_value
        usa_val = self.__usa_value
        chn_val=np.array(chn_val).T[0]
        usa_val=np.array(usa_val).T[0]
        res=pd.concat([testStationarity(chn_val),testStationarity(usa_val)],axis=1)
        res.columns=[self.chn_stock_name,self.chn_stock_name]
        return res
    '''
                	            stockC	        stockA
    Test Statistic	            -1.669242e+01	-5.084458
    p-value	1.484626e-29	    0.000015
    Lags Used               	0.000000e+00	6.000000
    Number of Observations Used	2.360000e+02	230.000000
    Critical Value (5%)     	-2.873866e+00	-2.874190
    Critical Value (1%)	        -3.458366e+00	-3.459106
    Critical Value (10%)    	-2.573339e+00	-2.573512
    '''

    def diffVals(n):
        chn_val = self.__chn_value
        diff_chn=chn_val.diff(n).dropna(inplace=True)
        diff_chn=np.array(diff_chn).T[0]
        usa_val = self.__usa_value
        diff_usa=usa_val.diff(n).dropna(inplace=True)
        diff_usa=np.array(diff_usa).T[0]
        res=pd.concat([testStationarity(diff_chn),testStationarity(diff_usa)],axis=1)
        res.columns=[self.chn_stock_name,self.chn_stock_name]
        return res

    def coint():
        chn_val = self.__chn_value
        usa_val = self.__usa_value
        chn_val=np.array(chn_val)
        usa_val=np.array(usa_val)
        a,pvalue,b = coint(chn_val,usa_val)
        return pvalue

    def getSpreadPrice():
        chn_val = self.__chn_value
        usa_val = self.__usa_value
        mean=(chn_val-usa_val).mean()
        std=(chn_val-usa_val).std()
        s1=pd.Series(mean[0],index=range(len(chn_val)))
        s2=pd.Series(mean[0]+std[0],index=range(len(chn_val)))
        s3=pd.Series(mean[0]-std[0],index=range(len(chn_val)))
        res=pd.concat([chn_val-usa_val,s1,s2,s3],axis=1)
        res.columns=['spread_price','mean','upper','lower']
        return res
    '''
    1.spread_price is greater than upper: short position

    2.spread_price is lower than lower: open position

    3.spread_price is closer to zero: close position
    '''





    

    

        
        
            
            
    

