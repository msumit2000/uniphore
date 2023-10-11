import configparser
import sys
import os
class duplotoken:
    def ChangeToken(self,tenant,token):
        try:
            configParser = configparser.RawConfigParser()
            home = os.path.expanduser('~')
            configFilePath = home + "/.aws/config"
            print("000000000000000000000000000000000000")
            print("change_token")
            print(f"configfile_path--> {configFilePath}")

            configParser.read(configFilePath)

            newvalue = "duplo-jit aws --tenant={} --host https://uniphore-ds.duplocloud.net --token {}".format(tenant,token)

            configParser.set('default','credential_process',newvalue)

            with open(configFilePath, 'w') as configfile:
                configParser.write(configfile)

        except Exception as e:
            raise e
