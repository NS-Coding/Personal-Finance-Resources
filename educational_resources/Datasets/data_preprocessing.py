import pandas as pd



def BTOP50_data():
    CTA = pd.read_excel('/Users/davidfitzpatrick/Desktop/Codes/Newer_codes/Data_sets/BTOP50_Index_historical_data.xls',header=1)
    CTA = CTA.rename(columns={'Jan':1,
                        'Feb':2,
                        'Mar':3,
                        'Apr':4,
                        'May':5,
                        'Jun':6,
                        'Jul':7,
                        'Aug':8,
                        'Sep':9,
                        'Oct':10,
                        'Nov':11,
                        'Dec':12,
                        'Unnamed: 0':'Date'})
    #the .iloc[:number] determines the years used
    CTA = CTA.iloc[:38]

    #the .iloc[:number] determines the last month of data
    CTA = CTA.set_index('Date').T.unstack().reset_index().iloc[:-1]

    CTA['level_1'] = CTA['level_1'].astype(str)

    CTA['Date'] = CTA['Date'].astype(str).str[:-2]

    CTA['Date'] = CTA['Date'] + '-' + CTA['level_1']

    CTA = CTA.drop(columns='level_1')

    CTA['Date'] = pd.to_datetime(CTA['Date'], format='%Y-%m')

    CTA = CTA.rename(columns={0:'CTA'})
    return CTA

#http://www.econ.yale.edu/~shiller/data.htm
def shiller_data():
    temp = pd.read_csv("/Users/davidfitzpatrick/Desktop/Codes/Newer_codes/Data_sets/shiller_stock_data.csv").iloc[:,[0,9,18]].dropna()
    temp.loc[temp['Date'].str.len()==6,'Date'] = temp.loc[temp['Date'].str.len()==6,'Date']+'0'
    temp['Date'] = temp['Date'].str.replace('-','').str.replace('.','')
    temp['Date'] = pd.to_datetime(temp['Date'], format='%Y%m')
    return temp.set_index('Date')