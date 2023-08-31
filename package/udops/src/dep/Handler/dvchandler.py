from udops.src.dep.config.teamusermanager import *


class dvchandler:
    def team_authenticator(self,username,team_name):
        teamuser = teamusermanager()
        teamuser.team_authentication(username,team_name)
