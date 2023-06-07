from udops.src.dep.Manager.UACusermanager import *

class uacuserhandler:
    def list_users(self):
        uacusermanager1 = uacusermanager()
        rows = uacusermanager1.list_users()
        return rows
    
    def upsert_user(self,username,firstname,lastname,email):
        uacusermanager1 = uacusermanager()
        uacusermanager1.upsert_user(username,firstname,lastname,email)