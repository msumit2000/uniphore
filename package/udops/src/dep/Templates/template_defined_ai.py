import os
import json
import datasets
import pandas as pd

_CITATION = ""

_DESCRIPTION = "sample description"

_HOMEPAGE = ""


class DefinedAIDataset(datasets.GeneratorBasedBuilder):
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
        detail_list = []
        audio_path = os.path.join(data_dir, 'audio')
        lst_1 = os.listdir(audio_path)
        audio_lst = [file for file in lst_1 if file.endswith(".wav")]

        file_path_list = [os.path.join(path, file_name) for path, subdirs, files in os.walk(data_dir) for file_name in
                          files if file_name.endswith(".tsv")]

        for key, audio in enumerate(audio_lst):
            audio_file = os.path.join(audio_path, audio)
            output_schema = aOBD0b4GRw
            audio_flag = False
            # id_=0
            output_keys = list(output_schema.keys())
            id_ = audio.replace(".wav", "")

            for file_path in file_path_list:
                dataframe = pd.read_csv(file_path, sep="\t")
                rslt_df = dataframe[(dataframe['RecordingId']) == id_]
                native_keys = ['TranscriptionId', 'Channels', 'Channel', 'StartTime', 'EndTime', 'SegmentDuration',
                               'Transcription',
                               'RecordingId', 'Domain', 'Duration', 'SampleRate', 'BitDepth', 'AudioFileUrl',
                               'RelativeFileName',
                               'LeftChannelSpeakerId', 'LeftChannelNative', 'LeftChannelRole', 'LeftChannelSpeakerAge',
                               'LeftChannelSpeakerGender', 'LeftChannelSpeakerLivingCountry',
                               'LeftChannelSpeakerAccent',
                               'RightChannelSpeakerId', 'RightChannelNative', 'RightChannelRole',
                               'RightChannelSpeakerAge',
                               'RightChannelSpeakerGender', 'RightChannelSpeakerLivingCountry',
                               'RightChannelSpeakerAccent']

                for index, row in rslt_df.iterrows():
                    detail = {}
                    for key1 in native_keys:
                        detail[key1] = row[key1]
                    detail_list.append(detail)

                output_schema['audio'] = None

                if "id" in output_keys:
                    output_schema['id'] = id_
                if "file" in output_keys:
                    output_schema['file'] = audio_file
                if "transcription_detail" in output_keys:
                    output_schema['transcription_detail'] = detail_list
            yield id_, output_schema
            # id_ += 1

