from udops.src.dep.Handler.AccessControlHandler import UserAuthenticationHandler
from udops.src.dep.Handler.UserLogHandler import User_log
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

    def authorize_user(self,user_id,corpus_id,access_type):
        user = UserAuthenticationHandler()
        if user.authorize_user(user_id,corpus_id,access_type)==1:
            return 1
        else:
            return 2

    def login(self,token,username):
        Userlog = User_log()
        return Userlog.login(token,username)

    def logout(self):
        Userlog = User_log()
        return Userlog.logout()




