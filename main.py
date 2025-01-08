import MetaTrader5 as mt5 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# Define your credentials
login = 31747620
server = 'Deriv-Demo'
password = 'IronMan4Life@Lex'

# Initialize connection to MetaTrader 5
if not mt5.initialize(login=login, server=server, password=password):
    print("Initialization failed")
    print("Error code:", mt5.last_error())
    mt5.shutdown()
    exit()  # Exit if initialization fails

# Define the symbol and timeframe
symbol = "XAUUSD" 
timeframe = mt5.TIMEFRAME_M1
num_bars = 10000

# Fetch Historical Data
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

# Convert to a pandas DataFrame
data = pd.DataFrame(rates)
data['time'] = pd.to_datetime(data['time'], unit='s')
data.set_index('time', inplace=True)

# Calculate the 50 period EMA 
data['EMA_200'] = data['close'].ewm(span=50, adjust=False).mean()

# Print the last few rows to see EMA
print(data[['close', 'EMA_200']].tail())

# Export to CSV
csv_file_path = 'ema.csv'
data[['close', 'EMA_200']].to_csv(csv_file_path)  # Corrected column name

print(f"Data exported to {csv_file_path}")

# Optional plot EMA using Matplotlib
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['close'], label='Close Price', color='blue')
plt.plot(data.index, data['EMA_200'], label='EMA_200', color='red')
plt.title(f'{symbol} Price and 200 EMA')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.grid()
plt.show()

# Shutdown connection to MetaTrader 5
mt5.shutdown()