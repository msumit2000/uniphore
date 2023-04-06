from udops.src.dep.Manager.CorpusMetadataManager import *
from udops.src.dep.Manager.CorpusRepositoryManager import *
from udops.src.dep.Manager.CorpusDataReaderManager import *
import os
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *
prop=properties()
connection = Connection()
conn = connection.get_connection()



class CorpusHandler:

    def RDSConfig(self,host, dbname , user, password):
        connection.create_connection( host=host, dbname=dbname, user=user, password=password)


    def corpus_custom_fields(self,corpusname,kv_pairs):
        corpusMetadataManager = CorpusMetadataManager()
        conn = connection.get_connection()
        corpusMetadataManager.corpus_custom_fields(corpusname, kv_pairs, conn)

    def list_commits(self):
        corpusRepositoryManager = CorpusRepositoryManager()
        corpusRepositoryManager.list_commits()
       
    def checkout(self, commitid):
        corpusRepositoryManager = CorpusRepositoryManager()
        corpusRepositoryManager.checkout(commitid)



    def list_corpus_names(self, filter_value):
         try:
             corpusMetadataManager = CorpusMetadataManager()
             conn = connection.get_connection()
 #            print(filter_value)
             answer = corpusMetadataManager.list_corpus_names(filter_value, conn)
  #           print(answer)
             if answer == []:
                 raise Exception("No corpus belongs to this filter  exist")
             for names in answer:
                 print(names['corpus_name'])
             return answer
         except Exception as e:
             raise e

    def get_corpus_metadata(self, corpus_name):
        try:
            corpusMetadataManager = CorpusMetadataManager()
            
            row1 = corpusMetadataManager.get_corpus_metadata_by_id(corpus_name, conn)
            if row1 ==[]:
                raise Exception("ENter valid corpus name")
            output=""
            str1={}
            
            for row in row1:
                output={
                        "corpus_id":row['corpus_id'],
                        "corpus_name":row['corpus_name'],
                        "language":row['language'],
                        "corpus_type":row['corpus_type'],
                        "source_type":row['source_type'],
                        "customer_name":row['customer_name'],
                        "data_domain_name":row['data_domain_name']
                        }
            response=json.dumps(output)
            return response
        except Exception as e:
            raise e
     
    def delete_corpus(self, corpus_name):
        try:
            corpusMetadataManager = CorpusMetadataManager()
            corpusMetadataManager.delete_corpus(corpus_name,conn)
            corpusRepositoryManager = CorpusRepositoryManager()
            corpusRepositoryManager.destroy()
        except Exception as e:
            raise e

    def manager_get_metadata_type(self, corpus_type):
        try:
            corpusMetadataManager = CorpusMetadataManager()
            rows = corpusMetadataManager.get_corpus_metadata_by_type(corpus_type, conn)
            if rows ==[]:
                raise Exception("ENter valid corpus name")
            output=""
            # str1={}
            for row in rows:
                output={
                    "corpus_id":row['corpus_id'],
                    "corpus_name":row['corpus_name'],
                    "language":row['language'],
                    "corpus_type":row['corpus_type'],
                    "source_type":row['source_type'],
                    "customer_name":row['customer_name'],
                    "data_domain_name":row['data_domain_name']
                }
                # str1=((x, y) for x, y in output )
            response=json.dumps(output)
