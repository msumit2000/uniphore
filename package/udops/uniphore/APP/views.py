from udops.src.dep.ucorpus import *
from udops.src.dep.udataset import *
from udops.src.dep.UserManagement import *
from udops.src.dep.Manager.CorpusMetadataManager import *
from udops.src.dep.Manager.UserManagementManager import *
from udops.src.dep.Handler.UserManagementHandler import *
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

prop = properties()
connection = Connection()
conn = connection.get_connection()


# Create your views here.
################# -----------------------------------------------------##################
@csrf_exempt
def get_udops_count(request):
    if request.method == 'GET':
        re = ucorpus()
        response = re.get_Counts()
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def summary(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        corpus = ucorpus()
        response = corpus.summary(data['column'])
        print(response)
        data = json.loads(response)
        return JsonResponse(data, safe=False)


@csrf_exempt
def get_corpus_list(request):
    if request.method == 'POST':
        re = ucorpus()
        response = re.list_corpus()
        response_data = {
            "status": "success",
            "failure_error": " ",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def search_corpus(request):
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
            json_string = json.dumps(response)
            data = json.loads(json_string)
            response_data = {
                "status": "success",
                "data": data
            }
            return JsonResponse(response_data, safe=False)


@csrf_exempt
def upsert(request):
    if request.method == 'PUT':
        try:

            data = json.loads(request.body)
            corpus = ucorpus()
            if corpus.update_corpus(data) == 0:
                return JsonResponse({"status": "failure", "failure_error": "Corpus doesn't exist"}, safe=False)

            else:
                return JsonResponse({"status": "success"}, safe=False)
        except Exception as e:
            raise e


@csrf_exempt
def donut(request):
    if request.method == 'GET':
        # data= json.loads(request.body)
        data = ['language', 'corpus_type', 'source_type', 'vendor', 'domain']
        corpus = ucorpus()
        const_data = []
        i = 0
        for i in range(len(data)):
            corpus_property = data[i]
            response = corpus.donut(corpus_property)
            print(response)
            key = response[0]
            value = response[1]
            _data = {'name': f'Per {corpus_property}', 'labels': key, 'dataset': [{'label': ' ', 'data': f'{value}'}]}
            const_data.append(_data)
            i = i + 1
        return JsonResponse(const_data, safe=False)


@csrf_exempt
def summary_custom(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        corpus = ucorpus()
        response = corpus.summary_custom(data["corpus_name"])
        # print(response)
        data = json.loads(response)
        return JsonResponse(data, safe=False)


@csrf_exempt
def update_custom_field(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        corpus = ucorpus()
        response = corpus.update_custom_field(data)
        if response == 1:
            return JsonResponse({"status": "updated successfully"}, safe=False)
        else:
            return JsonResponse({"status": "failed"}, safe=False)


####################### Dataset API #####################################

@csrf_exempt
def dataset_summary(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = udataset()
        response = dataset.get_summary(data["dataset_name"])
        d = {
            "status": "success / failed",
            "failure_error": "",
            "data": {
                "corpusSummary": response
            }
        }
        json_string = json.dumps(d)
        data = json.loads(json_string)
        return JsonResponse(data, safe=False)


@csrf_exempt
def dataset_list(request):
    if request.method == 'POST':
        dataset = udataset()
        response = dataset.get_list()
        return JsonResponse(response, safe=False)


@csrf_exempt
def dataset_search(request):
    if request.method == 'POST':
        dataset = udataset()
        data = json.loads(request.body)
        response = dataset.search_dataset(data["property"])
        return JsonResponse(response, safe=False)


@csrf_exempt
def update_dataset(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = udataset()
        response = dataset.update(data["dataset_name"], data["corpus_filter"])
        if response == 1:
            return JsonResponse({"status": "updated successfully !!!"}, safe=False)
        else:
            return JsonResponse({"status": "failed"}, safe=False)


@csrf_exempt
def dataset_corpus_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = udataset()
        response = dataset.dataset_corpus_list(data["dataset_name"])
        return JsonResponse(response, safe=False)


####################### User Management API #####################################

@csrf_exempt
def list_user(request):
    if request.method == 'GET':
        user = UserManagement()
        response = user.get_user_list()
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def upsert_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.update_user(data["firstname"], data["lastname"], data["email"], data["existing_user_name"],
                                       data["new_user_name"])
        if response == 1:
            return JsonResponse({"status": "updated successfully !!!"}, safe=False)
        else:
            return JsonResponse({"status": "Existing Username is not present!!!"}, safe=False)


@csrf_exempt
def team_list(request):
    if request.method == 'GET':
        user = UserManagement()
        response = user.get_team_list()
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def team_upsert(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.update_team(data["permanent_access_token"], data["tenant_id"], data["admin_user_name"],
                                       data["s3_base_path"], data["existing_teamname"], data["new_teamname"])
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def add_users_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.add_users_team(data["user_name"], data["teamname"])
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def remove_users_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.delete_user(data["user_name"], data["teamname"])
        if response == 1:
            return JsonResponse({"status": "Data Deleted Successfully !!!"}, safe=False)
        else:
            return JsonResponse({"status": "Teamname is not valid!!!!!"}, safe=False)


@csrf_exempt
def grant_corpus(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.grant_access_corpus(data["user_name"], data["corpus_name"], data["permission"])
        if response == 1:
            return JsonResponse({"status": "Permission Updated Successfully !!!"}, safe=False)
        else:
            return JsonResponse({"status": "failed"}, safe=False)


@csrf_exempt
def remove_user_corpus(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.remove_access_corpus(data["user_name"], data["corpus_name"], data["permission"])
        if response == 1:
            return JsonResponse({"status": "Permission Deleted Successfully !!!"}, safe=False)
        else:
            return JsonResponse({"status": "failed"}, safe=False)


@csrf_exempt
def grant_corpus_list_write(request):
    if request.method == 'POST':
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


@csrf_exempt
def grant_corpus_list_read(request):
    if request.method == 'POST':
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


@csrf_exempt
def get_list_teams_read(request):
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


@csrf_exempt
def get_list_teams_write(request):
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


@csrf_exempt
def grant_team_pemission_read(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.grant_team_pemission_read(data["user_name"], data["teamname"])
        if response == 1:
            return JsonResponse({"status": "Permission Granted Successfully !!!"}, safe=False)
        elif response == 2:
            return JsonResponse({"status": "No team found with the teamname !!!"}, safe=False)
        elif response == 3:
            return JsonResponse({"status": "The user does not have access to the team !!!"}, safe=False)
        elif response == 4:
            return JsonResponse({"status": "Invalid teamname !!!"}, safe=False)
        else:
            return JsonResponse({"status": "failed"}, safe=False)


@csrf_exempt
def grant_team_pemission_write(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.grant_team_pemission_write(data["user_name"], data["teamname"])
        if response == 1:
            return JsonResponse({"status": "Permission Granted Successfully !!!"}, safe=False)
        elif response == 2:
            return JsonResponse({"status": "No team found with the teamname !!!"}, safe=False)
        elif response == 3:
            return JsonResponse({"status": "The user does not have access to the team !!!"}, safe=False)
        elif response == 4:
            return JsonResponse({"status": "Invalid teamname !!!"}, safe=False)
        else:
            return JsonResponse({"status": "failed"}, safe=False)


@csrf_exempt
def existing_users(request):
    if request.method == 'POST':
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


@csrf_exempt
def not_existing_users(request):
    if request.method == 'POST':
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


@csrf_exempt
def add_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.add_team(data["permanent_access_token"], data["tenant_id"], data["admin_user_name"],
                                    data["s3_base_path"], data["teamname"])
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.add_user(data["user_name"], data["firstname"], data["lastname"], data["email"])
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def get_team_list_search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.get_team_list_search(data["teamname_substring"])
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)


@csrf_exempt
def list_user_search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dataset = UserManagement()
        response = dataset.list_user_search(data["user_name_substring"])
        response_data = {
            "status": "success",
            "data": response
        }
        return JsonResponse(response_data, safe=False)
