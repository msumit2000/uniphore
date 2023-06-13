import requests
from psycopg2.extras import RealDictCursor

class udpos_authentication:
    def authenticate_user(self,ACCESS_TOKEN,conn):
        try:
            url = 'https://api.github.com/user'
            headers = {'Authorization': f'token {ACCESS_TOKEN}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                username = response.json()['login']
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                query  = f"select user_id from cfg_udops_acl where user_name = '{username}'"
                cursor.execute(query)
                rows = cursor.fetchone()
                user_id = rows['user_id']
                conn.commit()
                return user_id
            else:
                return 0 
        except Exception as e:
            print(e)

    def get_user_team(self, user_id_,conn):
        try:
            cursor = conn.cursor()
            query = f"select team_id from cfg_udops_users where user_id = '{user_id_}'"
            cursor.execute(query)
            rows = cursor.fetchone()
            if rows is not None:
               team_id = rows[0]
               conn.commit()

               return team_id
            else:
                return 1
        except Exception as e:
            print(e)




