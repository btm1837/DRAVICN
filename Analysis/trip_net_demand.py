import pandas as pd
import os

def get_trip_net_demand_df(data,path):
    df=pd.DataFrame.from_dict(data=data.trip_net_demand,orient='columns')
    df=df.reset_index()
    df.columns = ['name','net_demand']
    df['arc'], df['trip_name'] = zip(*df.name)
    df.to_csv(os.path.join(path,'trip_net_demand.csv'))
    return