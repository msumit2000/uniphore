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

    
            
        
    
    