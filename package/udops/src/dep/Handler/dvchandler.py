from udops.src.dep.config.teamusermanager import *

teamuser = teamusermanager()

class dvchandler:
    def team_authenticator(self,username,team_name):
        teamuser.team_authentication(username,team_name)
        print(username)
        print(team_name)
