from psycopg2.extras import RealDictCursor
import requests
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
from udops.src.dep.Handler.duplotoken import *
import configparser
import os

duplo = duplotoken()
prop = properties()
connection = Connection()
conn = connection.get_connection()
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'udops_config')


class teamusermanager:
    def team_authentication(self,username,team_name):
        print("##########################################")
        print("Duplo authentication")
        directory = file_path
        print(f"directory-->  {directory}")

        config = configparser.ConfigParser()
        config.read(directory)

        if 'github' not in config:
            config.add_section('github')
        config.set('github', 'team_name', team_name)
        with open(directory, 'w') as config_file:
            config.write(config_file)

        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = (f"select exists (select user_id, team_id from cfg_udops_users "
                 f"where user_id = ( select user_id from udops_users where user_name = '{username}' ) "
                 f"and team_id = ( select team_id from cfg_udops_teams_metadata where teamname = '{team_name}'));")
        cursor.execute(query)
        rows = cursor.fetchone()
        user_team_exist = rows['exists']
        conn.commit()

        if user_team_exist:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select permanent_access_token from cfg_udops_teams_metadata where teamname = '{team_name}';"
            cursor.execute(query)
            rows = cursor.fetchone()
            duplo_token = rows['permanent_access_token']
            print(f"duplo_token--> {duplo_token}")
            conn.commit()

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select tenant_id from cfg_udops_teams_metadata where teamname = '{team_name}';"
            cursor.execute(query)
            rows = cursor.fetchone()
            tenant = rows['tenant_id']
            print(f"tenant--> {tenant}")
            conn.commit()
            cursor.close()
            duplo.ChangeToken(tenant,duplo_token)
        else:
            print('User not mapped in the selected team')

    def get_s3_path(self):
        directory = os.path.join(dir_path,file_path)        
        config = configparser.ConfigParser()
        config.read(directory)
        team = config.get('github','team_name')
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("select team_id from cfg_udops_teams_metadata where teamname = '{}';".format(team))
        git_token = config.get('github','access_token')
        url = 'https://api.github.com/user'
        headers = {'Authorization': f'token {git_token}'}
        response = requests.get(url, headers=headers)
        github_username = response.json()['login']
        cursor.execute("select user_id from cfg_udops_users where user_name = '{}' and team_id = (select team_id from cfg_udops_teams_metadata where teamname = '{}');".format(github_username,team))
        rows2 = cursor.fetchone()
        if rows2 != '':
            cursor.execute("select s3_base_path from cfg_udops_teams_metadata where teamname = '{}';".format(team))
            s3 = cursor.fetchone()
            return s3['s3_base_path']
        else: 
            raise('User doesnt have permission for the team')
