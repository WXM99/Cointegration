from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint
import numpy as np
import pandas as pd
from pandas import *

class Cointegration:
    "the class encapsulating cointegration opes on two stocks."
    chn_stock_dict = {}
    chn_stock_name = ""
    chn_stock_code = ""
    usa_stock_dict = {}
    usa_stock_name = ""
    usa_stock_code = ""

    usa_stock_value = []
    chn_stock_value = []
    
    def __init__(self, stock_chn, stock_usa):
        self.chn_stock_dict = stock_chn
        self.usa_stock_dict = stock_usa
        chn_val = list()
        usa_val = list()
        for (date, value) in self.chn_stock_dict.items():
            chn_val.append(value)
        self.chn_stock_value = chn_val
        for (date, value) in self.usa_stock_dict.items():
            usa_val.append(value)
        self.usa_stock_value = usa_val
    
    def __testSingleStationarity(self, data):
        adftest = adfuller(data)
        result = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])
        for key,value in adftest[4].items():
            result['Critical Value (%s)'%key] = value
        return result

    def testSationarity(self): 
        chn_val = self.chn_stock_value
        usa_val = self.usa_stock_value
        chn_val=np.array(chn_val).T[0]
        usa_val=np.array(usa_val).T[0]
        res=pd.concat([self.__testSingleStationarity(chn_val),self.__testSingleStationarity(usa_val)],axis=1)
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

    def diffVals(self, n):
        chn_val = self.chn_stock_value
        diff_chn=chn_val.diff(n).dropna(inplace=True)
        diff_chn=np.array(diff_chn).T[0]
        usa_val = self.usa_stock_value
        diff_usa=usa_val.diff(n).dropna(inplace=True)
        diff_usa=np.array(diff_usa).T[0]
        res=pd.concat([self.__testSingleStationarity(diff_chn),self.__testSingleStationarity(diff_usa)],axis=1)
        res.columns=[self.chn_stock_name,self.chn_stock_name]
        return res

    def coint(self):
        chn_val = self.chn_stock_value
        usa_val = self.usa_stock_value
        chn_val=np.array(chn_val)
        usa_val=np.array(usa_val)
        a,pvalue,b = coint(chn_val,usa_val)
        return pvalue

    def getSpreadPrice(self):
        chn_val = np.array(self.chn_stock_value)
        usa_val = np.array(self.usa_stock_value)
        return chn_val-usa_val

    def getParas(self):
        spread = self.getSpreadPrice()
        mean = spread.mean()
        std = spread.std()
        return {"mean": mean, "upper": mean + std, "lower": mean-std}

    '''
    1.spread_price is greater than upper: short position
    2.spread_price is lower than lower: open position
    3.spread_price is closer to zero: close position
    '''