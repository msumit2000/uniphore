from udops.src.dep.Manager.UserManagementManager import *
import os
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *

prop = properties()
connection = Connection()
conn = connection.get_connection()

class UserManagementHandler:
    def get_user_list(self):
        try:
            user = UserManagementManager()
            return user.get_user_list()
        except Exception as e:
            raise e

    def update_user(self,firstname,lastname, email, existing_user_name, new_user_name):
        try:
            user = UserManagementManager()
            return user.update_user(firstname,lastname, email, existing_user_name, new_user_name)
        except Exception as e:
            raise e

    def get_team_list(self):
        try:
            user = UserManagementManager()
            return user.get_team_list()
        except Exception as e:
            raise e

    def update_team(self, permanent_access_token, tenant_id, s3_base_path,destination_base_path, existing_teamname,new_teamname):
        try:
            user = UserManagementManager()
            return user.update_team(permanent_access_token, tenant_id,  s3_base_path,
                                    destination_base_path, existing_teamname,new_teamname)
        except Exception as e:
            raise e

    def upadate_admin(self,user_name, teamname):
        try:
            user = UserManagementManager()
            return user.update_admin(user_name, teamname)
        except Exception as e:
            raise e

    def list_admin(self,teamname):
        try:
            user = UserManagementManager()
            return user.update_admin(teamname)
        except Exception as e:
            raise e

    def remove_admin(self, user_name, teamname):
        try:
            user = UserManagementManager()
            return user.remove_admin(user_name, teamname)
        except Exception as e:
            raise e

    def add_users_team(self, user_name, teamname):
        try:
            user = UserManagementManager()
            return user.add_users_team(user_name, teamname)
        except Exception as e:
            raise e

    def delete_user(self, user_name, teamname):
        try:
            user = UserManagementManager()
            return user.delete_user(user_name, teamname)
        except Exception as e:
            raise e

    def grant_access_corpus(self, user_name,corpus_name,permission):
        try:
            user = UserManagementManager()
            return user.grant_access_corpus(user_name,corpus_name,permission)
        except Exception as e:
            raise e

    def remove_access_corpus(self, user_name,corpus_name,permission):
        try:
            user = UserManagementManager()
            return user.remove_access_corpus(user_name,corpus_name,permission)
        except Exception as e:
            raise e

    def access_corpus_list_write(self,corpus_name):
        try:
            user = UserManagementManager()
            return user.access_corpus_list_write(corpus_name)
        except Exception as e:
            raise e

    def access_corpus_list_read(self,corpus_name):
        try:
            user = UserManagementManager()
            return user.access_corpus_list_read(corpus_name)
        except Exception as e:
            raise e

    def get_list_teams_read(self,user_name):
        try:
            user = UserManagementManager()
            return user.get_list_teams_read(user_name)
        except Exception as e:
            raise e

    def get_list_teams_write(self,user_name):

        try:
            user = UserManagementManager()
            return user.get_list_teams_write(user_name)
        except Exception as e:
            raise e

    def remove_access_team(self, user_name, teamname, permission):
        try:
            user = UserManagementManager()
            return user.remove_access_team(user_name,teamname,permission)
        except Exception as e:
            raise e

    def grant_team_pemission_read(self,user_name,teamname):
        try:
            user = UserManagementManager()
            return user.grant_team_pemission_read(user_name,teamname)
        except Exception as e:
            raise e

    def grant_team_pemission_write(self,user_name,teamname):
        try:
            user = UserManagementManager()
            return user.grant_team_pemission_write(user_name,teamname)
        except Exception as e:
            raise e

    def existing_users(self,teamname):
        try:
            user = UserManagementManager()
            return user.existing_users(teamname)
        except Exception as e:
            raise e

    def not_existing_users(self,teamname):
        try:
            user = UserManagementManager()
            return user.not_existing_users(teamname)
        except Exception as e:
            raise e

    def add_team(self, permanent_access_token, tenant_id, admin_user_name, s3_base_path,destination_base_path, teamname):
        try:
            user = UserManagementManager()
            return user.add_team(permanent_access_token, tenant_id, admin_user_name, s3_base_path,destination_base_path, teamname)
        except Exception as e:
            raise e

    def delete_team(self,teamname):
        try:
            user = UserManagementManager()
            return user.delete_team(teamname)
        except Exception as e:
            raise e

    def add_user(self, user_name, firstname, lastname, email):
        try:
            user = UserManagementManager()
            return user.add_user(user_name, firstname, lastname, email)
        except Exception as e:
            raise e

    def get_team_list_search(self, teamname_substring):
        try:
            user = UserManagementManager()
            return user.get_team_list_search(teamname_substring)
        except Exception as e:
            raise e

    def list_user_search(self, user_name_substring):
        try:
            user = UserManagementManager()
            return user.list_user_search(user_name_substring)
        except Exception as e:
            raise e

    def user_status(self, github_username, token):
        try:
            user = UserManagementManager()
            return user.user_status(github_username, token)
        except Exception as e:
            raise e