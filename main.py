"""DocString main.py
    Module for Feb, March 2016 weather analysis.
            
        Hottest date: '2016-03-17' 
        Temperature: '15.8' 
        Region: 'Highland & Eilean Siar'
    Usage:
        cli: python3 main.py   
"""

import logging
import pandas as pd
from utils.helper import Helper


def main():
    """[summary]
    Gets job parameters from config file and
    run all jobs that are mentioned in config file.
    Currently only one job is configured and more can be added
    as and when required by making few or no changes depending
    on the requirements
    """    
    try:
        # create utils helper object
        helper = Helper()
        # get job parameters from config file
        configs = helper.get_config('weather_test')
        weather_df = get_data(helper, configs)
        weather_df_pq = helper.convert_to_parquet(weather_df)
        hottest_day_row = weather_df_pq[weather_df_pq['ScreenTemperature'] == \
        weather_df_pq['ScreenTemperature'].max()]
        get_hottest_day(hottest_day_row)
        get_temp_on_hottest_day(hottest_day_row)
        get_region_of_hottest_day(hottest_day_row)
    except Exception as e:
        logging.error(e)


def get_data(helper: Helper, params) -> None:
    try:
        weather_data_df1 = helper.get_data_from_csv(params['path']+ params['file1'], params['separator'])
        weather_data_df2 = helper.get_data_from_csv(params['path']+ params['file2'], params['separator'])
        weather_df = weather_data_df1.append(weather_data_df2)
        weather_df[['WindGust', 'Visibility', 'Pressure']] = weather_df[['WindGust', 'Visibility', 'Pressure']].fillna(0)
        weather_df['Country'] = weather_df['Country'].fillna('')
        weather_df.name='weather_df'
        return weather_df
    except Exception as e:
        logging.error(e)


def get_hottest_day(hottest_day_row):
    """Gets date of the hottest day"
    Helper    
        help(main.get_hottest_day)
    """
    try:
        hottest_day = hottest_day_row.iloc[:,2].map(lambda x: str(x)[:-9])
        logging.info("Date of the hottest day: {}".format(hottest_day.values))
        return hottest_day
    except Exception as e:
        logging.error(e)


def get_temp_on_hottest_day(hottest_day_row):
    """Gets the temperature on the hottest day"
    Helper    
        help(main.get_temp_on_hottest_day)
    """
    try:
        temp_on_hottest_day = hottest_day_row.iloc[:,7]
        logging.info("Temperature on hottest day: {}".format(temp_on_hottest_day.values))
        return temp_on_hottest_day
    except Exception as e:
        logging.error(e)


def get_region_of_hottest_day(hottest_day_row):
    """Gets region of the hottest day"
    Helper    
        help(main.get_region_of_hottest_day)
    """
    try: 
        hottest_day_region = hottest_day_row.iloc[:,13]
        logging.info("Region of hottest day: {}".format(hottest_day_region.values))
        return hottest_day_region
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()