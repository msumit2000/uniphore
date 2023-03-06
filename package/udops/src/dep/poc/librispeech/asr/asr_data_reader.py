import json
import os
from datetime import datetime
from pprint import pprint
import numpy as np
from datasets import load_dataset


class ASRDataReader:
    def read_all_records(self, output_schema, data_dir, template_file_path):
        temp_file_path = "reader-" + datetime.now().strftime('%Y%m%d%H%M%S') + ".py"
        try:
            self.__create_file(output_schema, data_dir[0], template_file_path[0], temp_file_path)
#            print( data_dir, template_file_path,temp_file_path)
            dataset = load_dataset(temp_file_path, data_dir=data_dir[0])
            return dataset
        except Exception as err:
            raise err
        finally:
            os.remove(temp_file_path)

    def __create_file(self, output_schema, data_dir, template_file_path, temp_file_path):
        default_output_schema = {}
        features = '{'
        for feature in output_schema:
            if feature['data_class'] == 'Sequence':
                features = features + "'" + feature['key'] + "':" + 'datasets.' + feature['data_class'] + "({"
                for row in feature['data_type']:
                    features = features + "'" + row['key'] + "':" + 'datasets.' + row['data_class'] + "('" + \
                               row['data_type'] + "'),"
                features = features + "}),"
                default_output_schema[feature['key']] = None
            elif feature['data_class'] != 'Audio':
                features = features + "'" + feature['key'] + "':" + 'datasets.' + feature['data_class'] + "('" + \
                           feature['data_type'] + "'),"
                default_output_schema[feature['key']] = None
            elif feature['data_class'] == 'Audio':
                features = features + "'" + feature['key'] + "':" + 'datasets.' + feature[
                    'data_class'] + "(sampling_rate=16_000),"

        features = features.rstrip(features[-1])
        features = features + '}'
        with open(template_file_path, 'r+') as f:
            file = f.read()
            row_lst = file.split("\n")
        with open(temp_file_path, 'wt') as fp:
            for row in row_lst:
                if row.__contains__("mpFsc8ZAaY"):
                    data_dir = "'" + data_dir + "'"
                    row = row.replace("mpFsc8ZAaY", data_dir)
                elif row.__contains__("aOBD0b4GRw"):
                    row = row.replace("aOBD0b4GRw", str(default_output_schema))
                elif row.__contains__("FdeDu4ulIk"):
                    row = row.replace("FdeDu4ulIk", features)
                fp.write("%s\n" % row)

    def get_dataset_as_json(self, dataset):
        dataset_list = []
        for split in dataset.keys():
            for record in dataset[split]._iter():
                record_string = json.dumps(record, cls=NumpyEncoder)
                record_dict = json.loads(record_string)
                dataset_list.append(record_dict)
        return dataset_list


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

