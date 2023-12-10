#Question 1: Car Matrix Generation
import pandas as pd

def generate_car_matrix(df):
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[(range(len(car_matrix)), range(len(car_matrix)))] = 0
    return car_matrix

#Question 2: Car Type Count Calculation
def get_type_count(df):
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_counts = df['car_type'].value_counts().to_dict()
    type_counts = dict(sorted(type_counts.items()))  # Sort by keys alphabetically
    return type_counts

#Question 3: Bus Count Index Retrieval
def get_bus_indexes(df):
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['car'] == 'bus'].index[df['bus'] > 2 * mean_bus].tolist()
    bus_indexes.sort()  # Sort in ascending order
    return bus_indexes

#Question 4: Route Filtering
def filter_routes(df):
    average_truck_values = df.groupby('route')['truck'].mean()
    routes_above_threshold = average_truck_values[average_truck_values > 7].index.tolist()
    routes_above_threshold.sort()  # Sort in ascending order
    return routes_above_threshold

#Question 5: Matrix Value Modification
def multiply_matrix(matrix):
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix

#Question 6: Time Check
def time_check(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    time_check_series = df.groupby(['id', 'id_2'])['timestamp'].agg(lambda x: (x.max() - x.min()).total_seconds() >= 24 * 3600 * 7)
    return time_check_series
