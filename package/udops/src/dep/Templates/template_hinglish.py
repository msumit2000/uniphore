import json
import os
from functools import reduce
from pathlib import Path

import datasets
from datasets.tasks import AutomaticSpeechRecognition

_CITATION = ""

_DESCRIPTION = "sample description"

_HOMEPAGE = ""


class HinglishDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        features = datasets.Features(FdeDu4ulIk)
        # features = datasets.Features(
        #     {
        #         "file": datasets.Value("string"),
        #         "audio": datasets.Audio(sampling_rate=16_000),
        #         "text": datasets.Value("string"),
        #         "transcription_detail":
        #             datasets.Sequence(
        #             {
        #                 "start_time": datasets.Value("string"),
        #                 "end_time": datasets.Value("string"),
        #                 "transcription": datasets.Value("string"),
        #             }
        #         ),
        #         "id": datasets.Value("string"),
        #     })

        return datasets.DatasetInfo(description=_DESCRIPTION,
                                    features=features,
                                    supervised_keys=("file", "text"),
                                    homepage=_HOMEPAGE,
                                    citation=_CITATION,
                                    task_templates=[
                                        AutomaticSpeechRecognition(audio_column="audio", transcription_column="text")],
                                    )

    def _split_generators(self, dl_manager):
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_dir": data_dir})
        ]

    def _generate_examples(self, data_dir):
        audio_path = os.path.join(data_dir, 'audio')
        print(audio_path)
        lst_1 = os.listdir(audio_path)
        audio_lst = [file for file in lst_1 if file.endswith(".wav")]
        transcript_path = os.path.join(data_dir, 'transcripts', 'json')
        lst_2 = os.listdir(transcript_path)
        transcript_lst = [os.path.join(transcript_path, file) for file in lst_2 if file.endswith(".json")]
        for key, audio in enumerate(audio_lst):
            output_schema = aOBD0b4GRw
            audio_flag = False
            for json_file_path in transcript_lst:
                json_file = json.load(open(json_file_path, encoding='utf-8'))
                for row in json_file:
                    if row["original_filename"] == audio:
                        audio_flag = True
                        id_ = audio.split(".wav")[0]
                        audio_file = os.path.join(audio_path, audio)
                        segmentations = row["segmentations"]
                        transcription = []
                        details = []
                        for segment in segmentations:
                            detail = {}
                            transcription.append(segment['transcription'])
                            detail['start_time'] = segment['start_time']
                            detail['end_time'] = segment['end_time']
                            detail['transcription'] = segment['transcription']
                            details.append(detail)
                        # transcription = " ".join(transcription)
                        transcription = reduce(lambda str1, str2: str1 + " " + str2, transcription)
                        # output_schema['audio'] = os.path.join(transcript_path, audio)
                        with open(audio_file, "rb") as f:
                            file = f.read()
                        # output_schema['audio'] = {"path": audio_file, "bytes": file}
                        output_schema['audio'] = audio_file
                        output_keys = list(output_schema.keys())
                        if "id" in output_keys:
                            output_schema['id'] = id_
                        if "file" in output_keys:
                            output_schema['file'] = audio_file
                        if "text" in output_keys:
                            output_schema['text'] = transcription
                        if "transcription_detail" in output_keys:
                            output_schema['transcription_detail'] = details
                    if audio_flag:
                        break
                if audio_flag:
                    break
            yield key, output_schema
