from udops.src.dep.ucorpus import ucorpus
from udops.src.dep.udataset import udataset
from typing import Optional, List
import re
from urllib.parse import urlparse, parse_qs
import shutil
import os
import typer
from datetime import datetime
app = typer.Typer(name="udops",add_completion=False,help="Udops utility")

try:
    @app.command()
    def RDSConfig(host: str = typer.Option(...,"--host"),
                  dbname: str = typer.Option(...,"--dbname"),
                  username: str = typer.Option(...,"--username"),
                  password: str = typer.Option(...,"--password")):
        ucorpus.RDSConfig(host = host , dbname = dbname , user = username, password = password)
    
    @app.command()
    def delete_corpus(corpusname):
        ucorpus.delete_corpus(corpusname)

    @app.command()
    def listCorpusNames(filter_value: str):
        ucorpus.listCorpusNames(filter_value)

    @app.command()
    def getCorpusMetadata(corpus_id: str):  # take one argument
        
        response=ucorpus.getCorpusMetadata(corpus_id)
        print(response)

    @app.command()
    def getCorpusMetadatabytype(corpus_type: str):
        response=ucorpus.getCorpusMetadatabytype(corpus_type)

    @app.command()
    def create_corpus(corpus_name: str = typer.Option(..., "--corpus_name") ,
                      corpustype: str = typer.Option(..., "--corpus_type"),
                    language : str = typer.Option(..., "--language"), template: str = typer.Option(..., "--template"),
                    native_schema: str = typer.Option(..., "--native_schema") , common_schema: str = typer.Option(..., "--common"), 
                    source:str = typer.Option(..., "--source_url"),
                    source_type:str = typer.Option(..., "--source_type") , vendor :str = typer.Option(..., "--vendor"),
                     domain: Optional[str] =typer.Option(None, "--domain"), 
                    description : Optional[str] = typer.Option(None,"--description" ), 
                    lang_code: str = typer.Option(..., "--lang_code") , 
                    acquisition_date: datetime = typer.Option(None,"--acquisition_date"), 
                    migration_date : datetime = typer.Option(None,"--migration_date")):
        if corpus_name == os.path.basename(os.getcwd()):
            a = os.path.basename(template)
            b = os.path.basename(native_schema)
            c = os.path.basename(common_schema)
            corpus_details = {
            "corpus_name": corpus_name,
            "corpus_type": corpustype,
            "language": language,
            "source_type": source_type,
            "vendor": vendor,
            "domain": domain,
            "description": description,
            "lang_code":lang_code,
            "acquisition_date": acquisition_date,
            "migration_date": migration_date,
            "custom_fields": [
                {
                    "field_name": "template_file_path",
                    "field_value": str(a)
                },
                {
                    "field_name": "native_schema",
                    "field_value": str(b)
                },
                {
                    "field_name": "common_schema",
                    "field_value": "/poc/promise/" + str(c)
                }
            ]

        }
            shutil.copy(template,os.getcwd())
            shutil.copy(native_schema,os.getcwd())
            shutil.copy(common_schema,os.path.dirname(os.path.realpath(__file__)) + "/src/dep/poc/promise/")
            ucorpus.init(corpus_details,source)
        else:
            return "Corpus name and folder name should be same"
    
    @app.command()
    def corpus_custom_fields(corpusname , data: List[str]):
        """
        Process multiple key-value pairs
        """
        """
        Map key-value pairs to a name
        """
        kv_pairs = dict()
        for i in data:
            for pair in i.split():
                key, value = pair.split('=')
                kv_pairs[key] = value
        ucorpus.corpus_custom_fields(corpusname , kv_pairs)
    
    @app.command()
    def dataset_custom_fields(datasetname , data:List[str]):
        kv_pairs = dict()
        for i in data:
            for pair in i.split():
                key , value = pair.split('=')
                kv_pairs[key] = value
        ucorpus.corpus_custom_fields(datasetname , kv_pairs)

    @app.command()
    def list_commits():
        ucorpus.list_corpus()

    @app.command()
    def checkout(commitid):
        ucorpus.checkout(commitid)

    @app.command()
    def add(target: str):
        ucorpus.add(target)
    
    @app.command()
    def remote(name : str, data: str, gita: str):
        if re.sub(r'^.*/(.*?)(\.git)?$', r'\1', gita) == os.path.basename(os.getcwd()):
            ucorpus.remote(name, data, gita)
        else: 
            return "Git Repository name should be same as Corpus name"

    @app.command()
    def commit(message: str):
        ucorpus.commit(message)
    
    @app.command()
    def push():
        ucorpus.push()

    @app.command()
    def save(message:str):
        ucorpus.commit(message)
        ucorpus.push()
    
    @app.command()
    def clone(git:str):
        ucorpus.clone(git)
    
    @app.command()
    def fetch(git:str,folder:Optional[str] =typer.Argument(None)):
        ucorpus.clone(git)
        s = re.sub(r'^.*/(.*?)(\.git)?$', r'\1', git)
        os.chdir(s)
        ucorpus.pull(folder)

    @app.command()
    def pull(folder: Optional[str] =typer.Argument(None)):
        
        ucorpus.pull(folder)

    @app.command()
    def datareader(corpus_details_dict, schema_type : Optional[str] =typer.Argument("common"),custom_schema:Optional[str] =typer.Argument(None)):
        ucorpus.datareader(corpus_details_dict, schema_type, custom_schema)

    @app.command()

    def export_data(corpus_details_dict, output_loc, schema_type : Optional[str] =typer.Argument("common"), custom_schema:Optional[str] =typer.Argument(None) ):
        ucorpus.store_data(corpus_details_dict,output_loc,schema_type,custom_schema)

    #Dataset Commands    
    @app.command()
    def create_dataset_by_list(dataset_name: str = typer.Option(..., "--dataset_name"),
                               custom_field_file: str = typer.Option(None, "--custom_property"),
                               schema_type_args: str = typer.Option("common", "--schema_type"),
                               list_json: str = typer.Option(..., "--list")):
        print("No Custom field")
        if custom_field_file != None:
            dataset_properties = json.loads(custom_field_file)
            udataset.create_dataset_by_list(dataset_name, list_json,schema_type_args, dataset_properties)
        else:
            dataset_properties = None
            udataset.create_dataset_by_list(dataset_name, list_json,schema_type_args, dataset_properties)
        print("dataset Created successfully")

    @app.command()
    def create_dataset_by_filter(filter_value: str = typer.Option(..., "--filter"),
                                 custom_property: str = typer.Option(None, "--custom_property"),
                                 dataset_name: str = typer.Option(..., "--dataset_name"),
                                 corpus_type: str = typer.Option(None, "--corpus_type"),
                                 schema_type_args: Optional[str] = typer.Option("common", "--schema"),
                                 custom_schema: Optional[str] = typer.Option(None, "--custom_schema")):

        # dataset_properties = json.load(open(file, 'r'))
        if custom_property != None:
            dataset_properties = json.loads(custom_property)
            udataset.create_dataset_by_filter(filter_value, dataset_properties, dataset_name, corpus_type,
                                                     schema_type_args,
                                                     custom_schema)
        else:
            dataset_properties = None
            udataset.create_dataset_by_filter(filter_value, dataset_properties, dataset_name, corpus_type,
                                                     schema_type_args,
                                                     custom_schema)


    @app.command()
    def export_dataset(dataset_name: str = typer.Option(..., "--dataset_name"),
                      output_path: str = typer.Option(None, "--output_path"),
                      schema_type_args: Optional[str] = typer.Option("common", "--schema"),
                      custom_schema: Optional[str] = typer.Option(None, "--custom_schema")):
        udataset.store_dataset(dataset_name, output_path, schema_type_args, custom_schema)


    @app.command()
    def listDatasetNames(corpus_type: str, properties_file: str, detailed_flag: str = ""):
        dataset_props = json.load(open(properties_file, 'r'))
        result = udataset.list_dataset_names(corpus_type, dataset_props, detailed_flag)


    @app.command()
    def getDatasetMetadata(dataset_name: Optional[str] = typer.Option(None, "--dataset_name")):
        result = udataset.getDatasetMetadata(dataset_name)
        for i in result:
            print(i)


    @app.command()
    def getDatasetCorpora(dataset_name: Optional[str] = typer.Option(None, "--dataset_name")):
        result = udataset.getDatasetCorpora(dataset_name)
#        for i in result:
 #           print(i)

    @app.command()
    def dataset_init():
        udataset.init_dataset()


    @app.command()
    def dataset_add(target: str):
        udataset.add(target)


    @app.command()
    def dataset_commit(message: str):
        udataset.commit(message)


    @app.command()
    def dataset_remote(remote_location: str, git_remote: str):
        udataset.remote(remote_location, git_remote)


    @app.command()
    def dataset_push():
        udataset.push()


    @app.command()
    def dataset_clone(repo: str):
        udataset.clone(repo)


    @app.command()
    def dataset_pull():
        udataset.pull()

    @app.command()
    def generate_output(dataset_name: str = typer.Option(None, "--dataset_name"),schema_type_args: Optional[str] = typer.Option("common", "--schema"),custom_schema: Optional[str] = typer.Option(None, "--custom_schema")):
        udataset.generate_output(dataset_name,schema_type_args,custom_schema)


except Exception as e:
    raise e

if __name__ == "__main__":
    app()

    
