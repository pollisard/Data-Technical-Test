import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
bad_df = pd.read_csv('./data/bad.csv')
good_df = pd.read_csv('./data/good.csv')

bad_df['Join'] = pd.to_datetime(bad_df['Join'])
good_df['Join'] = pd.to_datetime(good_df['Join'])

# Group by 5 min span
bad_count_df = bad_df.groupby(pd.Grouper(key='Join', freq='5min')).size()
good_count_df = good_df.groupby(pd.Grouper(key='Join', freq='5min')).size()

# Accumulate previous hour results
bad_count_hourly_df = bad_count_df.rolling('60min').sum()
good_count_hourly_df = good_count_df.rolling('60min').sum()

# Ratio
hourly_ratio_df = bad_count_hourly_df / good_count_hourly_df

# Plot
plt.plot(hourly_ratio_df.index, hourly_ratio_df.values, label='Hourly Ratio')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Bad to Good Ratio')
plt.axhline(y=np.nanmean(hourly_ratio_df[1]))
plt.show()