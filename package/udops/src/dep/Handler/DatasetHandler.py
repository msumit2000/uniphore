from udops.src.dep.Manager.DatasetMetadatamanager import *

from udops.src.dep.Manager.DatasetReaderManager import *
import os
import shutil
from udops.src.dep.Manager.CorpusRepositoryManager import *
from udops.src.dep.Manager.DatasetRepositoryManager import *

datasetMetadatManager1 = DatasetMetadatamanager()
corpusMetadataManager = CorpusMetadataManager()
corpusDataReaderManager = CorpusDataReaderManager()
datasetReaderManager = DatasetReaderManager()
corpusReposirtoyManager = CorpusRepositoryManager()
datasetRepomanager = DatasetRepositoryManager()


class DatasetHandler:
    def create_dataset(self, dataset_name, list_corpus,schema_type_args, custom_field_file,training_corpus):
        try:

            resp = datasetMetadatManager1.list_dataset_by_name(dataset_name, list_corpus)
            datasetMetadatManager1.create_dataset(dataset_name, resp, list_corpus, custom_field_file,training_corpus)
        except Exception as e:
            raise e

    def create_dataset_by_filter(self, filter_value, file, dataset_name, corpus_type, schema_type,
                                 custom_schema,training_corpus):  # two args filter properties and other properties cutom must be optional
        try:
            corpus_list = datasetMetadatManager1.list_corpus_names(str(filter_value))
            datasetMetadatManager1.create_dataset_by_filter_ds(corpus_list, dataset_name, filter_value,corpus_type, file,training_corpus)
        except Exception as e:
            raise e
        
    def get_Counts(self):
        try:
            dataset = DatasetMetadatamanager()
            return dataset.get_Counts()
        except Exception as e:
            raise e

    def list_dataset_names(self, corpus_type, json_loader, detailed_flag):
        try:

            result = datasetMetadatManager1.list_dataset_names_ds(corpus_type, json_loader, detailed_flag)
            return result
        except Exception as e:
            raise e
    
    def dataset_custom_fields(self, datasetname, kv_pairs):
        try: 
            result = datasetMetadataManager1.dataset_custom_list(datasetname, kv_pairs)
        except Exception as e:
            raise e

    def store_dataset(self, dataset_name, output_file_path, schema_type_args, custom_schema):
        try:
            #            resp=datasetMetadatManager1.list_dataset_by_name(conn,dataset_name,list_corpus)
            datasetReaderManager.create_dataset_manager(dataset_name, output_file_path,schema_type_args,custom_schema)
            # datasetReaderManager.dataset_store(dataset_name, output_file_path, schema_type_args, custom_schema,resp)
        except Exception as e:
            raise e

    def get_dataset_metadata(self,  dataset_name):
        try:
            result = datasetMetadatManager1.get_dataset_metadata(dataset_name)
            return result
        except Exception as e:
            raise e

    def get_dataset_corpora(self, dataset_id):
        try:
            result = datasetMetadatManager1.get_dataset_corpora(dataset_id)
            return result
        except Exception as e:
            raise e

    def init_dataset(self):
        try:
            datasetRepomanager.init_dataset()
        except Exception as e:
            raise e

    def add(self, target):
        try:
            datasetRepomanager.add_dataset(target)
        except Exception as e:
            raise e

    def commit(self, args1):
        try:
            datasetRepomanager.commit_dataset(args1)
        except Exception as e:
            raise e

    def remote(self, remote_location, git_remote):
        try:
            datasetRepomanager.remote_dataset(remote_location, git_remote)
        except Exception as e:
            raise e

    def push(self):
        try:
            datasetRepomanager.push_dataset()
        except Exception as e:
            raise e

    def clone(self, repo):
        try:
            datasetRepomanager.clone_dataset(repo)
        except Exception as e:
            raise e

    def pull(self):
        try:
            datasetRepomanager.clone_dataset()
        except Exception as e:
            raise e
    def generate_output(self,dataset_name,schema,custom_field):
        try:
            datasetReaderManager.generate_output(dataset_name,schema,custom_field)
        except Exception as e:
            raise e


    ############ dataset upi ############

    def get_summary(self,dataset_name):
        dataset = DatasetMetadatamanager()
        return dataset.get_summary(dataset_name)

    def get_list(self):
        dataset = DatasetMetadatamanager()
        return dataset.get_list()

    def search_dataset(self,property):
        dataset = DatasetMetadatamanager()
        return dataset.search_dataset(property)

    def update(self,name,value):
        dataset = DatasetMetadatamanager()
        if  dataset.update(name,value)==1:
            return 1
        else:
            return 2

    def dataset_corpus_list(self,dataset_name):
        dataset = DatasetMetadatamanager()
        return dataset.dataset_corpus_list(dataset_name)

