from psycopg2.extras import RealDictCursor
import requests
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
from udops.src.dep.Handler.duplotoken  import *
duplo = duplotoken()
prop=properties()
connection = Connection()
conn = connection.get_connection()
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'udops_config')
import configparser
import os

class teamusermanager:
    def team_authentication(username,team_name):
        
        directory = os.path.join(dir_path,file_path)        
        config = configparser.ConfigParser()
        config.read(directory)

        if 'github' not in config:
            config.add_section('github')
        config.set('github', 'team_name', team)
        with open(directory, 'w') as config_file:
            config.write(config_file)
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = f"select exists (select user_id, team_id from cfg_udops_users where user_id = ( select user_id from udops_users where user_name = '{username}' ) and team_id = ( select team_id from cfg_udops_teams_metadata where teamname = '{team_name}'));"
        cursor.execute(query)
        rows = cursor.fetchone()
        user_team_exist = rows['exists']
        conn.commit()

        if user_team_exist == 't':
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query  = f"select permanent_access_token from cfg_udops_teams_metadata where teamname = {team_name};"
            cursor.execute(query)
            rows = cursor.fetchone()
            duplo_token = rows['permanent_access_token']
            conn.commit()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query  = f"select tenant_id from cfg_udops_teams_metadata where teamname = {team_name};"
            cursor.execute(query)
            rows = cursor.fetchone()
            tenant = rows['tenant_id']
            conn.commit()
            duplo.ChangeToken(tenant,duplo_token)


        

        

                
