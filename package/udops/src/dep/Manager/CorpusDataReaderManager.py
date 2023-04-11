import json
from pprint import pprint

from udops.src.dep.poc.librispeech.asr.asr_data_reader import ASRDataReader
from udops.src.dep.Manager.CorpusMetadataManager import *
corpus_metadat_manager=CorpusMetadataManager()
from udops.src.dep.config.Connection import *
connection = Connection()
conn=connection.get_connection()
class CorpusDataReaderManager:
    def store_data(self, corpus_name,corpus_details, output_location, schema_type, custom_schema=None):
        response = self.read_data(corpus_name,corpus_details, schema_type, custom_schema)
        conn=connection.get_connection()
    
        if response['status'] == "success":
            dataset_list = response['data']
            with open(output_location, 'w') as f:
                json.dump(dataset_list, f)
               # corpus_metadat_manager.insert_file_path(conn,str(output_location))
            return {'status': 'success', 'error': ''}
        else:
            return response

    def read_data(self,corpus_name,corpus_details, schema_type, custom_schema=None):
      #  corpus_details = corpusId
        if schema_type == "native":
            custom_schema = corpus_details['native_schema']
        elif schema_type == "common":
            custom_schema = corpus_details['common_schema']
        elif schema_type == "custom":
            pass
        else:
            return {'status': 'failed', 'error': 'invalid input', 'data': []}
        
        output_schema = self.get_output_schema(corpus_name,custom_schema)
        template_file_path = corpus_details['template_file_path']
        data_dir_path = corpus_details['data_dir_path']

        dataset = ASRDataReader().read_all_records(output_schema, data_dir_path, template_file_path)
        dataset_list = ASRDataReader().get_dataset_as_json(dataset)
        return {'status': 'success', 'error': '', 'data': dataset_list}

#    def get_output_schema(self, file_path):
 #       output_schema = json.load(open(file_path[0]))
  #      return output_schema['asr']
    def get_output_schema(self,corpus_name, file_path):

        corpus_detail=corpus_metadat_manager.get_corpus_metadata_by_id(corpus_name,conn)
        output_schema = json.load(open(file_path[0]))
    
        for corpus in corpus_detail:
        
            return output_schema[corpus['corpus_type']]
