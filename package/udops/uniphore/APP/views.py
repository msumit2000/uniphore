from udops.src.dep.udataset import *
from udops.src.dep.UserManagement import *
from udops.src.dep.corpusGUI import GUI
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class create_corpus(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            gui = GUI()
            response = gui.create_corpus(data)
            if response == 0:
                return JsonResponse({"status": "error","message":"user not exist"})
            elif response == 1:
                return JsonResponse({"status": "success","message":"created successfully"})
            elif response == 2:
                return JsonResponse({"status":"error","message":"team not found"})
            elif response == 3:
                return JsonResponse({"status":"error","message": "no mount location"})
            elif response == 4:
                return JsonResponse({"status":"error","message":"corpus already existed"})
            else:
                return JsonResponse({"status": "error", "message": response})


class add(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            gui = GUI()
            response = gui.add(data)
            if response == 1:
                return JsonResponse({"status": "success", "message": "added successfully"})
            elif response == 2:
                return JsonResponse({"status":"error" ,"message":"no mount location"})
            else:
                return JsonResponse({"status": "error", "message": response})


class remote(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            gui = GUI()
            response = gui.remote(data)
            if response == 0:
                return JsonResponse({"status":"error", "message":"no mount location"})
            elif response == 1:
                return JsonResponse({"status":"success", "message": "added successfully"})
            else:
                return JsonResponse({"status": "error", "message": response})


class commit(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            gui = GUI()
            response = gui.commit(data)
            if response == 0:
                return JsonResponse({"status": "error", "message": "no mount location"})
            elif response == 1:
                return JsonResponse({"status": "success", "message": data['message']})
            else:
                return JsonResponse({"status": "error", "message": response})


class push(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            gui = GUI()
            response = gui.push(data)
            if response == 0:
                return JsonResponse({"status":"error","message":"user not exist"})
            elif response == 1:
                return JsonResponse({"status": "success","message":"pushed  successfully"})
            elif response == 2:
                return JsonResponse({"status":"error","message": "no mount location"})
            elif response == 3:
                return JsonResponse({"status":"error","message": "ACCESS DENY"})
            else:
                return JsonResponse({"status": "error", "message": response})


class clone(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            gui = GUI()
            response = gui.clone(data)
            if response == 0:
                return JsonResponse({"status": "error", "message": "user not exist"})
            elif response == 1:
                return JsonResponse({"status": "success", "message": "cloned  successfully"})
            elif response == 2:
                return JsonResponse({"status": "error", "message": "no mount location"})
            elif response == 3:
                return JsonResponse({"status": "error", "message": "ACCESS DENY"})
            else:
                return JsonResponse({"status": "error", "message": response})


class pull(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            gui = GUI()
            response = gui.pull(data)

            if response == 0:
                return JsonResponse({"status": "error", "message": "user not exist"})
            elif response == 1:
                return JsonResponse({"status": "success", "message": "pulled  successfully"})
            elif response == 2:
                return JsonResponse({"status": "error", "message": "no mount location"})
            elif response == 3:
                return JsonResponse({"status": "error", "message": "ACCESS DENY"})
            else:
                return JsonResponse({"status": "error", "message": response})


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


class get_udops_count(APIView):
    permission_classes=([IsAuthenticated])

    def get(self,request):
        if request.method == 'GET':
            re = ucorpus()
            response = re.get_Counts()
            response_data = {
                "status": "success",
                "data": response
            }
            return JsonResponse(response_data, safe=False)


class summary(APIView):
    permission_classes=([IsAuthenticated])
    def get(self,request):
        if request.method =='GET':
            data= json.loads(request.body)
            corpus = ucorpus()
            response=corpus.summary(data['column'])
            data = json.loads(response)
            return JsonResponse(data, safe=False)


class get_corpus_list(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            re = ucorpus()
            response = re.list_corpus(data["language"],data["corpus_type"],data["source_type"])
            response_data = {
                "status": "success",
                "failure_error": " ",
                "data": response
            }
            return JsonResponse(response_data, safe=False)


class language(APIView):

    permission_classes=([IsAuthenticated])

    def get(self,request):
        if request.method == 'GET':
            re = ucorpus()
            response = re.language()
            response_data = {
                "status": "success",
                "failure_error": " ",
                "data": response
                }
            return JsonResponse(response_data, safe=False)


class corpus_type(APIView):

    permission_classes=([IsAuthenticated])
    def get(self,request):
        if request.method == 'GET':
            re = ucorpus()
            response = re.corpus_type()
            response_data = {
            "status": "success",
            "failure_error": " ",
            "data": response
            }
            return JsonResponse(response_data, safe=False)

class source_type(APIView):
    permission_classes=([IsAuthenticated])
    def get(self,request):
        if request.method == 'GET':
            re = ucorpus()
            response = re.source_type()
            response_data = {
            "status": "success",
            "failure_error": " ",
            "data": response
            }
            return JsonResponse(response_data, safe=False)
        


class search_corpus(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            re = ucorpus()
            response = re.search_corpus(data['corpus_name'])
            if response == 0:
                response_data = {
                    "status": "failure",
                    "failure_error": "corpus do not exits!!!",
                }
                return JsonResponse(response_data, safe=False)
            else:
                response_data = {
                "status": "success",
                "data": response
                }
                return JsonResponse(response_data, safe=False)

class upsert(APIView):
    permission_classes=([IsAuthenticated])
    def put(self,request):
        if request.method=='PUT':
            try:

                data= json.loads(request.body)
                corpus = ucorpus()
                if corpus.update_corpus(data)==0 :
                    return JsonResponse({"status":"failure","failure_error":"Corpus doesn't exist"},safe=False)

                else:
                    return JsonResponse({"status":"success"},safe=False)
            except Exception as e:
                raise e


class donut(APIView):
    permission_classes=([IsAuthenticated])
    def get(self,request):
        if request.method =='GET':
            #data= json.loads(request.body)
            data = ['language','corpus_type','source_type','vendor','domain']
            corpus = ucorpus()
            const_data = []
            i =0
            for i in range(len(data)):
                corpus_property= data[i]
                response=corpus.donut(corpus_property)
                key = response[0]
                value = response[1]
                _data = {'name': f'Per {corpus_property}','labels':key,'dataset': [{'label': ' ','data':f'{value}' }]}
                const_data.append(_data)
                i = i +1
            return JsonResponse(const_data,safe=False)

class summary_custom(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        if request.method =='POST':
            data= json.loads(request.body)
            corpus = ucorpus()
            response=corpus.summary_custom(data["corpus_name"])
        # print(response)
            data = json.loads(response)
            return JsonResponse(data, safe=False)


class update_custom_field(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            corpus = ucorpus()
            response = corpus.update_custom_field(data)
            if response ==1:
                return JsonResponse({"status": "updated successfully"}, safe=False)
            else:
                return JsonResponse({"status": "failed"}, safe=False)
####################### Dataset API #####################################


#
# class get_datset_count(APIView):
#     permission_classes=([IsAuthenticated])
#     def get(self,request):
#         if request.method == 'GET':
#             dataset = udataset()
#             response = dataset.get_counts()
#             response_data = {
#                 "status": "success",
#                 "data": response
#             }
#             return JsonResponse(response_data, safe=False)
#
# class dataset_summary(APIView):
#     permission_classes=([IsAuthenticated])
#     def post(self,request):
#         if request.method == 'POST':
#             data= json.loads(request.body)
#             dataset = udataset()
#             response = dataset.get_summary(data["dataset_name"])
#             d = {
#                 "status" : "success / failed",
#                 "failure_error" : "",
#                 "data" : {
#                     "corpusSummary" : response
#                 }
#                 }
#             json_string = json.dumps(d)
#             data = json.loads(json_string)
#             return JsonResponse(data, safe=False)
#
#
#
# class dataset_list(APIView):
#     permission_classes=([IsAuthenticated])
#     def get(self,request):
#         if request.method == 'GET':
#             dataset = udataset()
#             response = dataset.get_list()
#             return JsonResponse(response,safe=False)
#
#
# class dataset_search(APIView):
#     permission_classes=([IsAuthenticated])
#     def post(self,request):
#         if request.method == 'POST':
#             dataset = udataset()
#             data = json.loads(request.body)
#             response = dataset.search_dataset(data["property"])
#             return JsonResponse(response,safe=False)
#
# class update_dataset(APIView):
#     permission_classes=([IsAuthenticated])
#     def post(self,request):
#         if request.method == 'POST':
#             data = json.loads(request.body)
#             dataset = udataset()
#             response = dataset.update(data["dataset_name"],data["corpus_filter"])
#             if response==1:
#                 return JsonResponse({"status": "updated successfully !!!"}, safe=False)
#             else:
#                 return JsonResponse({"status": "failed"}, safe=False)
#
# class dataset_corpus_list(APIView):
#     permission_classes=([IsAuthenticated])
#     def post(self,request):
#         if request.method=='POST':
#             data = json.loads(request.body)
#             dataset = udataset()
#             response = dataset.dataset_corpus_list(data["dataset_name"])
#             return JsonResponse(response,safe=False)

###################### User Management API #####################################

class list_user(APIView):
    permission_classes=([IsAuthenticated])
    def get(self,request):
        if request.method=='GET':
            user = UserManagement()
            response=user.get_user_list()
            response_data = {
            "status":"success",
            "data":response
            }
            return JsonResponse(response_data, safe=False)



class upsert_user(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.update_user(data["firstname"],data["lastname"],data["email"],data["existing_user_name"],data["new_user_name"])
            if response==1:
                return JsonResponse({"status": "updated successfully !!!"}, safe=False)
            else:
                return JsonResponse({"status": "Existing Username is not present!!!"}, safe=False)



class team_list(APIView):
    permission_classes=([IsAuthenticated])
    def get(self,request):
        if request.method=='GET':
            user = UserManagement()
            response=user.get_team_list()
            response_data = {
            "status":"success",
            "data":response
            }
            return JsonResponse(response_data, safe=False)


class team_upsert(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.update_team(data["permanent_access_token"],data["tenant_id"],data["s3_base_path"],data["s3_destination_path"],data["existing_teamname"],data["new_teamname"])
            response_data = {
                "status":"success",
                "data":response
            }
            return JsonResponse(response_data, safe=False)


class upsert_admin(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.update_admin(data['user_name'],data['teamname'])
            if response == 1:
                response_data = {
                    "status": "success",
                    "message": "OK"
                }
                return JsonResponse(response_data, safe=False)

            else:
                response_data = {
                    "status": "error",
                    "data": response
                }
                return JsonResponse(response_data, safe=False)


class remove_admin(APIView):

    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.remove_admin(data['user_name'],data['teamname'])
            if response==1:
                response_data = {
                    "status": "success",
                    "message": "delete successfully"
                }
                return JsonResponse(response_data, safe=False)
            elif response==0:
                response_data = {
                    "status": "success",
                    "message": "team not found"
                }
                return JsonResponse(response_data, safe=False)

            else:
                response_data = {
                    "status": "error",
                    "message": response
                }
                return JsonResponse(response_data, safe=False)


class list_admin(APIView):

    permission_classes = ([IsAuthenticated])

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.list_admin(data['teamname'])
            response_data = {
                "status": "success",
                "message": response
            }
            return JsonResponse(response_data, safe=False)




class add_users_team(APIView):
    permission_classes=([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.add_users_team(data["user_name"],data["teamname"])
            print(response)
            if response == 1:
                response_data = {
                    "status":"error",
                    "data":"user already exist"
                    }
            else:
                response_data = {
                    "status": "success",
                    "data": response
                }

            return JsonResponse(response_data, safe=False)


class remove_users_team(APIView):

    permission_classes=([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.delete_user(data["user_name"],data["teamname"])
            if response==1:
                return JsonResponse({"status": "Data Deleted Successfully !!!"}, safe=False)
            else:
                return JsonResponse({"status": "Teamname is not valid!!!!!"}, safe=False)


class grant_corpus(APIView):

    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method=='POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.grant_access_corpus(data["user_name"],data["corpus_name"],data["permission"])
            if response==1:
                return JsonResponse({"status": "Permission granted successfully for user."}, safe=False)
            else:
                return JsonResponse({"status": "failed"}, safe=False)


class remove_user_corpus(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.remove_access_corpus(data["user_name"],data["corpus_name"],data["permission"])
            if response==1:
                return JsonResponse({"status": "Permission Deleted Successfully !!!"}, safe=False)
            else:
                return JsonResponse({"status": "failed"}, safe=False)


class grant_corpus_list_write(APIView):
    permission_classes=([IsAuthenticated])

    def post(self,request):
        if request.method=='POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.access_corpus_list_write(data["corpus_name"])
            json_string = json.dumps(response)
            data = json.loads(json_string)
            response_data = {
                "status": "success",
                "data": data
            }
            return JsonResponse(response_data, safe=False)

class grant_corpus_list_read(APIView):
    permission_classes=([IsAuthenticated])
    def post(self,request):
        if request.method=='POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.access_corpus_list_read(data["corpus_name"])
            json_string = json.dumps(response)
            data = json.loads(json_string)
            response_data = {
                "status": "success",
                "data": data
            }
            return JsonResponse(response_data, safe=False)


class get_list_teams_read(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.get_list_teams_read(data["user_name"])
            json_string = json.dumps(response)
            data = json.loads(json_string)
            response_data = {
                "status": "success",
                "data": data
            }
            return JsonResponse(response_data, safe=False)


class get_list_teams_write(APIView):

    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.get_list_teams_write(data["user_name"])
            json_string = json.dumps(response)
            data = json.loads(json_string)
            response_data = {
                "status": "success",
                "data": data
            }
            return JsonResponse(response_data, safe=False)


class grant_team_pemission_read(APIView):

    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.grant_team_pemission_read(data["user_name"],data["teamname"])
            return JsonResponse({"status": "success", "data": response}, safe=False)


class grant_team_pemission_write(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.grant_team_pemission_write(data["user_name"],data["teamname"])

            return JsonResponse({"status": "success", "data":response}, safe=False)


class remove_access_team(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.remove_access_team(data["user_name"],data["teamname"],data['permission'])
            if response == 1:
                return JsonResponse({"status": "success", "message":"removed successfully"}, safe=False)
            else:
                return JsonResponse({"status": "failed", "message":response}, safe=False)


class existing_users(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method=='POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.existing_users(data["teamname"])
            json_string = json.dumps(response)
            data = json.loads(json_string)
            response_data = {
            "status": "success",
            "data": data
            }
            return JsonResponse(response_data, safe=False)


class not_existing_users(APIView):
    permission_classes=([IsAuthenticated])

    def post(self,request):
        if request.method=='POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.not_existing_users(data["teamname"])
            json_string = json.dumps(response)
            data = json.loads(json_string)
            response_data = {
            "status": "success",
            "data": data
            }
            return JsonResponse(response_data, safe=False)


class add_team(APIView):

    permission_classes=([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.add_team(data["permanent_access_token"],data["tenant_id"],data["admin_user_name"],data["s3_base_path"],data["s3_destination_path"],data["teamname"])
            response_data = {
            "status":"success",
            "data":response
            }
            return JsonResponse(response_data, safe=False)


class delete_team(APIView):
    permission_classes=([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.delete_team(data["teamname"])
            if response == 1:
                response_data = {
                    "status":"success",
                    "data":"delete successfully !!!"
                }
                return JsonResponse(response_data, safe=False)
            else:
                response_data = {
                    "status": "ERRoR",
                    "data": response
                }
                return JsonResponse(response_data, safe=False)


class add_user(APIView):
    permission_classes=([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.add_user(data["user_name"],data["firstname"],data["lastname"],data["email"])
            response_data = {
                "status":"success",
                "data":response
            }
            return JsonResponse(response_data, safe=False)


class get_team_list_search(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.get_team_list_search(data["teamname_substring"])
            response_data = {
                "status":"success",
                "data":response
            }
            return JsonResponse(response_data, safe=False)


class list_user_search(APIView):
    permission_classes = ([IsAuthenticated])

    def post(self,request):
        if request.method == 'POST':
            data = json.loads(request.body)
            dataset = UserManagement()
            response = dataset.list_user_search(data["user_name_substring"])
            response_data = {
            "status":"success",
            "data":response
            }
            return JsonResponse(response_data, safe=False)

@csrf_exempt
def user_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        git_username = data['git_username']
        token = data['token']
        dataset = UserManagement()
        response = dataset.user_status(git_username, token)

        print(f"response from views--->{response}")

        if response == 0:
            response_data = {
                "User_role": "User Not exist",
            }
        else:
            val = response[0]
            print(f"val-->{val}")
            user_data = response[1]
            print(f"userdata-->{user_data}")
            if val == 1:
                response_data = {
                    "User_role": "normal user",
                    "user_data":user_data
                }
            else:
                response_data = {
                    "User_role": "Admin user",
                    "user_data": user_data
                }
        return JsonResponse(response_data, safe=False)
