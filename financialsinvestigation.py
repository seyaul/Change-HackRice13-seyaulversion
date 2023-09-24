import yfinance as yf
import pandas as pd
import allocation 
import statistics

top_tech_stocks = ['AAPL','MSFT','GOOG','AMZN','NVDA','TSLA','META','TSM','TCEHY',
        'AVGO','ORCL','ADBE','ASML','BABA','CSCO','CRM','NFLX','SAP','AMD',
        'TXN','INTC','INTU','IBM','PDD','QCOM','NOW','BKNG','SONY',
        'ADP','UBER','ADI','ABNB','LRCX','MU','ATVI','VMW','FI','PANW',
        'EQIX','SHOP','SNPS','NTES','MELI','PYPL','CDNS','KLAC','WDAY','ANET',
        'ROP','ARM','NXPI','DELL','TEAM','SNOW','JD','BIDU','FTNT','MRVL',
        'ADSK','MCHP','ON','STM','CRWD','XIACF','TTD','IQV','FIS',
        'VEEV','MBLY','EA','CSGP','GFS','GPN','CPNG','SPOT','PLTR','DASH',
        'DDOG','SQ']

tech_df = pd.DataFrame()

for stock in top_tech_stocks:
    temp_dict = {'Stock':stock, 
                 'Beginning Index':yf.Ticker(stock).history(period="12mo")['Close'][0], 
                 'Ending Index':yf.Ticker(stock).history(period="12mo")['Close'][-1], 
                 'Percent Change':(yf.Ticker(stock).history(period="12mo")['Close'][-1]/yf.Ticker(stock).history(period="12mo")['Close'][0]-1)}
    temp = pd.DataFrame(temp_dict, index=[0])
    tech_df = pd.concat([tech_df, temp])

tech_df.sort_values(by='Percent Change', inplace=True, ascending=False)

top25 = tech_df.head(25)
average = statistics.mean(top25['Percent Change'].tolist())
print(average)