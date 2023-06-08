from udops.src.dep.Manager.UACusermanager import *

class uacuserhandler:
    def list_users(self):
        uacusermanager1 = uacusermanager()
        rows = uacusermanager1.list_users()
        print(rows)
    
    def update_user(self,username,firstname,lastname,email):
        uacusermanager1 = uacusermanager()
        uacusermanager1.upsert_user(username,firstname,lastname,email)

    def update_team(self,  teamname , permanent_access_token , tenant_id , admin_user_id , s3_base_path):
        uacusermanager1 = uacusermanager()
        uacusermanager1.upsert_team(teamname , permanent_access_token , tenant_id , admin_user_id , s3_base_path)