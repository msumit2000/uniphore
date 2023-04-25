from udops.src.dep.Handler.CorpusHandler import *
from udops.src.dep.Manager.DatasetMetadatamanager import *
import shutil
import os
from datetime import datetime
from udops.src.dep.config.Connection import *
from udops.src.dep.ucorpus import ucorpus
from udops.src.dep.Manager.CorpusRepositoryManager import CorpusRepositoryManager

connection = Connection()
corpusHandler = CorpusHandler()
import json
corpusRepositoryManager1 = CorpusRepositoryManager()


class DatasetReaderManager:
    def create_dataset_manager(self, dataset_name, file_path,schema_type,custom_schema):
        conn = connection.get_connection()
        corpus_handler = CorpusHandler()
        output_file_path=os.getcwd()
#        output_file_path=
        datasetMetadataManager = DatasetMetadatamanager()
        corpora_name = datasetMetadataManager.list_corpora(conn, dataset_name)
        isExist = os.path.exists(output_file_path + "/" + dataset_name)
        counter = 0
        inp_path = output_file_path
        if not isExist:

            os.makedirs(output_file_path + "/" + dataset_name)
            os.chdir(output_file_path +"/"+ dataset_name)
            if not isExist:

                os.makedirs(os.getcwd() + "/corpora")

                os.makedirs(os.getcwd() + "/datasets")
            os.chdir(os.getcwd() + "/corpora")
            corpus_location = os.getcwd()

            corpus_location_list=[]
            json_output_path = output_file_path +"/"+dataset_name + "/datasets/" + datetime.now().strftime(
                '%Y%m%d%H%M%S')
            os.makedirs(json_output_path)

            for cpr in corpora_name:
                for corpus in cpr:
                    if not isExist:
                
                        isExist1 = os.path.exists(corpus_location+"/"+corpus["corpus_type"])
                        if not isExist1:
                            os.makedirs(corpus_location+"/"+corpus["corpus_type"])
                        os.chdir(corpus_location+"/"+corpus["corpus_type"])
                        corpusHandler.clone_repo(corpus['git_remote'])
                        os.chdir(corpus_location + "/"+corpus["corpus_type"]+"/" + corpus['corpus_name'])
                        dvc_file=corpus['corpus_name'] + ".dvc"
                #        print("!!!!!!!!!!!!!!!!!!!")
                     #   audio=""
                    #    if corpus['corpus_name']== "hinglish":
                      #      audio="audio"
                       # else :
                        audio=None
                        corpusRepositoryManager1.pull(audio)
                        final_file_path = json_output_path + "/" + corpus["corpus_type"]    
                        response_corpus = corpus_handler.datareader(corpus["corpus_name"], schema_type, custom_schema)
                    
                        isExists = os.path.exists(json_output_path + "/" + corpus["corpus_type"])
                        if not isExists:
                            os.makedirs(json_output_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"])
                            with open(json_output_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"]+"/part_"+str(counter)+".json", 'w+') as f:
                                json.dump(response_corpus, f)

                        else:
                            os.makedirs(json_output_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"])
                            with open(json_output_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"]+"/part_"+str(counter)+ ".json", 'w+') as f:
                                json.dump(response_corpus, f)
        else:

            os.chdir(output_file_path + "/" + dataset_name+"/datasets")
            corpus_location = os.getcwd()

            json_file_path=os.getcwd()+"/"+datetime.now().strftime(
                '%Y%m%d%H%M%S')
            os.makedirs(json_file_path)
            os.chdir(json_file_path)
            isExist = os.path.exists(output_file_path + "/" + dataset_name)

            for cpr in corpora_name:
                for corpus in cpr:
                    if isExist:
                        isExist1 = os.path.exists(corpus_location+"/"+corpus["corpus_type"])
                        if not isExist1:
                            os.makedirs(corpus_location+"/"+corpus["corpus_type"])
                        os.chdir(corpus_location+"/"+corpus["corpus_type"])
                        
                        corpusHandler.clone_repo(corpus['git_remote'])
                        os.chdir(corpus_location + "/"+corpus["corpus_type"]+"/" + corpus['corpus_name'])
                 #       corpusHandler.remote_repo(corpus['corpus_name'], corpus['remote_location'], corpus['git_remote'])
                        corpusHandler.pull_repo(corpus['corpus_name'] + ".dvc")
                        final_file_path = json_file_path + "/" + corpus["corpus_type"]
                        response_corpus = corpus_handler.datareader(corpus["corpus_name"], schema_type, custom_schema)
                    
                        isExists = os.path.exists(json_file_path + "/" + corpus["corpus_type"])
                        if not isExists:
                            os.makedirs(json_file_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"])
                            with open(json_file_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"]+"/part_"+str(counter)+".json", 'w+') as f:
                                json.dump(response_corpus, f)

                        else:
                            os.makedirs(json_file_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"])
                            with open(json_file_path + "/" + corpus["corpus_type"]+ "/" + corpus["corpus_name"]+"/part_"+str(counter)+ ".json", 'w+') as f:
                                json.dump(response_corpus, f)

            counter=counter+1

    def generate_output(self,dataset_name,schema,custom_schema):
        current_dir=os.getcwd()
  #      audio_path = os.path.join(data_dir, 'audio')
        lst_1 = os.listdir(current_dir)
        audio_lst = [file for file in lst_1 if file.endswith(".json")] 
       # print(audio_lst)
        #for file in audio_lst:
         #   print("1")
        
        
        for folder_name in os.listdir():
    
            os.chdir(os.getcwd()+"/"+folder_name)
            #for cpr in corpora_name:
             #   for corpus in cpr:
                    
            response_corpus = CorpusHandler().datareader(folder_name, "common",custom_schema)
        
            os.chdir(current_dir)
            with open(current_dir+"/"+folder_name+"_data.json",'w+') as f:
                json.dump(response_corpus, f)
