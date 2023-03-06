import os

import datasets
import pandas as pd

_CITATION = ""

_DESCRIPTION = "sample description"

_HOMEPAGE = ""


class PromiseDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        features = datasets.Features(FdeDu4ulIk)
        # features = datasets.Features(
        #     {
        #         "annotation": datasets.Value("string"),
        #         "annotation_session": datasets.Value("string"),
        #         "dataset": datasets.Value("string"),
        #         "answer": datasets.Value("string"),
        #         "transcript_id": datasets.Value("string"),
        #         "file_source": datasets.Value("float64"),
        #         "turn_id": datasets.Value("int64"),
        #         "speaker": datasets.Value("string"),
        #         "text": datasets.Value("string"),
        #         "tags": datasets.Value("string"),
        #         "turn_labels": datasets.Value("string"),
        #         "has_tag": datasets.Value("bool"),
        #         "source": datasets.Value("string"),
        #         "token_tags": datasets.Value("string"),
        #         "biluo_tags": datasets.Value("string")
        #     })
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
        print('data_dir')
        file_list = os.listdir(data_dir)
        file_path_list = [os.path.join(data_dir, file) for file in file_list if file.endswith(".csv")]
        id_ = 0
        for file_path in file_path_list:
            output_schema = aOBD0b4GRw
            output_keys = list(output_schema.keys())
            dataframe = pd.read_csv(file_path)
            for index, row in dataframe.iterrows():
                if "annotation" in output_keys:
                    output_schema["annotation"] = row["annotation"]
                if "annotation_session" in output_keys:
                    output_schema["annotation_session"] = row["annotation_session"]
                if "dataset" in output_keys:
                    output_schema["dataset"] = row["dataset"]
                if "answer" in output_keys:
                    output_schema["answer"] = row["answer"]
                if "transcript_id" in output_keys:
                    output_schema["transcript_id"] = row["transcript_id"]
                if "file_source" in output_keys:
                    output_schema["file_source"] = row["file_source"]
                if "turn_id" in output_keys:
                    output_schema["turn_id"] = row["turn_id"]
                if "speaker" in output_keys:
                    output_schema["speaker"] = row["speaker"]
                if "text" in output_keys:
                    output_schema["text"] = row["text"]
                if "tags" in output_keys:
                    output_schema["tags"] = row["tags"]
                if "turn_labels" in output_keys:
                    output_schema["turn_labels"] = row["turn_labels"]
                if "has_tag" in output_keys:
                    output_schema["has_tag"] = row["has_tag"]
                if "source" in output_keys:
                    output_schema["source"] = row["source"]
                if "token_tags" in output_keys:
                    output_schema["token_tags"] = row["token_tags"]
                if "biluo_tags" in output_keys:
                    output_schema["biluo_tags"] = row["biluo_tags"]
                yield id_, output_schema
                id_ += 1


if __name__ == '__main__':
    path = r"C:\Users\PrateekTiwari(c)\Documents\drive\data\promise_data\Annotations-cricket_promise_20220406.csv"
    df = pd.read_csv(path)
    column_names = df.columns.values.tolist()
    for index, row in df.iterrows():
        output_schema = {}
