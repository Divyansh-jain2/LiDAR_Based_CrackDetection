import pandas as pd
import numpy as np

df = pd.read_csv(r"test.csv")

print(df.columns)

df['Time'] = pd.to_datetime(df['Timestamp'])

df.drop(columns='Timestamp', axis=1, inplace=True)
df['Total_Seconds'] = df['Time'].dt.hour * 3600 + \
    df['Time'].dt.minute * 60 + df['Time'].dt.second

positive_bound = 80
negative_bound = 270
df = df[(df['Angle (degrees)'] <= positive_bound) |
        (df['Angle (degrees)'] >= negative_bound)]

df['Time'] = df['Time'].dt.floor('s')  # Round down to the nearest second
max_distance = df['Distance (mm)'][np.isfinite(df['Distance (mm)'])].max()

# Replace infinite values with the maximum distance found
df['Distance (mm)'].replace([np.inf, -np.inf], max_distance, inplace=True)

df_avg = df.groupby(['Time', 'Angle (degrees)'])[
    'Distance (mm)'].mean().reset_index()
df_avg['Angle (degrees)'] = df_avg['Angle (degrees)'].round()
df_avg = df_avg.groupby(['Time', 'Angle (degrees)'])[
    'Distance (mm)'].mean().reset_index()
print(df_avg)
df_avg.to_csv('test.csv', index=False)

df_pivot = df_avg.pivot(
    index='Time', columns='Angle (degrees)', values='Distance (mm)')

df_pivot = df_pivot.apply(lambda row: row.fillna(
    method='ffill').fillna(method='bfill'), axis=1)
print(df_pivot)
df_pivot.reset_index(inplace=True)


angle_columns_8_to_90 = [col for col in df_pivot.columns if isinstance(
    col, (int, float)) and 8 <= col <= 90]
reversed_columns_8_to_90 = angle_columns_8_to_90[::-1]
angle_columns_above_200 = [
    col for col in df_pivot.columns if isinstance(col, (int, float)) and col > 200]
reversed_columns_above_200 = angle_columns_above_200[::-1]

new_columns_order = (['Time'] + reversed_columns_8_to_90 + [col for col in df_pivot.columns if col not in angle_columns_8_to_90 and col not in angle_columns_above_200 and col != 'Time'] + reversed_columns_above_200
                     )

df_final = df_pivot[new_columns_order]

df_final.iloc[:, 1:] = df_final.iloc[:, 1:].diff()
df_final.reset_index(drop=True, inplace=True)  # Reset the index
df_final = df_final.drop(index=0)  # Drop the first row
df_final.iloc[:, 1:] = np.trunc(df_final.iloc[:, 1:].values * 1000) / 1000

df_final.to_csv('lidar_data_processed.csv', index=False)


