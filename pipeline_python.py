import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy as sqa

np.random.seed(42)
numofrecords = 25000

hubs = {
    'hub_id':['HUB-US-EAST', 'HUB-US-WEST', 'HUB-US-CENTRAL', 'HUB-US-SOUTH'],
    'hub_lat':[40.7128, 37.7749, 41.8781, 29.7604],
    'hub_lon':[-74.0060, -122.4194, -87.6298, -95.3698],
    'hub_region':['East', 'West', 'Mid-West', 'South']
}

df_hubs = pd.DataFrame(hubs)

start_date = dt.datetime(2026, 1, 1)
order_dates = [start_date + dt.timedelta(days = int(np.random.randint(0, 90)), hours = int(np.random.randint(0, 24)), minutes = int(np.random.randint(0, 60))) for _ in range(numofrecords)]

assigned_hubs = np.random.choice(df_hubs.hub_id, size = numofrecords)

order_types = np.random.choice(['Standard', 'Express', 'Next-day'], size = numofrecords, p = [0.6, 0.3, 0.1])
item_weights = np.round(np.random.exponential(scale = 5.0, size = numofrecords) + 0.5, 2)

item_weights[np.random.choice(numofrecords, size = 50)] = -10.00

cust_lats = np.random.uniform(25.0, 49.0, size = numofrecords)
cust_lons = np.random.uniform(-125.0, -70.0, size = numofrecords)

df_orders = pd.DataFrame(
    {
        'order_id':[f'ORD-{100000 + v}' for v in range(numofrecords)],
        'order_timestamp':order_dates,
        'hub_id': assigned_hubs,
        'shipping_tier':order_types,
        'item_weight_lbs':item_weights,
        'dest_lat':cust_lats,
        'dest_lon':cust_lons,
        'base_carrier_cost':np.round(np.random.uniform(5.0, 45.0, size = numofrecords), 2)
    }
)


df_pipeline = pd.merge(df_orders, df_hubs, on = 'hub_id', how = 'left')

def haversine_distance(lat1:float, lon1:float, lat2:float, lon2:float)-> float:
    r = 3958.8
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return r * c

df_pipeline['route_distance_miles'] = haversine_distance(df_pipeline['hub_lat'], df_pipeline['hub_lon'], df_pipeline['dest_lat'], df_pipeline['dest_lon'])

#Clean data
df_pipeline = df_pipeline[df_pipeline.item_weight_lbs > 0]

engine = sqa.create_engine('postgresql+psycopg2://postgres:vincent23@localhost:5432/enterprise_supply_chain_routing_audit')

with engine.connect() as connection:
    df_pipeline.to_sql('orders', con = connection, index = 'False', if_exists = 'replace')
    print('Connection (orders) opened successfully')

hub_points = df_pipeline[['order_id', 'hub_lat', 'hub_lon', 'route_distance_miles']].rename(columns = {'hub_lat':'latitude', 'hub_lon':'longitude'})
hub_points['point_type'] = 'Hub'
hub_points['point_order'] = 1

dest_points = df_pipeline[['order_id', 'dest_lat', 'dest_lon', 'route_distance_miles']].rename(columns = {'dest_lat':'latitude', 'dest_lon':'longitude'})
dest_points['point_type'] = 'Destination'
dest_points['point_order'] = 2

df_powerbi_map = pd.concat([hub_points, dest_points]).sort_values(by = ['order_id', 'point_order'])

with engine.connect() as connection:
    df_powerbi_map.to_sql('fact_map_routes', con = connection, index = False, if_exists = 'replace')
    print("Connection (fact_map_routes) opened successfully")
