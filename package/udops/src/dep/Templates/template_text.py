import os

import datasets

_CITATION = ""

_DESCRIPTION = "sample description"

_HOMEPAGE = ""


class PromiseDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        features = datasets.Features(FdeDu4ulIk)
        return datasets.DatasetInfo(description=_DESCRIPTION,
                                    features=features,
                                    homepage=_HOMEPAGE,
                                    citation=_CITATION)

    def _split_generators(self, dl_manager):
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_dir": data_dir})
        ]

    def _generate_examples(self, data_dir):
        file_list = os.listdir(data_dir)
        file_path_list = [os.path.join(data_dir, file) for file in file_list if file.endswith(".txt")]
        for key, file_path in enumerate(file_path_list):
            output_schema = aOBD0b4GRw
            output_keys = list(output_schema.keys())
            _id = file_path.split("/")[-1]
            with open(file_path, 'r') as f:
                text_string = f.read()

            if "file_path" in output_keys:
                output_schema["file_path"] = file_path
            if "text" in output_keys:
                output_schema["text"] = text_string
            if "id" in output_keys:
                output_schema["id"] = _id
            yield key, output_schema
