from udops.src.dep.Handler.CorpusHandler import *

import shutil
from typing import Optional
import typer

class ucorpus:
    def listCorpusNames(filter_value):
  #      typer.echo("load test")
#        print(filter_value)
        corpus_handler = CorpusHandler()
        response = corpus_handler.list_corpus_names(filter_value)
        #for row in response:
        #    print("Result :", row)


    def getCorpusMetadata(corpus_name):  # take one argument
        corpus_handler = CorpusHandler()
        row=corpus_handler.get_corpus_metadata(corpus_name)
        print(row)
        return row

    def getCorpusMetadatabytype(corpus_type: str):
        corpus_handler = CorpusHandler()
        row = corpus_handler.manager_get_metadata_type(corpus_type)
  #      print(row)
        return row
        

    def RDSConfig(host,dbname , user, password):
        corpus_handler = CorpusHandler()
        corpus_handler.RDSConfig(host = host , dbname = dbname , user = user , password = password)

    def corpus_custom_fields(corpusname , kv_pairs):
        corpus_handler = CorpusHandler()
        corpus_handler.corpus_custom_fields(corpusname , kv_pairs)
     
    def list_corpus(self):
        corpus_handler = CorpusHandler()
        corpus_handler.list_commits()

    def checkout(commitid):
        corpus_handler = CorpusHandler()
        corpus_handler.checkout(commitid)

    def delete_corpus(corpusname):
        corpus_handler = CorpusHandler()
        corpus_handler.delete_corpus(corpusname)

    def init(file,target):
        corpus_handler = CorpusHandler()
        corpus_properties = file
        corpus_handler.create_corpus(corpus_properties,target)
        print("Config written")


    def add(target: str):
        corpus_handler = CorpusHandler()
        corpus_handler.add_repo(target)
    
    def clone(args:str):
        corpus_handler = CorpusHandler()
        corpus_handler.clone_repo(args)


    def commit(message: str):
        corpus_handler = CorpusHandler()
        corpus_handler.commit_repo(message)


    def remote(name:str,data: str, gita: str):
        corpus_handler = CorpusHandler()
        corpus_handler.remote_repo(name,data,gita)


    def push(self):
        corpus_handler = CorpusHandler()
        corpus_handler.push_remote()


    def pull(audio):
        corpus_handler = CorpusHandler()
        corpus_handler.pull_repo(audio)


    # def update_corpus(self,file: str):
    #     corpus_handler = CorpusHandler()
    #     corpus_properties = json.load(open(file, 'r', encoding='utf-8'))
    #     str1 = corpus_handler.manager_update_corpus(corpus_properties)

    def datareader(corpus_details_dict, schema_type : Optional[str] =typer.Argument("common"),custom_schema:Optional[str] =typer.Argument(None)):
        corpus_handler = CorpusHandler()
        corpus_handler.datareader(corpus_details_dict, schema_type,custom_schema)
    
    def store_data(corpus_details_dict, output_loc, schema_type : Optional[str] =typer.Argument("common"), custom_schema:Optional[str] =typer.Argument(None) ):
        corpus_handler = CorpusHandler()
        corpus_handler.store_data(corpus_details_dict,output_loc,schema_type,custom_schema)

    def get_Counts(self):
        corpus_handler = CorpusHandler()
        return corpus_handler.get_Counts()

    def summary(self, column):
        corpus_handler = CorpusHandler()
        return corpus_handler.summary(column)

    def list_corpus(self):
        corpus_handler = CorpusHandler()
        return corpus_handler.list_corpus()

    def search_corpus(self, corpus_name):
        corpus_handler = CorpusHandler()
        if corpus_handler.search_corpus(corpus_name) == 0:
            return 0
        else:
            return corpus_handler.search_corpus(corpus_name)

    def update_corpus(self, data):
        corpus_handler = CorpusHandler()
        if corpus_handler.update_corpus(data) == 1:
            return 1
        else:
            return 0

    def donut(self, column):
        corpus_handler = CorpusHandler()
        return corpus_handler.donut(column)

    def summary_custom(self, corpus_name):
        corpus_handler = CorpusHandler()
        return corpus_handler.summary_custom(corpus_name)

    def update_custom_field(self, data):
        corpus_handler = CorpusHandler()
        if corpus_handler.update_custom_field(data) == 1:
            return 1
        else:
            return 2

if __name__ == '__main__':
    ucorpus()
