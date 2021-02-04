import yaml
import logging
from logging.config import fileConfig
import pandas as pd
from pathlib import Path
import os.path
import warnings


class Helper(object):

    """
    Provides common ETL functionality
    """

    def __init__(self):
        self.base = self.get_base()
        fileConfig(os.path.join(self.base, "logging.ini"))
        self.logger = logging.getLogger()
        self.conf = self.load_conf()
        self.logger.info("EtlUtils created!")

    def get_base(self) -> str:
        """
        Returns BASE directory for the ETL application
        :return: Base ETL directory
        :rtype: str
        """
        return Path(__file__).parents[1]
    
    def load_conf(self) -> dict:
        """
        Parses configuration yaml file into dictionary.
        :return: Dictionary of configurations
        :rtype: dict
        """
        config = os.path.join(self.base, "config.yml")
        self.logger.info(
            "Start: Loading ETL configuration from {}".format(config))
        with open(config, 'r') as conf_file:
            conf = yaml.load(conf_file, yaml.FullLoader)
        self.logger.info("Finished: Loading ETL configuration")
        return conf

    def get_config(self, config_key) -> dict:
        """
        Return a configuration value (based on a configuration key)
        :param config_key: Configuration key
        :return: Configuration value
        """
        self.logger.info(
            "Start: Getting configuration value for key {}".format(config_key))
        conf_value = self.conf[config_key]
        self.logger.info("Finished: Getting configuration value")
        return conf_value

    def get_data_from_csv(self, file_path: str, separator: str) -> pd.DataFrame:
        """
        Get data from csv and load to dataframe
        :param file_path (str): Full path of csv file
        :return: pd.DataFrame: pandas dataframe
        """
        self.logger.info(
            "Start: Import data to dataframe from csv {}".format(file_path))
        df = pd.read_csv(os.path.join(self.base, file_path), sep=separator)
        self.logger.info("Finished: Imported data to dataframe from csv")
        return df
    
    def convert_to_parquet(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts dataframe into parquet format.
        :param df (pd.Dataframe): pandas dataframe
        :return: pd.DataFrame: pandas dataframe
        """
        self.logger.info(
            "Start: Convert dataframe into parquet format")
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        df.to_parquet(df.name + '_pq.parquet.gzip', compression='gzip')
        df_pq = pd.read_parquet(df.name + '_pq.parquet.gzip')
        self.logger.info("Finished: Converted dataframe into parquet format.")
        return df_pq
    
    