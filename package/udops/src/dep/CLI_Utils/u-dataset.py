import typer as typer
from Handler.DatasetHandler import *
import json
from typing import Optional
from typing import List
from typing import Dict

app = typer.Typer()
dataset_handler = DatasetHandler()

try:
    @app.command()
    def create_dataset_by_list(dataset_name: str, custom_field_file: str, output_file: str, schema_type_args: str,
                               list_json: List[str]):
        print("12")
        dataset_custom_properties = json.load(open(custom_field_file, 'r'))
        dataset_handler.create_dataset(dataset_name,dataset_custom_properties, output_file,
                                       schema_type_args,list_json)


    @app.command()
    def create_dataset_by_filter(file: str, dataset_name: str, output_file: str,
                                 schema_type_args: Optional[str] = typer.Argument("common"),
                                 custom_schema: Optional[str] = typer.Argument(None)):
        dataset_properties = json.load(open(file, 'r'))
        dataset_handler.create_dataset_by_filter(dataset_properties, dataset_name, output_file, schema_type_args,
                                                 custom_schema)


    @app.command()
    def listDatasetNames(corpus_type: str, properties_file: str, detailed_flag: str = ""):
        dataset_props = json.load(open(properties_file, 'r'))
        result = dataset_handler.list_dataset_names(corpus_type, dataset_props, detailed_flag)


    @app.command()
    def getDatasetMetadata(dataset_id: int, dataset_name: str):
        result = dataset_handler.get_dataset_metadata(dataset_id, dataset_name)
        for i in result:
            print(i)


    @app.command()
    def getDatasetCorpora(dataset_id: int):
        result = dataset_handler.get_dataset_corpora(dataset_id)
        for i in result:
            print(i)


    @app.command()
    def dataset_reader(dataset_name: str, schema_type_args: Optional[str] = typer.Argument("common"),
                       custom_schema: Optional[str] = typer.Argument(None)):
        print(schema_type_args, dataset_name)
        dataset_handler.dataset_reader(dataset_name, schema_type_args)

except Exception as e:
    raise e
if __name__ == '__main__':
    app()
