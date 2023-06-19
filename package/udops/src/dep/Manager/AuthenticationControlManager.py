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
                query  = f"select user_id from udops_users where user_name = '{username}'"
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
                return 0
        except Exception as e:
            print(e)

    def corpus_id(self,corpus_name,conn):
        try:
            cursor = conn.cursor()
            query = f"select corpus_id from corpus_metadata where corpus_name = '{corpus_name}'"
            cursor.execute(query)
            rows = cursor.fetchone()
            cid = rows[0]
            return cid
        except Exception as e:
            print(e)

    def default_access(self,corpus_id,user_id,conn):
        try:
            cursor = conn.cursor()
            
            query1 = f"select user_name from udops_users where user_id = {user_id};"
            cursor.execute(query1)
            rows = cursor.fetchone()
            username = rows[0]
            p = 'write'
            data = user_id,username,corpus_id,p
            query = f"insert into cfg_udops_acl (user_id,user_name,corpus_id,permission) values (%s,%s,%s,%s);"
            cursor.execute(query,data)
            conn.commit()
            cursor.close()
        except Exception as e:
            print(e)

    def Corpus_team_map(self,team_id , corpus_id,conn):
        try:
            cursor = conn.cursor()
            data = team_id,corpus_id
            query = f"insert into cfg_udops_teams_acl (team_id,corpus_id) values (%s,%s);"
            cursor.execute(query,data)
            conn.commit()
            cursor.close()
        except Exception as e:
            print(e)




