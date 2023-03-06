import typer as typer
from Handler.CorpusHandler import *
import shutil
from typing import Optional

app = typer.Typer()

try:
    @app.command()
    def listCorpusNames(filter_value: str = ""):
        typer.echo("load test")
        corpus_handler = CorpusHandler()
        response = corpus_handler.list_corpus_names(filter_value)
        for row in response:
            print("Result :", row)


    @app.command()
    def getCorpusMetadata(corpus_id: str):  # take one argument
        corpus_handler = CorpusHandler()
        corpus_handler.get_corpus_metadata(corpus_id)


    @app.command()
    def getCorpusMetadatabytype(corpus_type: str):
        corpus_handler = CorpusHandler()
        row = corpus_handler.manager_get_metadata_type(corpus_type)
        print(row)
        return row
        


    @app.command()
    def init(file: str):
        corpus_handler = CorpusHandler()
        corpus_properties = json.load(open(file, 'r'))
        corpus_handler.create_corpus(corpus_properties)
        print("Config written")


    @app.command()
    def add(target: str):
        corpus_handler = CorpusHandler()
        corpus_handler.add_repo(target)
    
    @app.command()
    def clone(args:str):
        corpus_handler = CorpusHandler()
        corpus_handler.clone_repo(args)


    @app.command()
    def commit(args: str, args2: str):
        corpus_handler = CorpusHandler()
        corpus_handler.commit_repo(args, args2)


    @app.command()
    def remote(name:str,args: str, args2: str):
        corpus_handler = CorpusHandler()
        corpus_handler.remote_repo(name,args, args2)


    @app.command()
    def push():
        corpus_handler = CorpusHandler()
        corpus_handler.push_remote()


    @app.command()
    def pull(args):
        corpus_handler = CorpusHandler()
        corpus_handler.pull_repo(args)


    @app.command()
    def update_corpus(file: str):
        corpus_handler = CorpusHandler()
        corpus_properties = json.load(open(file, 'r', encoding='utf-8'))
        str1 = corpus_handler.manager_update_corpus(corpus_properties)

    @app.command()
    # TODO : Small case underscores
    def datareader(corpus_details_dict, schema_type : Optional[str] =typer.Argument("common"),custom_schema:Optional[str] =typer.Argument(None)):
        corpus_handler = CorpusHandler()
        # Prepare corpus_details_dict
        # "template_file_path": "C:\\Users\\PrateekTiwari(c)\\Documents\\drive\\git\\data-ops\\poc\\librispeech\\asr\\template_timit.py",
        #  "data_dir_path": "C:\\\\Users\\\\PrateekTiwari(c)\\\\Documents\\\\drive\\data\\\\timit\\\\data",
        #  "common_schema": "C:\\Users\\PrateekTiwari(c)\\Documents\\drive\\git\\data-ops\\common_schema.json",
        #  "native_schema": "C:\\Users\\PrateekTiwari(c)\\Documents\\drive\\git\\data-ops\\poc\\librispeech\\asr\\output_schema_timit.json"
        # Where will it come from?
        # template_file_path : <cwd>/.template/__<type>_data_reader.py
        # data_dir_path : <cwd>
        # common_schema : Should be derived from corpus_type within ReaderManager
        # native_schema ; <cwd>/.template/__native_schema.json
        corpus_handler.datareader(corpus_details_dict, schema_type,custom_schema)
    
    @app.command()
    def store_data(corpus_details_dict, output_loc, schema_type : Optional[str] =typer.Argument("common"), custom_schema:Optional[str] =typer.Argument(None) ):
        corpus_handler = CorpusHandler()
        corpus_handler.store_data(corpus_details_dict,output_loc,schema_type,custom_schema)

    @app.command()
    def register_reader(reader_template_fpath):
        # TODO : Copy files from above locations to ./template/ directory
        data_dir = os.getcwd()
        rel_path = data_dir + "/template/"
        if rel_path.endswith('.py') == False:
            print(rel_path.endswith('.py'))
            shutil.copy(reader_template_fpath,rel_path)
        else: 
            pass

except Exception as e:
    print(e)

if __name__ == '__main__':
    app()
