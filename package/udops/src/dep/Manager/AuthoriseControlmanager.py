import psycopg2
from psycopg2.extras import RealDictCursor

class udops_authorise:
    def authorise_user_clone(self,user_id,corpus_id,conn):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = f"select permission from cfg_udops_acl where user_id ={user_id} AND corpus_id={corpus_id};"
        cursor.execute(query)
        rows = cursor.fetchone()
        try: 
            access = rows['permission']
            if access == 'read' or access == 'write':
                return 1
            else:
                return 2
        except Exception as e:
            raise(e)
            print(" User not given access to this corpus")
        
    def authorise_user(self,user_id,corpus_id,access_type,conn):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = f"select permission from cfg_udops_acl where user_id ={user_id} AND corpus_id={corpus_id};"
        cursor.execute(query)
        rows = cursor.fetchone()
        access = rows['permission']
        if access != access_type:
            print("ACCESS DENY")
        else:
            return 1 

    def update_user_access(self, username, new_access_type,conn):
        try:
            cursor = conn.cursor()
            query = f"UPDATE git_access SET access = '{new_access_type}' WHERE username = '{username}'"
            cursor.execute(query)
            conn.commit()
            print(f"Access type updated successfully for user '{username}'")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
