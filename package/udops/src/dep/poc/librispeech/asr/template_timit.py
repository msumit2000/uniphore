# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""TIMIT automatic speech recognition dataset."""

import os
from pathlib import Path

import datasets
from datasets.tasks import AutomaticSpeechRecognition

_CITATION = """\
@inproceedings{
  title={TIMIT Acoustic-Phonetic Continuous Speech Corpus},
  author={Garofolo, John S., et al},
  ldc_catalog_no={LDC93S1},
  DOI={https://doi.org/10.35111/17gk-bn40},
  journal={Linguistic Data Consortium, Philadelphia},
  year={1983}
}
"""

_DESCRIPTION = """\
The TIMIT corpus of reading speech has been developed to provide speech data for acoustic-phonetic research studies
and for the evaluation of automatic speech recognition systems.

TIMIT contains high quality recordings of 630 individuals/speakers with 8 different American English dialects,
with each individual reading upto 10 phonetically rich sentences.

More info on TIMIT dataset can be understood from the "README" which can be found here:
https://catalog.ldc.upenn.edu/docs/LDC93S1/readme.txt
"""

_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC93S1"


class TimitASR(datasets.GeneratorBasedBuilder):
    """TimitASR dataset."""

    @property
    def manual_download_instructions(self):
        return (
            "To use TIMIT you have to download it manually. "
            "Please create an account and download the dataset from https://catalog.ldc.upenn.edu/LDC93S1 \n"
            "Then extract all files in one folder and load the dataset with: "
            "`datasets.load_dataset('timit_asr', data_dir='path/to/folder/folder_name')`"
        )

    def _info(self):
        features = datasets.Features(FdeDu4ulIk)

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

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('timit_asr', data_dir=...)` that includes files unzipped from the TIMIT zip. Manual download instructions: {self.manual_download_instructions}"
            )

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"split": "train", "data_dir": data_dir}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"split": "test", "data_dir": data_dir}),
        ]

    def _generate_examples(self, split, data_dir):
        # Iterating the contents of the data to extract the relevant information
        wav_paths = sorted(Path(data_dir).glob(f"**/{split}/**/*.wav"))
        wav_paths = wav_paths if wav_paths else sorted(Path(data_dir).glob(f"**/{split.upper()}/**/*.WAV"))
        for key, wav_path in enumerate(wav_paths):
            output_schema = aOBD0b4GRw
            # extract transcript
            txt_path = with_case_insensitive_suffix(wav_path, ".txt")
            with txt_path.open(encoding="utf-8") as op:
                transcript = " ".join(op.readlines()[0].split()[2:])  # first two items are sample number

            # extract phonemes
            phn_path = with_case_insensitive_suffix(wav_path, ".phn")
            with phn_path.open(encoding="utf-8") as op:
                phonemes = [
                    {
                        "start": i.split(" ")[0],
                        "stop": i.split(" ")[1],
                        "utterance": " ".join(i.split(" ")[2:]).strip(),
                    }
                    for i in op.readlines()
                ]

            # extract words
            wrd_path = with_case_insensitive_suffix(wav_path, ".wrd")
            with wrd_path.open(encoding="utf-8") as op:
                words = [
                    {
                        "start": i.split(" ")[0],
                        "stop": i.split(" ")[1],
                        "utterance": " ".join(i.split(" ")[2:]).strip(),
                    }
                    for i in op.readlines()
                ]

            dialect_region = wav_path.parents[1].name
            sentence_type = wav_path.name[0:2]
            speaker_id = wav_path.parents[0].name[1:]
            id_ = wav_path.stem
            output_keys = list(output_schema.keys())
            if "id" in output_keys:
                output_schema['id'] = id_
            if "speaker_id" in output_keys:
                output_schema['speaker_id'] = speaker_id
            if "file" in output_keys:
                output_schema['file'] = str(wav_path)
            if "text" in output_keys:
                output_schema['text'] = transcript
            if "phonetic_detail" in output_keys:
                output_schema['phonetic_detail'] = phonemes
            if "word_detail" in output_keys:
                output_schema['word_detail'] = words
            if "dialect_region" in output_keys:
                output_schema['dialect_region'] = dialect_region
            if "sentence_type" in output_keys:
                output_schema['sentence_type'] = sentence_type

            output_schema['audio'] = str(wav_path)

            yield key, output_schema


def with_case_insensitive_suffix(path: Path, suffix: str):
    path = path.with_suffix(suffix.lower())
    path = path if path.exists() else path.with_suffix(suffix.upper())
    return path
