import pandas as pd
import datetime as dt
import configparser
import sys
from pathlib import Path


sys.stdout.reconfigure(line_buffering=True)

config = configparser.ConfigParser()
CONFIG_FILE = Path(__file__).with_name("analysis_config.ini")
config.read(CONFIG_FILE)

class FeatureExtraction:


    def __init__(self):
        self.data_loaded = self.loadData()
        self.cityToState = {
                        'Ahmedabad': 'Gujarat',
                        'Ajmer': 'Rajasthan',
                        'Barwala': 'Haryana',
                        'Bengaluru': 'Karnataka',
                        'Brahmapur': 'Odisha',
                        'Chennai': 'Tamil Nadu',
                        'Delhi': 'Delhi',
                        'E.Godavari': 'Andhra Pradesh',
                        'Hospet': 'Karnataka',
                        'Jabalpur': 'Madhya Pradesh',
                        'Kolkata': 'West Bengal',
                        'Ludhiana': 'Punjab',
                        'Mumbai': 'Maharashtra',
                        'Mysuru': 'Karnataka',
                        'Namakkal': 'Tamil Nadu',
                        'Pune': 'Maharashtra',
                        'Raipur': 'Chhattisgarh',
                        'Surat': 'Gujarat',
                        'Vijayawada': 'Andhra Pradesh',
                        'Vizag': 'Andhra Pradesh',
                        'W.Godavari': 'Andhra Pradesh',
                        'Warangal': 'Telangana',
                        'Allahabad': 'Uttar Pradesh',
                        'Bhopal': 'Madhya Pradesh',
                        'Indore': 'Madhya Pradesh',
                        'Kanpur': 'Uttar Pradesh',
                        'Luknow': 'Uttar Pradesh',
                        'Muzaffurpur': 'Bihar',
                        'Nagpur': 'Maharashtra',
                        'Patna': 'Bihar',
                        'Ranchi': 'Jharkhand',
                        'Varanasi': 'Uttar Pradesh',
                        'Chittoor': 'Andhra Pradesh',
                        'Hyderabad': 'Telangana'
                    }   #form name in state



        # function which make rating on the basis of percentage change of price
    def daily_market_rating(self,change):

        if pd.isna(change):
            return 0

        if change >= 10:
            return 5

        elif change >= 7:
            return 4

        elif change >= 5:
            return 3

        elif change >= 3:
            return 2

        elif change >= 1:
            return 1

        elif change <= -10:
            return -5

        elif change <= -7:
            return -4

        elif change <= -5:
            return -3

        elif change <= -3:
            return -2

        elif change <= -1:
            return -1

        else:
            return 0
        
    
    def loadData(self):
        self.price_df = pd.read_csv(config['PATHS']['egg_price_data_path'])
        self.festival_df = pd.read_csv(config['PATHS']['festivals_data_path'])
        self.weather_df = pd.read_csv(config['PATHS']['weather_data_path'])

        print(f".."*20,f"\nPRICE DATASET SIZE :-",self.price_df.shape,"\nFESTIVAL DATASET SIZE :- ",self.festival_df.shape,"\nWEATHER DATASET SIZE :- ",self.weather_df.shape)
        print(f".."*20,"\n")
        return True

    def priceExtractoinPerCity(self,city):
        if self.data_loaded == True:
            print("Doing feature extraction of price df for city :- ",city)

            # converting date column to date time formate
            price_df = self.price_df
            price_df['Date'] = pd.to_datetime(price_df.Date)
            # removing all extra text from city name
            price_df['City'] = price_df['City'] = price_df['City'].str.split().str[0]

            # getting data for only specific city
            df = price_df[price_df['City']==city]
            df = df.sort_values(['Date'])

            #creating price percentange change on yersterday
            df['daily_change_pct'] = (
                df.groupby('City')['Price']
                .pct_change() * 100
            )

            # creating market rating column on the baisis of percentage change
            df['market_rating'] = (
                df['daily_change_pct']
                .apply(self.daily_market_rating)
            )


            # creating a column of lag of 1 day price
            df['lag_1'] = (
                df.groupby('City')['Price']
                .shift(1)
            )

            # creating a column of lag of 7 day price
            df['lag_7'] = (
                df.groupby('City')['Price']
                .shift(7)
            )

            df = df.sort_values("Date")

            # Rolling Means
            df["rolling_mean_7"] = (
                df["Price"]
                .shift(1)
                .rolling(7)
                .mean()
            )

            df["rolling_mean_14"] = (
                df["Price"]
                .shift(1)
                .rolling(14)
                .mean()
            )

            df["rolling_mean_30"] = (
                df["Price"]
                .shift(1)
                .rolling(30)
                .mean()
            )

            # Rolling Standard Deviation
            df["rolling_std_7"] = (
                df["Price"]
                .shift(1)
                .rolling(7)
                .std()
            )
            
            #creating some day define columns
            df["Date"] = pd.to_datetime(df["Date"])

            df["dayofweek"] = df["Date"].dt.dayofweek
            df["weekofyear"] = df["Date"].dt.isocalendar().week
            df["quarter"] = df["Date"].dt.quarter
            df["is_weekend"] = df["dayofweek"].isin([5,6]).astype(int)

            #creating some more lags column
            df["lag_3"] = df.groupby("City")["Price"].shift(3)
            df["lag_14"] = df.groupby("City")["Price"].shift(14)
            df["lag_30"] = df.groupby("City")["Price"].shift(30)

            self.df = df

            print(f"Feature extraction completed for price df for city {city} and stored in self.df")


        
    def weatherExtractionPerCity(self,city):

        if self.data_loaded == True:

            #getting weather data for sepecific city and converting to state
            df_weather = self.weather_df[
                ['date', 'tmax', 'prcp']
            ][
                self.weather_df['state'] == self.cityToState[city]
            ].copy()
            df_weather['date'] = pd.to_datetime(df_weather.date)

            # Merging of data_barwala and weather_df_Barwala on date 
            self.main_data = self.df.merge(
                df_weather,
                left_on='Date',
                right_on='date',
                how='left'
            )

            # print("MAIN DATA OVERVIEW :- \n",self.main_data.head())
            print(f"WEATHER FEATURE ADDED TO {city} DATA AND DATA IS STORED AFTER MERGE IN self.main_data")

    
    def festivalExtractionPerCity(self,city):

        if self.data_loaded == True:

            # converting data and extracting some feature
            festival_df = self.festival_df[
                ['Date', 'festival_name']
            ].copy()
            festival_df['Date'] = pd.to_datetime(festival_df.Date)
            festival_df["is_festival"] = festival_df["festival_name"].notna().astype(int)

            #merging festival on dates
            # Merging of price_df and festival_df on date 
            self.main_data = self.main_data.merge(
                festival_df,
                on='Date',
                how='left'
            )
            

            print(f"FESTIVAL DATA EXTRACTION COMPLETED FOR CITY {city} and FULL DATABASE IS SOTERD IN self.main_data")


    def storeToCsv(self, city):

        if self.data_loaded == True:

            file_path = (f"{config['STORE']['path']}\{city}_main_data.csv")

            self.main_data.to_csv(
                file_path,
                index=False
            )

            print(f"{city} data stored successfully!\n")




if __name__=='__main__':
    cities = [city.strip() for city in config['CITY']['city'].split(",") if city.strip()]
    model = FeatureExtraction()
    for city in cities:
        model.priceExtractoinPerCity(city=city)
        model.weatherExtractionPerCity(city=city)
        model.festivalExtractionPerCity(city=city)
        model.storeToCsv(city=city)
