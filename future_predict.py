import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Load the data
df = pd.read_csv('personal_transactions1.csv')
df['Date'] = pd.to_datetime(df['Date'])  # Convert Date column to datetime

# Group by Date and sum the Amount for each day
daily_spending = df.groupby('Date')['Amount'].sum().reset_index()

# Set Date column as index
daily_spending = daily_spending.set_index('Date')

# Plot the time series data
plt.figure(figsize=(12, 6))
plt.plot(daily_spending)
plt.title('Daily Spending Over Time')
plt.xlabel('Date')
plt.ylabel('Total Amount Spent')
plt.show()

# Train-test split (80% train, 20% test)
train_size = int(len(daily_spending) * 0.8)
train_data, test_data = daily_spending[:train_size], daily_spending[train_size:]

# Fit ARIMA model
model = ARIMA(train_data, order=(5,1,0))
model_fit = model.fit()

# Forecast future spending
forecast = model_fit.forecast(steps=len(test_data))

# Calculate average forecasted cost
average_cost = forecast.mean()

# Plot the forecast
plt.figure(figsize=(12, 6))
plt.plot(test_data.index, test_data, label='Actual')
plt.plot(test_data.index, forecast, color='red', label='Forecast')
plt.title('ARIMA Forecast of Daily Spending')
plt.xlabel('Date')
plt.ylabel('Total Amount Spent')
plt.axhline(y=average_cost, color='green', linestyle='--', label='Average Forecasted Cost')
plt.legend()
plt.show()

print("Average Forecasted Cost:", average_cost)
