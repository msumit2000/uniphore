from psycopg2.extras import RealDictCursor
from udops.src.dep.Handler.duplotoken import *


class uiauthentication:

    def authenticate_user(self,username,conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select user_id from udops_users where user_name = '{username}'"
            cursor.execute(query)
            rows = cursor.fetchone()
            conn.commit()
            cursor.close()
            if len(rows) == 0:
                return 0
            else:
                user_id = rows['user_id']
                return user_id
        except Exception as e:
            error = str(e)
            return error

    def authorise_user(self,user_id,corpus_id,access_type,conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select permission from cfg_udops_acl where user_id ={user_id} AND corpus_id={corpus_id};"
            cursor.execute(query)
            rows = cursor.fetchone()
            access = rows['permission']
            if access != access_type:
                return 0
            else:
                return 1
        except Exception as e:
            error = str(e)
            return error

    def authorise_user_clone(self, user_id, corpus_id, conn):

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = f" select permission from cfg_udops_acl where user_id = {user_id} AND corpus_id={corpus_id};"
        cursor.execute(query)
        rows = cursor.fetchone()
        try:
            if rows is None:
                return 0
            else:
                return 1
        except Exception as e:
            error = str(e)
            return error

    def get_user_team(self, team_name,conn):
        try:
            cursor = conn.cursor()
            query = f"select team_id from cfg_udops_teams_metadata where teamname = '{team_name}'"
            cursor.execute(query)
            rows = cursor.fetchone()
            conn.commit()
            cursor.close()
            if rows is not None:
                team_id = rows[0]
                return team_id
            else:
                return 0
        except Exception as e:
            error = str(e)
            return error

    def admin_user(self,team_id,admin_id,conn):
        try:
            cursor = conn.cursor()
            query = f"select * from cfg_udops_teams_admin where team_id = {team_id} AND admin_id = {admin_id}"
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            if len(rows) == 0:
                return 0
            else:
                return 1
        except Exception as e:
            error = str(e)
            return error

    def get_team_location(self, team_name,conn):
        try:
            cursor = conn.cursor()
            query = f"select mount_location, s3_destination_path from cfg_udops_teams_metadata where teamname = '{team_name}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            r1 = rows[0]
            conn.commit()
            cursor.close()
            if rows is not None:
                loc = r1[0]
                return loc
            else:
                return 0
        except Exception as e:
            error = str(e)
            return error

    def corpus_id(self,corpus_name,conn):
        try:
            cursor = conn.cursor()
            query = f"select corpus_id from corpus_metadata where corpus_name = '{corpus_name}'"
            cursor.execute(query)
            rows = cursor.fetchone()
            cid = rows[0]
            conn.commit()
            cursor.close()
            return cid
        except Exception as e:
            error = str(e)
            return error

    def default_access(self, corpus_id, user_id, conn):
        try:
            cursor = conn.cursor()
            query1 = f"select user_name from udops_users where user_id = {user_id};"
            cursor.execute(query1)
            rows = cursor.fetchone()
            username = rows[0]
            p = 'write'
            data = user_id, username, corpus_id, p
            query = f"insert into cfg_udops_acl (user_id,user_name,corpus_id,permission) values (%s,%s,%s,%s);"
            cursor.execute(query, data)
            conn.commit()
            cursor.close()
            return 1
        except Exception as e:
            error = str(e)
            return error

    def Corpus_team_map(self,team_id , corpus_id,conn):
        try:
            cursor = conn.cursor()
            data = team_id,corpus_id
            query = f"insert into cfg_udops_teams_acl (team_id,corpus_id) values (%s,%s);"
            cursor.execute(query,data)
            conn.commit()
            cursor.close()
            return 1
        except Exception as e:
            error = str(e)
            return error

    def change_credentials(self, team_name,conn):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select permanent_access_token from cfg_udops_teams_metadata where teamname = '{team_name}';"
            cursor.execute(query)
            rows = cursor.fetchone()
            duplo_token = rows['permanent_access_token']
            conn.commit()

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select tenant_id from cfg_udops_teams_metadata where teamname = '{team_name}';"
            cursor.execute(query)
            rows = cursor.fetchone()
            tenant = rows['tenant_id']
            conn.commit()
            cursor.close()
            duplo = duplotoken()
            duplo.ChangeToken(tenant, duplo_token)
            duplo.credentials(duplo_token, tenant)

        except Exception as e:
            err = str(e)
            print(err)


