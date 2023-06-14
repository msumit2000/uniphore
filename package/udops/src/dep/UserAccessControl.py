from udops.src.dep.Handler.AccessControlHandler import UserAuthenticationHandler
from udops.src.dep.Handler.UserLogHandler import User_log
from udops.src.dep.Handler.duplotoken  import *
from udops.src.dep.config.teamusermanager import *

import requests
duplo = duplotoken()
class AccessControl:
    def authenticate(self,ACCESS_TOKEN):
        user = UserAuthenticationHandler()
        return user.authenticate_user(ACCESS_TOKEN)

    def get_user_team(self,user_id):
        user = UserAuthenticationHandler()
        if user.get_user_team(user_id)==1:
            return 1
        else:
            return user.get_user_team(user_id)

    def authorize_user(self,user_id,corpus_id):
        user = UserAuthenticationHandler()
        if user.authorize_user(user_id,corpus_id)==1:
            return 1
        else:
            return 2

    def login(self,token,username):
        Userlog = User_log()
        return Userlog.login(token,username)

    def logout(self):
        Userlog = User_log()
        return Userlog.logout()
    
    def partial_change(self,source_tenant,own_token):
        duplo.ChangeToken(tenant=source_tenant,token=own_token)
    
    def corpus_id(self,corpus_name):
        user = UserAuthenticationHandler()
        return user.corpus_id(corpus_name)
    
    def default_access(self,corpus_id,user_id):
        user = UserAuthenticationHandler()
        return user.default_acess(corpus_id,user_id)


    def retrieve_change(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(dir_path, 'config/udops_config')
        config = configparser.ConfigParser()
        config.read(file_name)
        ACCESS_TOKEN = config.get('github', 'access_token')
        url = 'https://api.github.com/user'
        headers = {'Authorization': f'token {ACCESS_TOKEN}'}
        response = requests.get(url, headers=headers)
        username = response.json()['login']
        teamname = config.get('github','team_name')
        teamuser = teamusermanager()
        teamuser.team_authentication(username,teamname)

        




