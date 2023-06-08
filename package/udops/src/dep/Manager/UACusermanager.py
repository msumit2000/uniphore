from udops.src.dep.Common.Constants import Constants
from psycopg2.extras import RealDictCursor
import requests
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
prop=properties()
connection = Connection()
conn = connection.get_connection()

class uacusermanager:
    def list_users(self):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Constants.Udops_User_list)
        rows = cursor.fetchall()
        conn.commit()
        return rows
    
    def upsert_user(self,username,firstname,lastname,email):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Constants.Udops_users_select + username + "'")
        rows = cursor.fetchone()

        if rows != '':
            data = username , firstname,lastname, email
            cursor.execute(Constants.Udops_users_update + data + username + "'")
        else :
            data = username , firstname,lastname, email
            cursor.execute(Constants.Udops_users_insert + data)

    def upsert_team(self , teamname , permanent_access_token , tenant_id , admin_user_id , s3_base_path ):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('select team_id from cfg_udops_teams_metadata where teamname = "{teamname}"')

        rows = cursor.fetchone()

        if rows != '':
            cursor.execute('insert into cfg_udops_teams_metadata (teamname, permanent_access_token, tenant_id,admin_user_id,s3_base_path) values ("{teamname}","{permanent_access_token}","{tenant_id}","{admin_user_id}","{s3_base_path}");')
        else:
            cursor.execute('update cfg_udops_teams_metadata set teamname = "{teamname}" , permanent_access_token = "{permanent_access_token}", tenant_id = "{tenant_id}", admin_user_id = "{admin_user_id}", s3_base_path = "{s3_base_path}" where team_id = {rows};')

    
            
        
    
    