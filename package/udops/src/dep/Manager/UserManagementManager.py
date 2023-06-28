from psycopg2.extras import RealDictCursor
import json
import requests
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
from django.db import IntegrityError

prop = properties()
connection = Connection()
conn = connection.get_connection()


class UserManagementManager:
    ########################### User Management #######################

    def get_user_list(self, conn):
        try:

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT user_name,firstname,lastname,email FROM udops_users")
            rows = cursor.fetchall()
            #            print("$$$$$$$$$$$$$$")
            # print(rows)
            conn.commit()
            cursor.close()
            #  conn.close()
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

    def get_team_list(self, conn):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # query = f"""SELECT t.teamname,t.permanent_access_token,t.tenant_id,t.admin_user_id,t.s3_base_path, ARRAY(SELECT user_name FROM cfg_udops_users WHERE team_id = t.team_id) AS users FROM cfg_udops_teams_metadata AS t;"""
            query = f""" SELECT
                            t.teamname,
                            t.permanent_access_token,
                            t.tenant_id,
                            (SELECT user_name FROM udops_users WHERE user_id = t.admin_user_id) AS admin_user_name,
                            t.s3_base_path,
                            ARRAY(
                                SELECT user_name
                                FROM cfg_udops_users
                                WHERE team_id = t.team_id
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

    def update_team(self, permanent_access_token, tenant_id, admin_user_name, s3_base_path, existing_teamname,
                    new_teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Retrieve the user_id for the provided admin_user_id from udops_users table
            user_id_query = f"SELECT user_id FROM udops_users WHERE user_name = '{admin_user_name}'"
            cursor.execute(user_id_query)
            result = cursor.fetchone()
            if result is None:
                return "Invalid admin user_name !!!"

            admin_user_name = result['user_id']

            # Update the cfg_udops_teams_metadata table with the new values
            query = f"UPDATE cfg_udops_teams_metadata SET permanent_access_token = '{permanent_access_token}', tenant_id = '{tenant_id}', admin_user_id = '{admin_user_name}', s3_base_path = '{s3_base_path}', teamname = '{new_teamname}' WHERE teamname = '{existing_teamname}';"

            cursor.execute(query)

            if cursor.rowcount == 0:
                return "existing_teamname not found!!!"
            else:
                conn.commit()
                cursor.close()
                return "Update successful!!!"
        except Exception as e:
            raise e

    def add_users_team(self, user_name, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

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
            return e

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
            query1 = f"select exists (select user_id from cfg_udops_acl where corpus_id = ( SELECT corpus_id FROM corpus_metadata WHERE corpus_name = '{corpus_name}'))"
            cursor.execute(query1)
            rows = cursor.fetchone()
            user_exist = rows['exists']
            
            if user_exist != True:
                user_names_str = ", ".join([f"'{name}'" for name in user_name])

                # Construct the SQL query using f-strings
                query = f"""
                    UPDATE cfg_udops_acl
                SET permission = '{permission}'
                WHERE corpus_id = (
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
            else : 

                query = f"select user_id from udops_users where user_name = '{user_name}'"
                cursor.execute(query)
                user_id = cursor.fetchone()['user_id']
                query2 = f"select corpus_id from corpus_metadata where corpus_name = '{corpus_name}'"
                cursor.execute(query2)
                corpus_id = cursor.fetchone()['corpus_id']
                query3 = f"insert into cfg_udops_acl (user_id, user_name , corpus_id , permission) values ('{user_id}','{user_name}','{corpus_id}','{permission}')"
                cursor.execute(query3)
                conn.commit()
                cursor.close()
        except Exception as e:
            raise e

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

    def access_corpus_list_write(self, conn, corpus_name):
        try:

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

    def access_corpus_list_read(self, conn, corpus_name):
        try:

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

    def get_list_teams_read(self, conn, user_name):
        try:
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

    def get_list_teams_write(self, conn, user_name):
        try:
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
                    acl_query = f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = '{user_name}' AND corpus_id = ANY(%s) AND permission ='write'"
                    cursor.execute(acl_query, (corpus_ids,))
                    num_corpuses = cursor.fetchone()[0]

                    if num_corpuses == len(corpus_ids):
                        accessible_teams.append(teamname)

            conn.commit()
            cursor.close()

            return accessible_teams
        except Exception as e:
            raise e

    def grant_team_pemission_read(self, conn, user_name, teamname):
        try:
            cursor = conn.cursor()
            permission = 'read'
            for teamname in teamname:
                # Check if the given teamname exists in cfg_udops_teams_metadata
                team_query = f"SELECT COUNT(*) FROM cfg_udops_teams_metadata WHERE teamname = %s"
                cursor.execute(team_query, (teamname,))
                team_exists = cursor.fetchone()

                if not team_exists[0]:
                    return 4
                else:
                    # Check if the user_name is associated with the given teamname
                    user_query = f"SELECT COUNT(*) FROM cfg_udops_users WHERE user_name = %s AND team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = %s)"
                    cursor.execute(user_query, (user_name, teamname))
                    user_exists = cursor.fetchone()

                    if not user_exists[0]:
                        return 3
                    else:
                        # Get the team_id for the given teamname
                        team_query = f"SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = %s"
                        cursor.execute(team_query, (teamname,))
                        team_id = cursor.fetchone()

                        if not team_id:
                            return 2

                        # Get the corpus_id values associated with the team
                        corpus_query = f"SELECT corpus_id FROM cfg_udops_teams_acl WHERE team_id = %s"
                        cursor.execute(corpus_query, (team_id[0],))
                        corpus_ids = cursor.fetchall()

                        # Insert or update records in cfg_udops_acl table
                        for corpus_id in corpus_ids:
                            # Check if the entry already exists in cfg_udops_acl
                            existing_query = f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = %s AND corpus_id = %s"
                            cursor.execute(existing_query, (user_name, corpus_id[0]))
                            existing_entry = cursor.fetchone()

                            if existing_entry[0]:
                                # Update the permission for the existing entry
                                update_query = f"UPDATE cfg_udops_acl SET permission = %s WHERE user_name = %s AND corpus_id = %s"
                                cursor.execute(update_query, (permission, user_name, corpus_id[0]))
                            else:
                                # Insert a new record
                                insert_query = f"INSERT INTO cfg_udops_acl (user_name, corpus_id, permission) VALUES (%s, %s, %s)"
                                cursor.execute(insert_query, (user_name, corpus_id[0], permission))

            conn.commit()
            cursor.close()

            return 1
        except Exception as e:
            print(e)

    def grant_team_pemission_write(self, conn, user_name, teamname):
        try:
            cursor = conn.cursor()
            permission = 'write'
            for teamname in teamname:
                # Check if the given teamname exists in cfg_udops_teams_metadata
                team_query = f"SELECT COUNT(*) FROM cfg_udops_teams_metadata WHERE teamname = %s"
                cursor.execute(team_query, (teamname,))
                team_exists = cursor.fetchone()

                if not team_exists[0]:
                    return 4
                else:
                    # Check if the user_name is associated with the given teamname
                    user_query = f"SELECT COUNT(*) FROM cfg_udops_users WHERE user_name = %s AND team_id = (SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = %s)"
                    cursor.execute(user_query, (user_name, teamname))
                    user_exists = cursor.fetchone()

                    if not user_exists[0]:
                        return 3
                    else:
                        # Get the team_id for the given teamname
                        team_query = f"SELECT team_id FROM cfg_udops_teams_metadata WHERE teamname = %s"
                        cursor.execute(team_query, (teamname,))
                        team_id = cursor.fetchone()

                        if not team_id:
                            return 2

                        # Get the corpus_id values associated with the team
                        corpus_query = f"SELECT corpus_id FROM cfg_udops_teams_acl WHERE team_id = %s"
                        cursor.execute(corpus_query, (team_id[0],))
                        corpus_ids = cursor.fetchall()

                        # Insert or update records in cfg_udops_acl table
                        for corpus_id in corpus_ids:
                            # Check if the entry already exists in cfg_udops_acl
                            existing_query = f"SELECT COUNT(*) FROM cfg_udops_acl WHERE user_name = %s AND corpus_id = %s"
                            cursor.execute(existing_query, (user_name, corpus_id[0]))
                            existing_entry = cursor.fetchone()

                            if existing_entry[0]:
                                # Update the permission for the existing entry
                                update_query = f"UPDATE cfg_udops_acl SET permission = %s WHERE user_name = %s AND corpus_id = %s"
                                cursor.execute(update_query, (permission, user_name, corpus_id[0]))
                            else:
                                # Insert a new record
                                insert_query = f"INSERT INTO cfg_udops_acl (user_name, corpus_id, permission) VALUES (%s, %s, %s)"
                                cursor.execute(insert_query, (user_name, corpus_id[0], permission))

            conn.commit()
            cursor.close()

            return 1
        except Exception as e:
            print(e)

    def existing_users(self, conn, teamname):
        try:

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

    def not_existing_users(self, conn, teamname):
        try:

            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query = f"""
                        SELECT ARRAY(
                            SELECT user_name
                            FROM udops_users
                            WHERE user_name NOT IN (
                                SELECT user_name
                                FROM cfg_udops_users
                                WHERE team_id = (
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

    def add_team(self, permanent_access_token, tenant_id, admin_user_name, s3_base_path, teamname):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Retrieve the user_id for the provided admin_user_id from udops_users table
            user_id_query = f"SELECT user_id FROM udops_users WHERE user_name = '{admin_user_name}'"
            cursor.execute(user_id_query)
            result = cursor.fetchone()
            if result is None:
                return "Admin user not found!!!"

            admin_user_name = result['user_id']

            # Check if the teamname already exists
            team_query = f"SELECT teamname FROM cfg_udops_teams_metadata WHERE teamname = '{teamname}' LIMIT 1"
            cursor.execute(team_query)
            result = cursor.fetchone()
            if result is not None:
                return "Teamname already exists!!!"

            # Insert the new team into cfg_udops_teams_metadata table
            insert_query = f"INSERT INTO cfg_udops_teams_metadata (teamname, permanent_access_token, tenant_id, admin_user_id, s3_base_path) VALUES ('{teamname}', '{permanent_access_token}', '{tenant_id}', '{admin_user_name}', '{s3_base_path}')"
            cursor.execute(insert_query)

            conn.commit()
            cursor.close()

            return "Team added successfully !!!"
        except Exception as e:
            raise e

    def add_user(self, conn, user_name, firstname, lastname, email):
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

    def get_team_list_search(self, conn, teamname_substring):
        try:
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"""SELECT
                            t.teamname,
                            t.permanent_access_token,
                            t.tenant_id,
                            (SELECT user_name FROM udops_users WHERE user_id = t.admin_user_id) AS admin_user_name,
                            t.s3_base_path,
                            ARRAY(
                                SELECT user_name
                                FROM cfg_udops_users
                                WHERE team_id = t.team_id
                            ) AS users
                        FROM
                            cfg_udops_teams_metadata AS t
                        WHERE
                            t.teamname ILIKE '%{teamname_substring}%';"""

            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            # conn.close()
            return rows
        except Exception as e:
            print(e)

    def list_user_search(self, conn, user_name_substring):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"""SELECT user_name, firstname, lastname, email
                        FROM udops_users
                        WHERE user_name ILIKE '%{user_name_substring}%';"""
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            return rows
        except Exception as e:
            print(e)
