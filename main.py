# Author: Roberto Barroso García
# Date: 2021

# Imports
import pandas as pd
import argparse as argp
import sys


# Function definition
def calculate(args):
    # Read trips data
    yellow_trip_df = pd.read_csv(args.t,
                                 usecols=['trip_distance', 'DOLocationID'])
    # Read Zones data
    zone_lookup_df = pd.read_csv(args.z,
                                 usecols=['LocationID', 'Borough', 'Zone'])
    # Calculate the percentile
    perc95 = yellow_trip_df.trip_distance.quantile(args.q)

    # Filter trips with distance above the percentile
    trips_df = yellow_trip_df[yellow_trip_df['trip_distance'] > perc95]

    # Retrieve Drop off locations ordered by number of trips that fulfil the requirement
    result_df = pd.DataFrame(trips_df["DOLocationID"].value_counts().head(10).reset_index().values,
                             columns=["DOLocationID", "trips"])
    result_df = result_df.rename(columns={'DOLocationID': 'LocationID'})  # Rename column to match the keys
    result_df = result_df.join(zone_lookup_df.set_index('LocationID'),
                               on='LocationID')  # Join two tables by key:LocationID
    result_df = result_df.drop(['LocationID'], axis=1)  # Drop the column of Ids
    result_df = result_df.rename(columns={'Borough': 'end_borough', 'Zone': 'end_zone'})  # Rename columns

    return result_df


# Introducing arguments
parser = argp.ArgumentParser(description='Process some data.')  # Creating parser
parser.add_argument('--q', type=float, default=0.95, help='Quantile, choose a number between 0 and 1')
parser.add_argument('--t', type=str, default='https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2021-07.csv',
                    help='url of trips data source')
parser.add_argument('--z', type=str, default='https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv',
                    help='url of zones data source')
args = parser.parse_args()

sys.stdout.write(str(calculate(args)))
