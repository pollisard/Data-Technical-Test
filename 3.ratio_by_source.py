import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
bad_df = pd.read_csv('./data/bad.csv')
good_df = pd.read_csv('./data/good.csv')

bad_df['Join'] = pd.to_datetime(bad_df['Join'])
good_df['Join'] = pd.to_datetime(good_df['Join'])

# Group by source and merge
bad_by_source_df = bad_df.groupby('Source').size().reset_index(name='bad count')
good_by_source_df = good_df.groupby('Source').size().reset_index(name='good count')

all_by_source_df = pd.merge(bad_by_source_df, good_by_source_df, on='Source')

# Add ratio to df
all_by_source_df['ratio'] = all_by_source_df['bad count'] / all_by_source_df['good count']

# Drop the source '0' since it has a much higher ratio than the rest
# so it warps the plot and creates difficulty when visualizing the other data.
all_by_source_df = all_by_source_df.drop([0])

# Sort the sources by descending ratio
all_by_source_df = all_by_source_df.sort_values(by='ratio', ascending=False).reset_index(drop=True)

# Plot the data
all_by_source_df.boxplot(column='ratio', by='Source', figsize=(10, 5))
plt.xlabel('Source ID')
plt.ylabel('Bad to Good Ratio')
plt.show()

# From the visual examination we could determine that sources with a bad to good ratio over
# 50 stand out of the norm and may be the main cause of the problems
sources_ratio_over_50_df = all_by_source_df.apply(lambda row: row[all_by_source_df['ratio'] > 50])

print(sources_ratio_over_50_df)

# What would the first graph we generated look like without these sources?
top10_sources_ratio_over_50_list = sources_ratio_over_50_df['Source'].values.tolist()

bad_filtered_df = bad_df[~bad_df['Source'].isin(top10_sources_ratio_over_50_list)]
good_filtered_df = good_df[~good_df['Source'].isin(top10_sources_ratio_over_50_list)]

bad_filtered_count_df = bad_filtered_df.groupby(pd.Grouper(key='Join', freq='5min')).size()
good_filtered_count_df = good_filtered_df.groupby(pd.Grouper(key='Join', freq='5min')).size()

bad_accumulated_count_df = bad_filtered_count_df.rolling('60min').sum()
good_accumulated_count_df = good_filtered_count_df.rolling('60min').sum()

hourly_ratio_filtered_df = bad_accumulated_count_df / good_accumulated_count_df

plt.plot(hourly_ratio_filtered_df.index, hourly_ratio_filtered_df.values, label='Hourly Ratio')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Bad to Good Ratio')
plt.axhline(y=np.nanmean(hourly_ratio_filtered_df[1]))
plt.show()