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


    def getCorpusMetadata(corpus_id: str):  # take one argument
        corpus_handler = CorpusHandler()
        row=corpus_handler.get_corpus_metadata(corpus_id)
        return row

    def getCorpusMetadatabytype(corpus_type: str):
        corpus_handler = CorpusHandler()
        row = corpus_handler.manager_get_metadata_type(corpus_type)
  #      print(row)
        return row
        


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


    def push():
        corpus_handler = CorpusHandler()
        corpus_handler.push_remote()


    def pull(audio):
        corpus_handler = CorpusHandler()
        corpus_handler.pull_repo(audio)


    def update_corpus(self,file: str):
        corpus_handler = CorpusHandler()
        corpus_properties = json.load(open(file, 'r', encoding='utf-8'))
        str1 = corpus_handler.manager_update_corpus(corpus_properties)

    def datareader(corpus_details_dict, schema_type : Optional[str] =typer.Argument("common"),custom_schema:Optional[str] =typer.Argument(None)):
        corpus_handler = CorpusHandler()
        corpus_handler.datareader(corpus_details_dict, schema_type,custom_schema)
    
    def store_data(corpus_details_dict, output_loc, schema_type : Optional[str] =typer.Argument("common"), custom_schema:Optional[str] =typer.Argument(None) ):
        corpus_handler = CorpusHandler()
        corpus_handler.store_data(corpus_details_dict,output_loc,schema_type,custom_schema)


if __name__ == '__main__':
    app()
