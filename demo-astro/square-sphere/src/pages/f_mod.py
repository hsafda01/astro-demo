import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import yfinance as yf
from MCForecastTools import MCSimulation


    
spy_ticker = yf.Ticker('SPY')
spy = spy_ticker.history(period = 'max')

agg_ticker = yf.Ticker('AGG')
agg = agg_ticker.history(period = 'max')

df = pd.concat([spy,agg],axis = 'columns',keys =['spy','agg'],join = 'inner')
df.rename(columns = {'Close':'close'},inplace = True)
df.to_csv('stock_data_final.csv',index = False)
data = pd.read_csv('stock_data_final.csv')
# data.head()
# print(data)
weights = [.45,.55]
simulation = MCSimulation(portfolio_data = df,  weights= weights , num_simulation = 500 ,num_trading_days = 252)
simulation.calc_cumulative_return()
simulation.plot_simulation()
simulation.plot_distribution()
stats = simulation.summarize_cumulative_return()
initial_investment = 20000
ci_upper = stats[9]*initial_investment
ci_lower = stats[8]*initial_investment
mean_return = round((((stats[1]*initial_investment)-initial_investment)/initial_investment)*100,2)
print(f'Expected portfolio returns with 95% upper confidence interval : {round(ci_upper,2)}')
print(f'Expected portfolio returns with 95% lower confidence interval : {round(ci_lower,2)}')
