#Question 1: Distance Matrix Calculation
import pandas as pd

def calculate_distance_matrix(df):
    distances = pd.DataFrame(index=df['id_start'], columns=df['id_end'])

    for start_id in df['id_start'].unique():
        for end_id in df['id_end'].unique():
            if start_id == end_id:
                distances.loc[start_id, end_id] = 0
            else:
                distance = df[(df['id_start'] == start_id) & (df['id_end'] == end_id)]['distance'].sum()
                distances.loc[start_id, end_id] = distance
                distances.loc[end_id, start_id] = distance

    return distances

#Question 2: Unroll Distance Matrix
def unroll_distance_matrix(df):
    unrolled_data = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for id_start in df.index:
        for id_end in df.columns:
            if id_start != id_end:
                distance = df.loc[id_start, id_end]
                unrolled_data = unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)

    return unrolled_data

#Question 3: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(df, reference_id):
    reference_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_distance

    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= (reference_distance - threshold)) & (result_df['distance'] <= (reference_distance + threshold))]
    
    return result_df

#Question 4: Calculate Toll Rate
def calculate_toll_rate(df):
    toll_rates = pd.DataFrame(columns=['id_start', 'id_end', 'distance', 'vehicle_type', 'toll_rate'])

    for index, row in df.iterrows():
        toll_rate = row['distance'] * {
            'moto': 0.8,
            'car': 1.2,
            'rv': 1.5,
            'bus': 2.2,
            'truck': 3.6
        }[row['vehicle_type']]

        toll_rates = toll_rates.append({'id_start': row['id_start'], 'id_end': row['id_end'], 'distance': row['distance'],
                                        'vehicle_type': row['vehicle_type'], 'toll_rate': toll_rate}, ignore_index=True)

    return toll_rates

#Question 5: Calculate Time-Based Toll Rates
import datetime

def calculate_time_based_toll_rates(df):
    time_based_toll_rates = pd.DataFrame(columns=['id_start', 'id_end', 'distance', 'vehicle_type', 'timestamp', 'toll_rate'])

    for index, row in df.iterrows():
        if row['timestamp'].weekday() < 5:  # Weekdays
            if datetime.time(0, 0, 0) <= row['timestamp'].time() < datetime.time(10, 0, 0):
                discount_factor = 0.8
            elif datetime.time(10, 0, 0) <= row['timestamp'].time() < datetime.time(18, 0, 0):
                discount_factor = 1.2
            else:
                discount_factor = 0.8
        else:  # Weekends
            discount_factor = 0.7

        toll_rate = row['distance'] * discount_factor

        time_based_toll_rates = time_based_toll_rates.append({'id_start': row['id_start'], 'id_end': row['id_end'],
                                                              'distance': row['distance'], 'vehicle_type': row['vehicle_type'],
                                                              'timestamp': row['timestamp'], 'toll_rate': toll_rate},
                                                             ignore_index=True)

    return time_based_toll_rates

