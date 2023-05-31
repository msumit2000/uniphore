from udops.src.dep.Manager.UserLogManager import *


class Userlog:
    def login(self,token,user_name):
        Userlog = User_log()
        return Userlog.login(token,user_name)

    def logout(self):
        Userlog = User_log()
        return Userlog.logout()