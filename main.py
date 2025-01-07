import MetaTrader5 as mt5 # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore

# Initialize MT5 connection
if not mt5.initialize():
    print("initialize() failed!")
    mt5.shutdown()

# Define the symbol and tiemframe
symbol = "EURUSD" 
timeframe = mt5.TIMEFRAME_M1
num_bars = 1000

# fetch Historicl Data
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

# Convert to a pands Dataframes
data = pd.DataFrame(rates)
data['time'] = pd.to_datetime(data['time'], unit = 's')
data.set_index('time' , inplace=True)

# Calculate the 50 period-EMA 
data['EMA_50'] = data['close'].ewm(span=50, adjust=False).mean()

# Print the Last few Rowsto see EMA
print(data[['close' , 'EMA_50']].tail())

# Export to CSV
csv_file_path = 'ema.csv'
data[['close', 'EM_50']].to_csv(csv_file_path)

print(f"Data exported to {csv_file_path}")

# Optional plot EMA using Matplotlib
import matplotlib.pyplot as plt # type: ignore

plt.figure(figsize=(12,6))
plt.plot(data.index, data['close'], label='Close Price', color='blue')
plt.plot(data.index, data['EMA_50'], label='EMA_50', color='red')
plt.title(f'{symbol} Price and 50 EMA ')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.grid()
plt.show()

# Shutdown connection to MetaTrader5
mt5.shutdown()

