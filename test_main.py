'''Test suite for main.py  
Usage:
    CLI: python3 -m unittest test_main.py 
'''

import unittest
from unittest.mock import patch
import pandas as pd
import main
import os
from utils.helper import Helper
import logging

    
class TestMain(unittest.TestCase):
    # pass

    @classmethod
    def setUpClass(cls):
        logging.info('setUpClass')
        # define in-memory mock data for the weather files
        cls.mock_weather_df = pd.DataFrame ( 
                    { 'ForecastSiteCode': ['','','','',''],
                      'ObservationTime': ['','','','',''],
                      'ObservationDate': ['2016-02-01',
                                          '2016-02-01',
                                          '2016-02-01',
                                          '2016-02-01',
                                          '2016-02-01'],
                      'WindDirection': ['','','','',''],
                      'WindSpeed': ['','','','',''],
                      'WindGust': ['','','','',''],
                      'Visibility': ['','','','',''],
                      'ScreenTemperature': 
                        ['2.1','0.1','2.8','1.6','9.8'],
                      'Pressure': ['','','','',''],
                      'SignificantWeatherCode': ['','','','',''],
                      'SiteName': ['','','','',''],
                      'Latitude': ['60.7490','40.7490','30.7490','20.7490',''],
                      'Longitude': ['-1.8540','-2.8540','-0.8540','-0.1854',''],
                       'Region':
                        ['Orkney & Shetland',
                        'Orkney & Shetland',
                        'Orkney & Shetland',
                        'Orkney & Shetland',
                        'Highland & Eilean Siar'],
                       'Country': ['SCOTLAND','SCOTLAND','SCOTLAND','SCOTLAND','']} )
        cls.mock_weather_df['ObservationDate'] = pd.to_datetime(cls.mock_weather_df['ObservationDate'])
        cls.mock_weather_df['ScreenTemperature'] = cls.mock_weather_df['ScreenTemperature'].astype('float64')
        # create utils helper object
        helper = Helper()
        cls.configs ={'file1': 'weather.20160201.csv', 'file2': 'weather.20160301.csv', 'path': 'raw_data/', 'separator': ','}
        cls.weather_data_df = main.get_data(helper, cls.configs)
    
    @classmethod
    def tearDownClass(cls):
        logging.info('tearDownClass')

    def setUp(self):
        logging.info('setUp')
        self.file_paths = [os.path.join(os.path.dirname(__file__), 'raw_data/weather.20160201.csv') \
                         , os.path.join(os.path.dirname(__file__), 'raw_data/weather.20160301.csv')]
        self.mock_df_max_temp = self.mock_weather_df['ScreenTemperature'].max()
        self.mock_df_empty_dates = self.mock_weather_df['ObservationDate'].isnull().values.any()
        self.hottest_day_row = self.mock_weather_df[self.mock_weather_df['ScreenTemperature'] == \
                                            self.mock_weather_df['ScreenTemperature'].max()]
    
    def tearDown(self):
        logging.info('tearDown\n')
    
    
    def test_that_source_files_exist(self):
        logging.info('test_the_existence_of_main.20160201.csv_and_main.20160301.csv_source_files')
        self.assertEqual(self.file_paths[0], os.path.join(os.path.dirname(__file__),self.configs['path'] +  self.configs['file1']))        
        self.assertEqual(self.file_paths[1], os.path.join(os.path.dirname(__file__),self.configs['path'] +  self.configs['file2']))
        self.assertNotEqual(self.file_paths[0], self.file_paths[1])


    def empty_df_except(self):
        ''' Function that helps to mock exception for empty dataframes '''
        if self.mock_weather_df.empty:
            raise TypeError('Empty dataframe. Review source files')
        else:
            return True
    
    def test_for_empty_dataframe(self):
        logging.info('test_mock_for_empty_dataframe')
        self.assertRaises(TypeError, self.empty_df_except())            
    
    
    def test_max_temperature_function(self):
        logging.info('test_that_max_temperature_function_returns_the_maximum_ScreenTemperature_value')
        self.assertEqual(self.mock_df_max_temp, 9.8)
    
    def test_dates_not_empty(self):
        logging.info('test_that_date_column_not_empty_returns_true_if_found_empty')
        self.assertFalse(self.mock_df_empty_dates)
    
    def test_get_hottest_day(self):
        logging.info('test_get_hottest_day_returns_hottest_day')
        hot_date = main.get_hottest_day(self.hottest_day_row).values[0]
        self.assertEqual(hot_date,'2016-02-01')
    
    def test_get_temp_on_hottest_day(self):
        logging.info('test_get_temp_on_hottest_day_returns_hottest_day')
        highest_temp = main.get_temp_on_hottest_day(self.hottest_day_row).values[0]
        self.assertEqual(highest_temp,9.8)
    
    def test_get_region_of_hottest_day(self):
        logging.info('test_get_region_of_hottest_day_returns_region')
        hot_region = main.get_region_of_hottest_day(self.hottest_day_row).values[0]
        self.assertEqual(hot_region,'Highland & Eilean Siar')

if __name__=='__main__':
    unittest.main()