from psycopg2.extras import RealDictCursor
import requests
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
from udops.src.dep.Manager.mount_s3 import *

prop = properties()
connection = Connection()
mount = mount_s3()


class UserManagementManager:
    ########################### User Management #######################

    def get_user_list(self):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT user_name,firstname,lastname,email FROM udops_users")
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            return rows
        except Exception as e:
            print(e)

    def update_user(self, firstname, lastname, email, existing_user_name, new_user_name):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"UPDATE udops_users SET firstname = '{firstname}', lastname = '{lastname}', email = '{email}', user_name='{new_user_name}' where user_name ='{existing_user_name}';"
            cursor.execute(query)
            if cursor.rowcount == 0:
                return 2
            else:
                conn.commit()
                cursor.close()
                return 1
        except Exception as e:
            raise e

    def get_team_list(self):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # query = f"""SELECT t.teamname,t.permanent_access_token,t.tenant_id,t.admin_user_id,t.s3_base_path, ARRAY(SELECT user_name FROM cfg_udops_users WHERE team_id = t.team_id) AS users FROM cfg_udops_teams_metadata AS t;"""
            query = f"""    
                            SELECT
                            t.teamname,
                            t.permanent_access_token,
                            t.tenant_id,
                            (SELECT ARRAY_AGG(user_name) FROM udops_users WHERE user_id IN (
                                SELECT admin_id FROM cfg_udops_teams_admin WHERE team_id = t.team_id
                            )) AS admin_user_names,
                            t.s3_base_path,
                            t.s3_destination_path,
                            ARRAY(
                                SELECT user_name FROM cfg_udops_users WHERE team_id = t.team_id
                            ) AS users
                            FROM
                            cfg_udops_teams_metadata AS t;
                    """

            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            #  conn.close()
            return rows
        except Exception as e:
            print(e)

    def update_team(self, permanent_access_token, tenant_id, s3_base_path, destination_base_path,existing_teamname,
                    new_teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = (f" UPDATE cfg_udops_teams_metadata SET permanent_access_token = '{permanent_access_token}',"
                     f" tenant_id = '{tenant_id}', s3_base_path = '{s3_base_path}', "
                     f" s3_destination_path = '{destination_base_path}',"
                     f" teamname = '{new_teamname}' WHERE teamname = '{existing_teamname}';")
            cursor.execute(query)

            if cursor.rowcount == 0:
                return "existing_teamname not found!!!"
            else:
                conn.commit()
                cursor.close()
                return "Update successful!!!"
        except Exception as e:
            raise e

    def remove_admin(self,user_name,teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query1 = f"select team_id from cfg_udops_teams_metadata where teamname ='{teamname}'"
            cursor.execute(query1)
            row1 = cursor.fetchone()

            if row1 is None:
                return 0
            else:
                team_id = row1['team_id']
                query = f"select user_id from udops_users where user_name= '{user_name}' "
                cursor.execute(query)
                row = cursor.fetchone()
                admin_id = row['user_id']
                query3 = f"DELETE from cfg_udops_teams_admin where team_id = {team_id} AND admin_id = {admin_id}"
                cursor.execute(query3)
                conn.commit()
                cursor.close()
                return 1
        except Exception as e:
            error = str(e)
            return error
        
    def list_admin(self, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select team_id from cfg_udops_teams_metadata where teamname='{teamname}'"
            cursor.execute(query)
            row = cursor.fetchone()
            team_id = row['team_id']

            query1 = f"select admin_id from cfg_udops_teams_admin where team_id = {team_id}"
            cursor.execute(query1)
            ro1 = cursor.fetchall()
            admin_ids = [row.get('admin_id') for row in ro1]

            admin_name = []
            for id1 in admin_ids:
                query2 = f"select user_name from udops_users where user_id = {id1} "
                cursor.execute(query2)
                row = cursor.fetchone()
                name = row['user_name']
                admin_name.append(name)

            return admin_name

        except Exception as e:
            err = str(e)
            return err

    def update_admin(self, username, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            userid = []
            for user in username:
                q = f"select user_id from udops_users where user_name = '{user}'"
                cursor.execute(q)
                row = cursor.fetchone()
                user_id = row['user_id']
                userid.append(user_id)



            # team_id respective to team
            query = f"select team_id, tenant_id from cfg_udops_teams_metadata where teamname = '{teamname}'"
            cursor.execute(query)
            row = cursor.fetchall()
            team_id = row[0]['team_id']
            tenant_id = row[0]['tenant_id']
            print("!!!!!!!!!!!!!!!!!1")
            print(team_id)
            print(tenant_id)

            # fetching admin_id with respect to given team
            que1 = f"select admin_id from cfg_udops_teams_admin where team_id = {team_id}"
            cursor.execute(que1)
            ro1 = cursor.fetchall()
            if len(ro1) == 0:
                for id2 in userid:
                    que2 = f"select user_name from udops_users where user_id = {id2}"
                    cursor.execute(que2)
                    ro2 = cursor.fetchone()
                    print(f"ro2--->{ro2}")
                    user_name = ro2['user_name']
                    print("@@@@@@@@@@@@@@@@@@@@")
                    print(user_name)

                    que3 = f"insert into cfg_udops_teams_admin (team_id, admin_id) VALUES ({team_id},{id2})"
                    cursor.execute(que3)
                    query = f"INSERT INTO cfg_udops_users(user_id,user_name,team_id,tenant_id) VALUES ({id2},'{user_name}',{team_id},'{tenant_id}')"
                    cursor.execute(query)
                conn.commit()
                cursor.close()
                return 1

            else:
                admin_ids = [row.get('admin_id') for row in ro1]

            # check weather admin_id is present in user_id array.
                array1 = []
                for id1 in userid:
                    if id1 in admin_ids:
                        array1.append(id1)
                    else:
                        query2 = f"insert into cfg_udops_teams_admin (team_id, admin_id) VALUES ({team_id},{id1})"
                        cursor.execute(query2)

                array2 = []
                if len(array1) == 0:
                    conn.commit()
                    cursor.close()
                    return 1
                else:
                    for id2 in array1:
                        q2 = f"select user_name from udops_users where user_id = {id2}"
                        cursor.execute(q2)
                        row1 = cursor.fetchone()
                        name = row1['user_name']
                        array2.append(name)
                conn.commit()
                cursor.close()
                return array2

        except Exception as e:
            error = str(e)
            return error

    def add_users_team(self, user_name, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query1 = f"SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}'"
            cursor.execute(query1)
            team = cursor.fetchone()
            team_id = team['team_id']

            query = f"SELECT  user_name FROM cfg_udops_users WHERE team_id = {team_id}"
            cursor.execute(query)
            rows = cursor.fetchall()

            values = [list(row.values())[0] for row in rows]

            if user_name in values:
                return 1
            else:
                # Check if the user_name exists in the udops_users table
                check_query = f"SELECT user_id, user_name FROM udops_users WHERE user_name = '{user_name}'"
                cursor.execute(check_query)
                rows = cursor.fetchall()

                if len(rows) == 0:
                    # User not present in udops_users table, raise an error
                    cursor.close()
                    conn.commit()
                    return "Invalid Username!!!!"
                else:
                    # Insert the new user into cfg_udops_users table
                    user_id = rows[0]['user_id']
                    query1 = f"SELECT team_id,tenant_id FROM cfg_udops_teams_metadata  WHERE teamname = '{teamname}'"
                    cursor.execute(query1)
                    rows1 = cursor.fetchall()
                    if len(rows1) == 0:
                        conn.commit()
                        cursor.close()
                        return "Invalid teamname!!!"
                    else:
                        team_id = rows1[0]['team_id']
                        tenant_id = rows1[0]['tenant_id']
                        query = f"INSERT INTO cfg_udops_users(user_id,user_name,team_id,tenant_id) VALUES ({user_id},'{user_name}',{team_id},'{tenant_id}')"
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        return "User added successfully !!!"

        except Exception as e:
            error = str(e)
            return error

    def delete_user(self, user_name, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"DELETE FROM cfg_udops_users WHERE user_name = '{user_name}' AND team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}')"

            cursor.execute(query)
            if cursor.rowcount == 0:
                return 2
            else:
                conn.commit()
                cursor.close()
                return 1
        except Exception as e:
            raise e

    def grant_access_corpus(self, user_name, corpus_name, permission):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # Get the corpus_id based on the corpus_name
            cursor.execute("SELECT corpus_id FROM corpus_metadata WHERE corpus_name = %s;", [corpus_name])
            corpus = cursor.fetchone()
            corpus_id = corpus['corpus_id']

            for user_names in user_name:
                # Check if the user exists based on the user_name
                cursor.execute("SELECT user_id FROM udops_users WHERE user_name = %s;", [user_names])
                user = cursor.fetchone()
                user_id = user['user_id']

                # Check if the user and corpus already have a permission record in cfg_udops_acl
                cursor.execute("SELECT * FROM cfg_udops_acl WHERE user_name = %s AND corpus_id = %s;", [user_names, corpus_id])
                existing_permission = cursor.fetchone()

                if existing_permission is None:
                    # Insert a new permission record
                    cursor.execute("INSERT INTO cfg_udops_acl (user_id, user_name, corpus_id, permission) VALUES (%s, %s, %s, %s);",[user_id, user_names, corpus_id, permission])
                else:
                    # Update the existing permission
                    cursor.execute("UPDATE cfg_udops_acl SET permission = %s WHERE user_name = %s AND corpus_id = %s;",[permission, user_names, corpus_id])

            conn.commit()
            cursor.close()
            conn.close()
            return 1
        
        except Exception as e:
            print(e)

    def remove_access_corpus(self, user_name, corpus_name, permission):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # query = f"DELETE FROM cfg_udops_acl WHERE permission = '{permission}', user_name = '{user_name}' AND corpus_id = (SELECT corpus_id FROM corpus_metadata WHERE corpus_name = '{corpus_name}')"
            user_names_str = ", ".join([f"'{name}'" for name in user_name])

            # Construct the SQL query using f-strings
            query = f"""
            DELETE FROM cfg_udops_acl
                WHERE permission = '{permission}'AND corpus_id = (
                SELECT corpus_id
                FROM corpus_metadata
                WHERE corpus_name = '{corpus_name}'
            )
            AND user_name IN ({user_names_str});
            """
            cursor.execute(query)
            if cursor.rowcount == 0:
                return 2
            else:
                conn.commit()
                cursor.close()
                return 1
        except Exception as e:
            raise e

    def access_corpus_list_write(self,corpus_name):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = f'''SELECT user_name
                        FROM cfg_udops_acl
                        WHERE corpus_id IN (
                            SELECT corpus_id
                            FROM corpus_metadata
                            WHERE corpus_name = '{corpus_name}'
                        )
                        AND permission = 'write';
                    '''
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            #  conn.close()
            return rows
        except Exception as e:
            print(e)

    def access_corpus_list_read(self, corpus_name):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = f'''SELECT user_name
                        FROM cfg_udops_acl
                        WHERE corpus_id IN (
                            SELECT corpus_id
                            FROM corpus_metadata
                            WHERE corpus_name = '{corpus_name}'
                        )
                        AND permission = 'read';
                    '''
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            #  conn.close()
            return rows
        except Exception as e:
            print(e)

    def get_list_teams_read(self, user_name):
        try:

            conn = connection.get_connection()
            cursor = conn.cursor()
            # Check if the user_name exists in cfg_udops_users
            user_query = f"SELECT COUNT(*) FROM cfg_udops_users WHERE user_name = '{user_name}'"
            cursor.execute(user_query)
            user_exists = cursor.fetchone()

            if not user_exists[0]:
                return "Invalid user_name."
            else:
                # Fetch all the teamnames for the user_name
                team_query = f"SELECT teamname FROM cfg_udops_teams_metadata WHERE team_id IN (SELECT team_id FROM cfg_udops_users WHERE user_name = '{user_name}')"
                cursor.execute(team_query)
                teamnames = [row[0] for row in cursor.fetchall()]

                accessible_teams = []

                for teamname in teamnames:
                    # Fetch all the corpus_ids associated with the teamname
                    corpus_query = f"SELECT DISTINCT corpus_id FROM cfg_udops_teams_acl WHERE team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}')"
                    cursor.execute(corpus_query)
                    corpus_ids = cursor.fetchall()

                    # Check if the user_name has permission for all the corpus_ids
                    acl_query = f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = '{user_name}' AND corpus_id = ANY(%s) AND permission = 'read'"
                    cursor.execute(acl_query, (corpus_ids,))
                    num_corpuses = cursor.fetchone()[0]

                    if num_corpuses == len(corpus_ids):
                        accessible_teams.append(teamname)

            conn.commit()
            cursor.close()

            return accessible_teams
        except Exception as e:
            raise e

    def get_list_teams_write(self, user_name):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor()

            # Check if the user_name exists in cfg_udops_users
            user_query = f"SELECT COUNT(*) FROM cfg_udops_users WHERE user_name = '{user_name}'"
            cursor.execute(user_query)
            user_exists = cursor.fetchone()

            if not user_exists[0]:
                return "Invalid user_name."
            else:
                # Fetch all the teamnames for the user_name
                team_query = f"SELECT teamname FROM cfg_udops_teams_metadata WHERE team_id IN (SELECT team_id FROM cfg_udops_users WHERE user_name = '{user_name}')"
                cursor.execute(team_query)
                teamnames = [row[0] for row in cursor.fetchall()]
                accessible_teams = []
                for teamname in teamnames:
                    # Fetch all the corpus_ids associated with the teamname
                    corpus_query = (f"SELECT DISTINCT corpus_id FROM cfg_udops_teams_acl WHERE "
                                    f"team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}')")
                    cursor.execute(corpus_query)
                    corpus_ids = cursor.fetchall()

                    # Check if the user_name has permission for all the corpus_ids
                    acl_query = (f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = '{user_name}' AND "
                                 f"corpus_id = ANY(%s) AND permission ='write'")
                    cursor.execute(acl_query, (corpus_ids,))
                    num_corpuses = cursor.fetchone()[0]

                    if num_corpuses == len(corpus_ids):
                        accessible_teams.append(teamname)
                conn.commit()
                cursor.close()

            return accessible_teams

        except Exception as e:
            raise e

    def grant_team_pemission_read(self,user_name, teamname):

        try:
            conn = connection.get_connection()
            cursor = conn.cursor()
            permission = 'read'
            ## here teamname is array of team
            ## fetch user_id
            query1 = f"select user_id from udops_users where user_name = '{user_name}'"
            cursor.execute(query1)
            row1 = cursor.fetchone()
            user_id = row1[0]

            ## fetch teamname related to given usename

            team_query = (f"SELECT teamname FROM cfg_udops_teams_metadata WHERE team_id IN "
                          f"(SELECT team_id FROM cfg_udops_users WHERE user_name = '{user_name}')")
            cursor.execute(team_query)
            teamnames = [row[0] for row in cursor.fetchall()]

            user_team = []  # it will store the teamname who don't have user access.

            for name in teamname:
                t = name
                if t not in teamnames:
                    user_team.append(t)
            remain = [x for x in teamname if x not in user_team]
            # this will give list of team where user have read access
            accessible_teams = []

            for team_name in teamnames:

                # Fetch all the corpus_ids associated with the teamname
                corpus_query = (f"SELECT DISTINCT corpus_id FROM cfg_udops_teams_acl WHERE "
                                f"team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE"
                                f" teamname = '{team_name}')")

                cursor.execute(corpus_query)
                corpus_ids = cursor.fetchall()
                print(f"cursor_id--->{corpus_ids}")

                # Check if the user_name has permission for all the corpus_ids
                acl_query = (f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = '{user_name}' "
                             f"AND corpus_id = ANY(%s) AND permission ='read'")

                cursor.execute(acl_query, (corpus_ids,))

                num_corpuses = cursor.fetchone()[0]

                if num_corpuses == len(corpus_ids):
                    accessible_teams.append(team_name)

            result = []
            for team in remain:
                a = team
                if a in accessible_teams:
                    result.append(team)
                else:
                    team_query = f"SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = %s"
                    cursor.execute(team_query, (team,))
                    team_id = cursor.fetchone()

                    corpus_query = f"SELECT corpus_id FROM cfg_udops_teams_acl WHERE team_id = %s"
                    cursor.execute(corpus_query, (team_id[0],))
                    corpus_ids = cursor.fetchall()

                    # Insert or update records in cfg_udops_acl table
                    for corpus_id in corpus_ids:
                        # Check if the entry already exists in cfg_udops_acl
                        existing_query = (f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = %s "
                                          f"AND corpus_id = %s")
                        cursor.execute(existing_query, (user_name, corpus_id[0]))
                        existing_entry = cursor.fetchone()

                        if existing_entry[0]:
                            # Update the permission for the existing entry
                            update_query = (f"UPDATE cfg_udops_acl SET permission = %s WHERE user_name = %s "
                                            f"AND corpus_id = %s")
                            cursor.execute(update_query, (permission, user_name, corpus_id[0]))

                        else:
                            # Insert a new record
                            insert_query = (f"INSERT INTO cfg_udops_acl (user_id,user_name, corpus_id, permission)"
                                            f" VALUES (%s, %s, %s, %s)")
                            cursor.execute(insert_query, (user_id,user_name, corpus_id[0], permission))

            conn.commit()
            cursor.close()

            return result, user_team
        except Exception as e:
            print(e)

    def grant_team_pemission_write(self, user_name, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor()
            permission = 'write'

            query1 = f"select user_id from udops_users where user_name = '{user_name}'"
            cursor.execute(query1)
            row1 = cursor.fetchone()
            user_id = row1[0]

            team_query = (f"SELECT teamname FROM cfg_udops_teams_metadata WHERE team_id IN "
                          f"(SELECT team_id FROM cfg_udops_users WHERE user_name = '{user_name}')")
            cursor.execute(team_query)
            teamnames = [row[0] for row in cursor.fetchall()]  # it gives the list of teams associated with username
            user_team = []  # it will store the teamname who don't have user access.

            for name in teamname:
                t = name
                if t not in teamnames:
                    user_team.append(t)

            remain = [x for x in teamname if x not in user_team]
            # this will gve list of team where user have read access
            accessible_teams = []
            for team_name in teamnames:

                # Fetch all the corpus_ids associated with the teamname
                corpus_query = (f"SELECT DISTINCT corpus_id FROM cfg_udops_teams_acl WHERE "
                                f"team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE"
                                f" teamname = '{team_name}')")

                cursor.execute(corpus_query)
                corpus_ids = cursor.fetchall()
                # Check if the user_name has permission for all the corpus_ids
                acl_query = (f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = '{user_name}' "
                             f"AND corpus_id = ANY(%s) AND permission ='write'")
                cursor.execute(acl_query, (corpus_ids,))

                num_corpuses = cursor.fetchone()[0]

                if num_corpuses == len(corpus_ids):
                    accessible_teams.append(team_name)

            result = []
            for team in remain:
                a = team
                if a in accessible_teams:
                    result.append(team)
                else:
                    team_query = f"SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = %s"
                    cursor.execute(team_query, (team,))
                    team_id = cursor.fetchone()

                    corpus_query = f"SELECT corpus_id FROM cfg_udops_teams_acl WHERE team_id = %s"
                    cursor.execute(corpus_query, (team_id[0],))
                    corpus_ids = cursor.fetchall()

                    # Insert or update records in cfg_udops_acl table
                    for corpus_id in corpus_ids:
                        # Check if the entry already exists in cfg_udops_acl
                        existing_query = (f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = %s "
                                          f"AND corpus_id = %s")
                        cursor.execute(existing_query, (user_name, corpus_id[0]))
                        existing_entry = cursor.fetchone()

                        if existing_entry[0]:
                            # Update the permission for the existing entry
                            update_query = (f"UPDATE cfg_udops_acl SET permission = %s WHERE user_name = %s "
                                            f"AND corpus_id = %s")
                            cursor.execute(update_query, (permission, user_name, corpus_id[0]))

                        else:
                            # Insert a new record
                            insert_query = (f"INSERT INTO cfg_udops_acl (user_id,user_name, corpus_id, permission)"
                                            f" VALUES (%s, %s, %s, %s)")
                            cursor.execute(insert_query, (user_id, user_name, corpus_id[0], permission))

            conn.commit()
            cursor.close()

            return result, user_team
        except Exception as e:
            print(e)

    def remove_access_team(self, user_name, teamname, permission):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = (f"DELETE FROM cfg_udops_acl WHERE user_name ='{user_name}' AND permission = '{permission}' "
                     f"AND corpus_id IN (SELECT DISTINCT corpus_id FROM cfg_udops_teams_acl "
                     f"WHERE team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname ='{teamname}'))")
            cursor.execute(query)
            conn.commit()
            cursor.close()
            return 1
        except Exception as e:
            error = str(e)
            return error

    def existing_users(self, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = f"""
                        SELECT ARRAY(
                            SELECT user_name
                            FROM cfg_udops_users
                            WHERE team_id = (
                                SELECT team_id
                                FROM cfg_udops_teams_metadata
                                WHERE teamname = '{teamname}'
                            )
                        ) AS usernames;
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            #  conn.close()
            return rows
        except Exception as e:
            print(e)

    def not_existing_users(self, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = f"""
                        SELECT ARRAY(
                            SELECT user_name
                            FROM udops_users
                            WHERE user_name NOT IN (
                                SELECT user_name
                                FROM cfg_udops_users
                                WHERE team_id = ANY (
                                    SELECT team_id
                                    FROM cfg_udops_teams_metadata
                                    WHERE teamname = '{teamname}'
                                )
                            )
                        ) AS usernames;
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            #  conn.close()
            return rows
        except Exception as e:
            print(e)

    def add_team(self, permanent_access_token, tenant_id, admin_user_name, s3_base_path, destination_base_path, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # Retrieve the user_id for the provided admin_user_id from udops_users table
            admin_id = []
            for name in admin_user_name:
                user_id = f"SELECT user_id FROM udops_users WHERE user_name = '{name}'"
                cursor.execute(user_id)
                result  = cursor.fetchone()
                id1 = result['user_id']
                admin_id.append(id1)

                # Check if the teamname already exists
            team_query = f"SELECT teamname FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}' LIMIT 1"
            cursor.execute(team_query)
            result = cursor.fetchone()
            if result is not None:
                return "Teamname already exists!!!"
            else:
                mount_location = mount.mount_s3_bucket(destination_base_path, mount_point=teamname)
            # Insert the new team into cfg_udops_teams_metadata table
                insert_query = (f" INSERT INTO cfg_udops_teams_metadata (teamname,permanent_access_token,"
                                f" tenant_id,  s3_base_path, s3_destination_path,"
                                f" mount_location) VALUES ('{teamname}','{permanent_access_token}', '{tenant_id}',"
                                f"'{s3_base_path}','{destination_base_path}','{mount_location}')")
                cursor.execute(insert_query)

                query1 = f"select team_id from cfg_udops_teams_metadata where teamname='{teamname}'"
                cursor.execute(query1)
                row = cursor.fetchone()
                team_id = row['team_id']
                print(f"team_id-->{team_id}")

                for id2 in admin_id:
                    insert_query1 = (f"INSERT INTO cfg_udops_teams_admin (team_id, admin_id)"
                                     f" VALUES ({team_id},{id2})")
                    cursor.execute(insert_query1)

                conn.commit()
                cursor.close()
                message = "Team added successfully !!!"
                return message
        except Exception as e:
            raise e

    def delete_team(self,teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query1 = f"SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}'"
            cursor.execute(query1)
            row = cursor.fetchone()
            team_id = row['team_id']

            query2 = f"DELETE FROM cfg_udops_teams_admin WHERE team_id = {team_id} "
            cursor.execute(query2)
            query3 = f"DELETE FROM cfg_udops_teams_acl WHERE team_id = {team_id} "
            cursor.execute(query3)
            query4 = f"DELETE FROM cfg_udops_users WHERE team_id = {team_id} "
            cursor.execute(query4)

            query = f"DELETE FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}' "
            cursor.execute(query)
            conn.commit()
            cursor.close()
            return 1
        except Exception as e:
            raise e

    def add_user(self,user_name, firstname, lastname, email):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Check if the user_name already exists
            user_query = f"SELECT user_name FROM udops_users WHERE user_name = '{user_name}' LIMIT 1"
            cursor.execute(user_query)
            result = cursor.fetchone()
            if result is not None:
                return "User already exists!"

            # Insert the new user into the table
            insert_query = f"INSERT INTO udops_users (user_name, firstname, lastname, email) " \
                           f"VALUES ('{user_name}', '{firstname}', '{lastname}', '{email}')"
            cursor.execute(insert_query)

            conn.commit()
            cursor.close()

            return "User added successfully!"

        except Exception as e:
            raise e

    def get_team_list_search(self,teamname_substring):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if teamname_substring=="":
                query=f""" SELECT
                            t.teamname,
                            t.permanent_access_token,
                            t.tenant_id,
                            (SELECT ARRAY_AGG(user_name) FROM udops_users WHERE user_id IN (
                                SELECT admin_id FROM cfg_udops_teams_admin WHERE team_id = t.team_id
                            )) AS admin_user_names,
                            t.s3_base_path,
                            t.s3_destination_path,
                            ARRAY(
                                SELECT user_name FROM cfg_udops_users WHERE team_id = t.team_id
                            ) AS users
                            FROM
                            cfg_udops_teams_metadata AS t;
                            """

                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                return rows

            else:

                query = f""" 
                            SELECT
                            t.teamname,
                            t.permanent_access_token,
                            t.tenant_id,
                            (SELECT ARRAY_AGG(user_name) FROM udops_users WHERE user_id IN (
                                SELECT admin_id FROM cfg_udops_teams_admin WHERE team_id = t.team_id
                            )) AS admin_user_names,
                            t.s3_base_path,
                            t.s3_destination_path,
                            ARRAY(
                                SELECT user_name FROM cfg_udops_users WHERE team_id = t.team_id
                            ) AS users
                            FROM
                            cfg_udops_teams_metadata AS t
                            WHERE t.teamname ILIKE '%{teamname_substring}%';
                            """
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                return rows
        except Exception as e:
            print(e)

    def list_user_search(self,user_name_substring):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if user_name_substring == "":
                query ="SELECT user_name, firstname, lastname, email FROM udops_users;"
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                return rows
            else:
                query = f"SELECT user_name, firstname, lastname, email FROM udops_users WHERE user_name ILIKE '%{user_name_substring}%';"
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                return rows
        except Exception as e:
            print(e)

    def user_status(self, github_username, token):
        try:
            url = 'https://api.github.com/user'
            headers = {'Authorization': f'token {token}'}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                username = response.json()['login']
                if username == github_username:
                    conn = connection.get_connection()
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                    query = f"select user_id,user_name,firstname,lastname,email from udops_users where user_name ='{github_username}'"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    user_id = rows[0]['user_id']

                    if len(rows) == 0:
                        cursor.close()
                        conn.commit()
                        return 0

                    else:
                        query2 = "select admin_id from cfg_udops_teams_admin"
                        cursor.execute(query2)
                        rows1 = cursor.fetchall()
                        arr = []
                        for i in range(len(rows1)):
                            a = rows1[i]['admin_id']
                            arr.append(a)

                        cursor.close()
                        conn.commit()

                        if user_id not in arr:
                            return 1, rows
                        else:
                            return 2, rows
                else:
                    return 0
            else:
                return 0
        except Exception as e:
            err = str(e)
            return err



