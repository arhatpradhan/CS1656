import os
import pandas as pd
import datetime
import numpy as np

class Calculations:
    def __init__(self, files):
        self.trips = self.produce_trips_table(files)
        self.daily_counts = self.calculate_daily_counts(self.get_trips())
        self.monthly_counts = self.calculate_monthly_counts(self.get_trips())
    
    def get_trips(self):
        return self.trips

    def get_daily_counts(self):
        return self.daily_counts

    def get_monthly_counts(self):
        return self.monthly_counts

    def produce_trips_table(self, files):
        # DataFrame must have at least the 'Bikeid', 'Starttime', 'Trip id', 'From station id', 'To station id' columns
        # create an empty list to store the individual trip DataFrames to combine for later
        trips_list = []

        # iterate over the input files
        for file in files:
            # read in the CSV file as a DataFrame
            df = pd.read_csv(file, usecols=["Bikeid", "Starttime", "From station id", "To station id"])
            # convert the Starttime column to a datetime object
            df["Starttime"] = pd.to_datetime(df["Starttime"])
            # append the DataFrame to the trips list
            trips_list.append(df)

        # concatenate all the trip DataFrames into a single DataFrame
        trips = pd.concat(trips_list)
        return trips
    
    def calculate_daily_counts(self, trips):
        # DataFrame must have "Starttime", "From station id", "To station id" and "Bikeid" columns

        # Calculate day column from Starttime column
        trips['day'] = trips['Starttime'].dt.strftime('%m/%d/%Y')

        # Calculate fromCNT
        from_counts = trips.groupby(['day', 'From station id']).count().reset_index()[['day', 'From station id', 'Starttime']]
        from_counts = from_counts.rename(columns={'From station id': 'station_id', 'Starttime': 'fromCNT'})

        # Calculate toCNT
        to_counts = trips.groupby(['day', 'To station id']).count().reset_index()[['day', 'To station id', 'Starttime']]
        to_counts = to_counts.rename(columns={'To station id': 'station_id', 'Starttime': 'toCNT'})

        # Merge from_counts and to_counts DataFrames
        daily_counts = from_counts.merge(to_counts, how='outer', on=['day', 'station_id']).fillna(0)

        # Calculate rebalCNT
        daily_counts['rebalCNT'] = abs(daily_counts['fromCNT'] - daily_counts['toCNT'])

        # Format columns
        daily_counts['station_id'] = daily_counts['station_id'].astype(int)
        daily_counts['day'] = pd.to_datetime(daily_counts['day'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')

        # Rearrange columns
        daily_counts = daily_counts[['day', 'station_id', 'fromCNT', 'toCNT', 'rebalCNT']]

        daily_counts['fromCNT'] = daily_counts['fromCNT'].astype(int)
        daily_counts['toCNT'] = daily_counts['toCNT'].astype(int)
        daily_counts['rebalCNT'] = daily_counts['rebalCNT'].astype(int)
        return daily_counts
    
    def calculate_monthly_counts(self, trips):
        df_daily = Calculations.get_daily_counts(self)
        # Convert the 'day' column to datetime format
        df_monthly = df_daily.copy()
        df_monthly['day'] = pd.to_datetime(df_monthly['day'], format='%m/%d/%Y')

        # Group the daily counts by month and station_id, and sum the counts for each group
        df_monthly = df_monthly.groupby([pd.Grouper(key='day', freq='M'), 'station_id']).sum().reset_index()

        # Rename the 'day' column to 'month'
        df_monthly = df_monthly.rename(columns={'day': 'month'})

        # Convert the 'month' column to string format
        df_monthly['month'] = df_monthly['month'].dt.strftime('%m/%Y')

        
        return df_monthly
        
if __name__ == "__main__":
    calculations = Calculations(['HealthyRideRentals2021-Q1.csv', 'HealthyRideRentals2021-Q2.csv', 'HealthyRideRentals2021-Q3.csv'])
    print("-------------- Daily Counts ---------------")
    print(calculations.get_daily_counts())
    print()
    print("------------- Monthly Counts---------------")
    print(calculations.get_monthly_counts())
    print()