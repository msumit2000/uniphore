import configparser
import sys
import os
class duplotoken:
    def ChangeToken(Self,tenant,token):
        try:
            configParser = configparser.RawConfigParser()
            home = os.path.expanduser('~')
            configFilePath = home + "/.aws/config"
            configParser.readfp(open(configFilePath))
            print(configParser.get("default",'region'))
            newvalue = "duplo-jit aws --tenant={} --host https://uniphore-ds.duplocloud.net --token {}".format(tenant,token)
            configParser.set("default",'credential_process',newvalue)
            configParser.write(sys.stdout)
        except Exception as e:
            raise e