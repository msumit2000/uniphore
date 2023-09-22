from udops.src.dep.Handler.UserManagementHandler import *


class UserManagement:
    def get_user_list(self):
        Userlog = UserManagementHandler()
        return Userlog.get_user_list()

    def update_user(self, firstname, lastname, email, existing_user_name, new_user_name):
        user = UserManagementHandler()
        if user.update_user(firstname, lastname, email, existing_user_name, new_user_name) == 1:
            return 1
        else:
            return 2

    def get_team_list(self):
        user = UserManagementHandler()
        return user.get_team_list()

    def update_team(self, permanent_access_token, tenant_id, s3_base_path,destination_base_path, existing_teamname,
                    new_teamname):
        user = UserManagementHandler()
        return user.update_team(permanent_access_token, tenant_id,  s3_base_path,destination_base_path, \
                                existing_teamname,new_teamname)

    def update_admin(self,user_name, teamname):
        try:
            user = UserManagementManager()
            return user.update_admin(user_name, teamname)
        except Exception as e:
            raise e

    def remove_admin(self,user_name, teamname):
        try:
            user = UserManagementManager()
            return user.remove_admin(user_name, teamname)
        except Exception as e:
            raise e

    def list_admin(self,teamname):
        try:
            user = UserManagementManager()
            return user.remove_admin(teamname)
        except Exception as e:
            raise e

    def add_users_team(self, user_name, teamname):
        user = UserManagementHandler()
        return user.add_users_team(user_name, teamname)

    def delete_user(self, corpus_name, teamname):
        user = UserManagementHandler()
        return user.delete_user(corpus_name, teamname)

    def grant_access_corpus(self, user_name, corpus_name, permission):
        user = UserManagementHandler()
        return user.grant_access_corpus(user_name, corpus_name, permission)

    def remove_access_corpus(self, user_name, corpus_name, permission):
        user = UserManagementHandler()
        return user.remove_access_corpus(user_name, corpus_name, permission)

    def access_corpus_list_write(self, corpus_name):
        user = UserManagementHandler()
        return user.access_corpus_list_write(corpus_name)

    def access_corpus_list_read(self, corpus_name):
        user = UserManagementHandler()
        return user.access_corpus_list_read(corpus_name)

    def get_list_teams_read(self, user_name):
        user = UserManagementHandler()
        return user.get_list_teams_read(user_name)

    def get_list_teams_write(self, user_name):
        user = UserManagementHandler()
        return user.get_list_teams_write(user_name)

    def grant_team_pemission_read(self, user_name, teamname):
        user = UserManagementHandler()
        return user.grant_team_pemission_read(user_name, teamname)

    def grant_team_pemission_write(self, user_name, teamname):
        user = UserManagementHandler()
        return user.grant_team_pemission_write(user_name, teamname)

    def remove_access_team(self, user_name, teamname, permission):
        try:
            user = UserManagementHandler()
            return user.remove_access_team(user_name, teamname, permission)
        except Exception as e:
            raise e

    def existing_users(self, teamname):
        user = UserManagementHandler()
        return user.existing_users(teamname)

    def not_existing_users(self, teamname):
        user = UserManagementHandler()
        return user.not_existing_users(teamname)

    def add_team(self, permanent_access_token, tenant_id, admin_user_name, s3_base_path,destination_base_path, teamname):
        user = UserManagementHandler()
        return user.add_team(permanent_access_token, tenant_id, admin_user_name, s3_base_path,destination_base_path, teamname)

    def delete_team(self, teamname):
        user = UserManagementHandler()
        return user.delete_team(teamname)

    def add_user(self, user_name, firstname, lastname, email):
        user = UserManagementHandler()
        return user.add_user(user_name, firstname, lastname, email)

    def get_team_list_search(self, teamname_substring):
        user = UserManagementHandler()
        return user.get_team_list_search(teamname_substring)

    def list_user_search(self, user_name_substring):
        user = UserManagementHandler()
        return user.list_user_search(user_name_substring)

    def user_status(self,github_username, token):
        user = UserManagementHandler()
        return user.user_status(github_username, token)