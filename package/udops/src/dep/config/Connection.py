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


    def create_connection(self,host,dbname,user,password):
        config = configparser.ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            with open(dir_path + '/DatabaseConnection.properties', 'r') as f:
                config.read_file(f)
        except FileNotFoundError:
            pass
        
        if 'DatabaseSection' not in config:
            config['DatabaseSection'] = {}
        config['DatabaseSection']['host'] = host
        config['DatabaseSection']['database'] = dbname 
        config['DatabaseSection']['user'] = user
        config['DatabaseSection']['password'] = password
        config['DatabaseSection']['port'] = '5432'

        with open(dir_path + '/DatabaseConnection.properties', 'w') as f:
            config.write(f)
            print(config.get('DatabaseSection','user'))