#            for i in response:
 #               print(i)
            return response
        except Exception as e:
            raise e

    def create_corpus(self, json_loader,target):
        try:
            corpusRepositoryManager1 = CorpusRepositoryManager()
            corpusRepositoryManager1.init()
            corpusRepositoryManager1.get_url(target)
            corpusMetadataManager = CorpusMetadataManager()
            corpusMetadataManager.create_corpus(json_loader, conn)

        except Exception as e:
            raise e

    def add_repo(self, target):
        try:
            corpusRepositoryManager1 = CorpusRepositoryManager()
            corpusRepositoryManager1.add(target)
        except Exception as e:
            raise e

    def commit_repo(self, str1):
        try:
            corpusRepositoryManager1 = CorpusRepositoryManager()
            corpusRepositoryManager1.commit(str1)
        except Exception as e:
            raise e

    def remote_repo(self, name,data, gita):
        try:
            corpusRepositoryManager1 = CorpusRepositoryManager()
            corpusRepositoryManager1.remote(name,data,gita)
            corpusMetadataManager=CorpusMetadataManager()
            corpusMetadataManager.update_corpus_remote(name,data,gita,conn)
        except Exception as e:
            raise e

    def clone_repo(self, args):
        try:
            CorpusRepositoryManager1 = CorpusRepositoryManager()
            CorpusRepositoryManager1.clone(args)
        except Exception as e:
            raise e

    def datareader(self, corpus_name, schema_type, custom_schema):
        try:
            CorpusDataReaderManager1 = CorpusDataReaderManager()
            path = os.getcwd()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            output = {"template_file_path": [],"data_dir_path":[], "common_schema": [], "native_schema": []}
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        
            cursor.execute("select * from corpus_metadata where corpus_name='" + corpus_name + "'")
            row = cursor.fetchone()
            cursor.execute("select * from corpus_custom_fields where corpus_id='" + str(row["corpus_id"]) + "'")
            result = cursor.fetchall()
            response=prop.input_properties(path,corpus_name,output,result)
            
            dataset = CorpusDataReaderManager1.read_data(corpus_name,response, schema_type, custom_schema=custom_schema)['data']
            return dataset
            # if corpus_name == "timit":
            #     response = {
            #         "template_file_path": dir_path + "/poc/librispeec/asr/template_timit.py",
            #         "data_dir_path": os.getcwd() + "/timit",
            #         "common_schema": dir_path + "/common_schema.json",
            #         "native_schema": dir_path + "/poc/output_schema_timit.json"
            #     }
            # elif corpus_name == "librispeech":
            #     response = {
            #         "template_file_path": dir_path + "/poc/librispeech/asr/template_librispeech.py",
            #         "data_dir_path": os.getcwd() + "/librispeech",
            #         "common_schema": dir_path + "/common_schema.json",
            #         "native_schema": dir_path + "/poc/output_schema_librispeech.json"
            #     }
            # elif corpus_name == corpus_name:
            #     print(dir_path + "/poc/hinglish/native_schema.json")
            #     response = {
            #         "template_file_path": dir_path+"",
            #         "data_dir_path": "C:\\Users\\AtharvaBokare(c)\\PycharmProjects\\siddhant_code\\data-ops\\hinglish",
            #         "common_schema": "C:\\Users\\AtharvaBokare(c)\\PycharmProjects\\data_ops\\src\\main\\poc\\hinglish\\native_schema.json",
            #         "native_schema": "C:\\Users\\AtharvaBokare(c)\\PycharmProjects\\data_ops\\src\\main\\poc\\hinglish\\native_schema.json"
            #     }
            # else:
            #     return ("invalid corpus name")
            #
            # dataset = CorpusDataReaderManager1.read_data(response, schema_type, custom_schema=custom_schema)['data']
            # print("1.2")
            #
            # return dataset
        except Exception as e:
            raise e

    def store_data(self, corpus_name, output_loc, schema_type, custom_schema=None):
        try:
            CorpusDataReaderManager1 = CorpusDataReaderManager()
            CorpusDataReaderManager1 = CorpusDataReaderManager()
            path = os.getcwd()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            output = {"template_file_path": [],"data_dir_path":[], "common_schema": [], "native_schema": []}
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("select * from corpus_metadata where corpus_name='" + corpus_name + "'")
            row = cursor.fetchone()
            cursor.execute("select * from corpus_custom_fields where corpus_id='" + str(row["corpus_id"]) + "'")
            result = cursor.fetchall()
            response=prop.input_properties(path,corpus_name,output,result)

#            if corpus_name == "timit":
 #               response = {
  #                  "template_file_path": dir_path + "/poc/librispeec/asr/template_timit.py",
   #                 "data_dir_path": os.getcwd() + "/timit",
    #                "common_schema": dir_path + "/common_schema.json",
     #               "native_schema": dir_path + "/poc/output_schema_timit.json"
      #          }
       #     elif corpus_name == "librispeech":
        #        response = {
         #           "template_file_path": dir_path + "/poc/librispeech/asr/template_librispeech.py",
          #          "data_dir_path": os.getcwd() + "/librispeech",
           #         "common_schema": dir_path + "/common_schema.json",
             #       "native_schema": dir_path + "/poc/output_schema_librispeech.json"
           #     }
            #elif corpus_name == "hinglish":
             #   response = {
              #      "template_file_path": dir_path + "/poc/hinglish/template_hinglish.py",
               #     "data_dir_path": os.getcwd() + "/hinglish",
                #    "common_schema": dir_path + "/poc/hinglish/native_schema.json",
                 #   "native_schema": dir_path + "/poc/hinglish/native_schema.json"
                #}
         #   else:
          #      return ("invalid corpus name")

            if output_loc == ".":
                output_loc = os.getcwd()

            if schema_type == "custom":
                if custom_schema is not None:
                    dataset = CorpusDataReaderManager1.store_data(response, output_loc, schema_type, custom_schema)
                else:
                    return ("invalid custom_schema path")
            else:
                dataset = CorpusDataReaderManager1.store_data(response, output_loc, schema_type)

            return dataset
        except Exception as e:
            raise e

    def push_remote(self):
        try:
            connection = Connection()
            corpusRepositoryManager1 = CorpusRepositoryManager()
            corpusRepositoryManager1.push()
            corpusMetadataManager = CorpusMetadataManager()
            # print("xvz")
            # corpusMetadataManager.update_timestamp(conn,args)
        except Exception as e:
            raise e

    def pull_repo(self, audio):
        try:
            corpusRepositoryManager1 = CorpusRepositoryManager()
            corpusRepositoryManager1.pull(audio)
        except Exception as e:
            raise e

