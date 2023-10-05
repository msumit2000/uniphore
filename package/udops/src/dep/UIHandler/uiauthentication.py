from udops.src.dep.UIManager.uiauthentication import uiauthentication
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
prop = properties()
connection = Connection()
conn = connection.get_connection()


class authentication:
    def authenticate_user(self, username):
        auth = uiauthentication()
        return auth.authenticate_user(username,conn)

    def authorize_user(self,user_id,corpus_id,access_type):
        auth = uiauthentication()
        return auth.authorise_user(user_id,corpus_id,access_type,conn)

    def authorize_user_clone(self,user_id,corpus_id):
        auth = uiauthentication()
        return auth.authorise_user_clone(user_id,corpus_id,conn)

    def get_user_team(self, teamname):
        auth = uiauthentication()
        return auth.get_user_team(teamname, conn)

    def admin_user(self, team_id, user_id):
        auth = uiauthentication()
        return auth.admin_user(team_id, user_id, conn)

    def get_team_location(self, teamname):
        auth = uiauthentication()
        return auth.get_team_location(teamname, conn)

    def default_acess(self, corpus_id, user_id):
        auth = uiauthentication()
        return auth.default_access(corpus_id, user_id, conn)

    def corpus_id(self, corpus_name):
        auth = uiauthentication()
        return auth.corpus_id(corpus_name, conn)

    def Corpus_team_map(self, team_id, corpus_id):
        auth = uiauthentication()
        return auth.Corpus_team_map(team_id, corpus_id, conn)