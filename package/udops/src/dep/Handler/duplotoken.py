import configparser
import os
import json
import http.client


class duplotoken:

    def ChangeToken(self,tenant,token):
        try:
            configParser = configparser.RawConfigParser()
            home = os.path.expanduser('~')
            configFilePath = home + "/.aws/config"
            configParser.read(configFilePath)

            newvalue = "duplo-jit aws --tenant={} --host https://uniphore-ds.duplocloud.net --token {}".format(tenant,token)
            configParser.set('default','credential_process',newvalue)

            with open(configFilePath, 'w') as configfile:
                configParser.write(configfile)

        except Exception as e:
            raise e

    def credentials(self, duplotoken, tenant):
        try:
            conn = http.client.HTTPSConnection("uniphore-ds.duplocloud.net")
            payload = ''
            token = f'Bearer {duplotoken}'
            headers = {
                'Authorization': token
            }

            tenant_dict = {
                "dataopsdev": "475c088e-a3a0-416c-9407-3c70b4ceed52",
                "dsg-india": "817bf893-8540-4360-a63d-b9b87000fa2e",
                "dsg-us": "7b54fb98-5aef-4464-b751-c0a8c1d62c47"
            }
            if tenant in tenant_dict:
                value = tenant_dict[tenant]
                conn.request("GET", "/subscriptions/" + value + "/GetAwsConsoleTokenUrl", payload, headers)
                response = conn.getresponse()
                response_data = response.read()
                data = json.loads(response_data.decode("utf-8"))

                # Extract required fields
                access_key_id = data.get("AccessKeyId", "")
                secret_access_key = data.get("SecretAccessKey", "")
                session_token = data.get("SessionToken", "")

                # Print or store the extracted values as strings
                print("Access Key ID:", access_key_id)
                print("Secret Access Key:", secret_access_key)
                print("Session Token:", session_token)
                print("REPLACE KEY, SECRET AND TOKEN IN THE TENANT PROFILE IN THE AWS CONFIG AND THEN DO S3 MOUNT")

                configParser = configparser.RawConfigParser()
                home = os.path.expanduser('~')
                configFilePath = home + "/.aws/credentials"
                configParser.read(configFilePath)

                configParser.set('default', 'aws_access_key_id',access_key_id)
                configParser.set('default', 'aws_secret_access_key', secret_access_key)

                with open(configFilePath, 'w') as configfile:
                    configParser.write(configfile)
            else:
                print(f"{tenant} not found in the dictionary.")

        except Exception as e:
            err = str(e)
            return err
