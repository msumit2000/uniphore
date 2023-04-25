
from udops.src.dep.Handler.DatasetHandler import * 
import json
from typing import Optional
from typing import List
from typing import Dict
import typer

dataset_handler = DatasetHandler()


class udataset:
    def create_dataset_by_list(dataset_name,input_list,custom_field_file,schema_type_args,training_corpus):
        dataset_handler.create_dataset(dataset_name, input_list, custom_field_file, schema_type_args,training_corpus)



    def create_dataset_by_filter(filter_value: str,custom_property: str,dataset_name: str,corpus_type: str,schema_type_args:str,custom_schema:str,training_corpus):
        
        dataset_handler.create_dataset_by_filter(filter_value, custom_property, dataset_name, corpus_type,
                                                  schema_type_args,
                                                 custom_schema,training_corpus)
    def store_dataset(dataset_name: str,output_path: str,schema_type_args:str,custom_schema:str):
        dataset_handler.store_dataset(dataset_name, output_path, schema_type_args, custom_schema)


    def dataset_custom_fields(datasetname, kv_pairs):
        dataset_handler.dataset_custom_fields(datasetname, kv_pairs)

    def listDatasetNames(corpus_type: str, properties_file: str, detailed_flag: str = ""):
   #     dataset_props = json.load(open(properties_file, 'r'))
        result = dataset_handler.list_dataset_names(corpus_type, properties_file, detailed_flag)


    def getDatasetMetadata(dataset_name: str):
        result = dataset_handler.get_dataset_metadata(dataset_name)
#        for i in result:
 #           print(i)
        return result

    def getDatasetCorpora(dataset_id):
        result = dataset_handler.get_dataset_corpora(dataset_id)
        for i in result:
            print(i['corpus_name'])


    def dataset_reader(dataset_name: str, schema_type_args: Optional[str] = typer.Argument("common"),
                       custom_schema: Optional[str] = typer.Argument(None)):
        dataset_handler.dataset_reader(dataset_name, schema_type_args)

    def generate_output(dataset_name,schema,custom_schema):
        try:
            dataset_handler.generate_output(dataset_name,schema,custom_schema)
        except Exception as e:
            raise e

if __name__ == '__main__':
    app()
