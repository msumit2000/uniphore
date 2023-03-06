import configparser
import psycopg2
import os

class Connection:
    def get_connection(self):
        try:
            config = configparser.RawConfigParser()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            configpath = dir_path + "/DatabaseConnection.properties"
            config.read(configpath)
            conn = psycopg2.connect(database=config.get('DatabaseSection', 'database'),
                                    user=config.get('DatabaseSection', 'user'),
                                    password=config.get('DatabaseSection', 'password'),
                                    host=config.get('DatabaseSection', 'host'),
                                    port=config.get('DatabaseSection', 'port'))
            return conn
        except Exception as e:
            raise e
