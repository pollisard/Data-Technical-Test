import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
bad_df = pd.read_csv('./data/bad.csv')
good_df = pd.read_csv('./data/good.csv')

# Convert 'Join' column to date time
bad_df['Join'] = pd.to_datetime(bad_df['Join'])
good_df['Join'] = pd.to_datetime(good_df['Join'])

# Top10 sources list
bad_by_source_df = bad_df.groupby('Source').size().reset_index()
good_by_source_df = good_df.groupby('Source').size().reset_index()

all_by_source_df = pd.concat([bad_by_source_df, good_by_source_df])\
    .groupby(['Source']).sum().reset_index()

all_by_source_df = all_by_source_df.sort_values(by=all_by_source_df.columns[1], ascending=False)

top10_sources_list = all_by_source_df.head(10)['Source'].values.tolist()

# Filter by top10 sources
bad_top10_df = bad_df[bad_df['Source'].isin(top10_sources_list)]
good_top10_df = good_df[good_df['Source'].isin(top10_sources_list)]

# Group by 5 min span
bad_top10_count_df = bad_top10_df.groupby(pd.Grouper(key='Join', freq='5min')).size()
good_top10_count_df = good_top10_df.groupby(pd.Grouper(key='Join', freq='5min')).size()

# Accumulate previous hour results
bad_top10_count_hourly_df = bad_top10_count_df.rolling('60min').sum()
good_top10_count_hourly_df = good_top10_count_df.rolling('60min').sum()

# Ratio
hourly_ratio_top10_df = bad_top10_count_hourly_df / good_top10_count_hourly_df

# Plot
plt.plot(hourly_ratio_top10_df.index, hourly_ratio_top10_df.values, label='Hourly Ratio')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Bad to Good Ratio Top 10 Sources')
plt.axhline(y=np.nanmean(hourly_ratio_top10_df[1]))
plt.show()
