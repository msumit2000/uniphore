import os

import datasets
from datasets.tasks import AutomaticSpeechRecognition

_CITATION = """\
@inproceedings{panayotov2015librispeech,
  title={Librispeech: an ASR corpus based on public domain audio books},
  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},
  booktitle={Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on},
  pages={5206--5210},
  year={2015},
  organization={IEEE}
}
"""

_DESCRIPTION = """\
LibriSpeech is a corpus of approximately 1000 hours of read English speech with sampling rate of 16 kHz,
prepared by Vassil Panayotov with the assistance of Daniel Povey. The data is derived from read
audiobooks from the LibriVox project, and has been carefully segmented and aligned.87
"""

_URL = "http://www.openslr.org/12"

_DL_URLS = mpFsc8ZAaY


class LibrispeechASR(datasets.GeneratorBasedBuilder):
    DEFAULT_WRITER_BATCH_SIZE = 256

    def _info(self):
        features = datasets.Features(FdeDu4ulIk)

        return datasets.DatasetInfo(description=_DESCRIPTION,
                                    features=features,
                                    supervised_keys=("file", "text"),
                                    homepage=_URL,
                                    citation=_CITATION,
                                    task_templates=[
                                        AutomaticSpeechRecognition(audio_column="audio", transcription_column="text")],
                                    )

    def _split_generators(self, dl_manager):
        archive_path = _DL_URLS
        # (Optional) In non-streaming mode, we can extract the archive locally to have actual local audio files:
        local_extracted_archive = dl_manager.extract(archive_path) if not dl_manager.is_streaming else {}
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "local_extracted_archive": local_extracted_archive,
                    "files": dl_manager.iter_archive(archive_path),
                },
            ),
        ]

    def _generate_examples(self, files, local_extracted_archive):
        """Generate examples from a LibriSpeech archive_path."""
        key = 0
        audio_data = {}
        transcripts = []
        for path, f in files:
            output_schema = aOBD0b4GRw
            if path.endswith(".flac"):
                id_ = path.split("/")[-1][: -len(".flac")]
                audio_data[id_] = f.read()
            elif path.endswith(".trans.txt"):
                for line in f:
                    if line:
                        line = line.decode("utf-8").strip()
                        id_, transcript = line.split(" ", 1)
                        audio_file = f"{id_}.flac"
                        speaker_id, chapter_id = [int(el) for el in id_.split("-")[:2]]
                        audio_file = (
                            os.path.join(local_extracted_archive, audio_file)
                            if local_extracted_archive
                            else audio_file
                        )
                        output_keys = list(output_schema.keys())
                        if "id" in output_keys:
                            output_schema['id'] = id_
                        if "speaker_id" in output_keys:
                            output_schema['speaker_id'] = speaker_id
                        if "chapter_id" in output_keys:
                            output_schema['chapter_id'] = chapter_id
                        if "file" in output_keys:
                            output_schema['file'] = audio_file
                        if "text" in output_keys:
                            output_schema['text'] = transcript
                        transcripts.append(output_schema)
            if audio_data and len(audio_data) == len(transcripts):
                for transcript in transcripts:
                    audio = {"path": transcript["file"], "bytes": audio_data[transcript["id"]]}
                    yield key, {"audio": audio, **transcript}
                    key += 1
                audio_data = {}
                transcripts = []
