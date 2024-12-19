import pandas as pd
import os

def cut_off_after_phrase(input_string, phrase):
    # Find the index of the phrase in the input string
    index = input_string.find(phrase)
    
    # If the phrase is found, cut off everything after it
    if index != -1:
        return input_string[:index + len(phrase)]
    else:
        # If the phrase is not found, return the original string
        return input_string


def BTOP50_data():
    '''
    Datasource: https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=Barclay-Investable-Benchmarks&indexName=BTOP50-Index

    It's possible this datasource has survivorship bias. Their website claims this is accounted for. Didn't look up methodology details. 
    The returns roughly match my expectation of riskfree rate + risk premium and outsized return during trending markets.
    
    '''
    working_directory = os.getcwd()
    result = cut_off_after_phrase(working_directory, 'educational_resources')
    BTOP50_path = os.path.join(result, "Datasets", "BTOP50_Index_historical_data.xls")

    CTA = pd.read_excel(BTOP50_path,header=1)
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


def msci_world_stock(Net=True):
    '''
    Market Cap weighted world stock index. this is the IMI or investible index so it does not include microcap companies.

    Net returns the series where dividends are taxed at the highest marginal tax rate or something like that
    Gross does not tax dividends

    Index Methodology details: https://www.msci.com/index-methodology

    Datasource: https://www.msci.com/end-of-day-history?chart=regional&priceLevel=0&scope=R&style=C&asOf=Nov%2029,%202024&currency=15&size=41&indexId=73562
    '''
    def msci_processing(df):
        df = df.iloc[4:-19].rename(columns={'Index Level :':'date'})
        df['date'] = pd.to_datetime(df['date'], format='%b %d, %Y')
        df.set_index('date',inplace=True)
        if 'Net' in df.columns:
            df = df['Net'].str.replace(',','').astype(float).pct_change()[1:]
        elif 'Gross' in df.columns: 
            df = df['Gross'].str.replace(',','').astype(float).pct_change()[1:]
        else:
            'need to create case for this type of data'
        return df
    
    working_directory = os.getcwd()
    result = cut_off_after_phrase(working_directory, 'educational_resources')
    msci_world_net_path = os.path.join(result, "Datasets", "msci_world_net.xls")
    msci_world_gross_path = os.path.join(result, "Datasets", "msci_world_gross.xls")

    if Net:
        msci_world = pd.read_excel(msci_world_net_path, header=2)
        msci_world = msci_processing(msci_world)

    else:
        msci_world = pd.read_excel(msci_world_gross_path, header=2)
        msci_world = msci_processing(msci_world)
    
    return msci_world

def shiller_data():
    '''
    Datasource: http://www.econ.yale.edu/~shiller/data.htm
    '''
    working_directory = os.getcwd()
    result = cut_off_after_phrase(working_directory, 'educational_resources')
    shiller_path = os.path.join(result, "Datasets", "shiller_stock_data.csv")
    temp = pd.read_csv(shiller_path).iloc[:,[0,9,18]].dropna()
    temp.loc[temp['Date'].str.len()==6,'Date'] = temp.loc[temp['Date'].str.len()==6,'Date']+'0'
    temp['Date'] = temp['Date'].str.replace('-','').str.replace('.','')
    temp['Date'] = pd.to_datetime(temp['Date'], format='%Y%m')
    return temp.set_index('Date')



def international_stock_data():
    working_directory = os.getcwd()
    result = cut_off_after_phrase(working_directory, 'educational_resources')
    path = os.path.join(result, "Datasets", "JSTdatasetR6.xlsx")
    
    df = pd.read_excel(path)

    cols = ['year','country','cpi','bond_rate','bill_rate',
    'eq_tr','housing_tr','bond_tr','crisisJST']

    selected_data = df[cols]
    selected_data.rename(columns={'cpi':'inflation'},inplace=True)

    #turn cpi into inflation rate
    reduced = {}
    for country in selected_data['country'].unique():
        selected_data.loc[selected_data['country'] == country,'inflation'] = selected_data.loc[selected_data['country'] == country,'inflation'].pct_change()
    
        eq_na_bool = selected_data.loc[selected_data['country'] == country,'eq_tr'].isna().cumprod()
        temp = selected_data.loc[selected_data['country'] == country].drop(eq_na_bool[eq_na_bool==1].index).copy(deep=True)
    
        inflation_na_bool = temp.loc[temp['country'] == country,'inflation'].isna().cumprod()
        reduced[country] = temp.loc[temp['country'] == country].drop(inflation_na_bool[inflation_na_bool==1].index)
    
    data = pd.concat(reduced.values())
    data['eq_tr'] = (data['eq_tr']+1) * (1/(1+data['inflation'])) - 1
    data['housing_tr'] = (data['housing_tr']+1) * (1/(1+data['inflation'])) - 1
    data['bond_tr'] = (data['bond_tr']+1) * (1/(1+data['inflation'])) - 1
    data['bond_rate'] = (data['bond_rate']+1) * (1/(1+data['inflation'])) - 1
    data['bill_rate'] = (data['bill_rate']+1) * (1/(1+data['inflation'])) - 1
    return data