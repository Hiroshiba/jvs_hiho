from difflib import SequenceMatcher
from pathlib import Path
from typing import List

from acoustic_feature_extractor.data.phoneme import JvsPhoneme
from tqdm import tqdm

mora_end_phoneme_list = (
    ("a", "i", "u", "e", "o", "A", "I", "U", "E", "O") + ("cl", "N") + ("pau", "sil")
)


def main():
    output_accent_start_base_dir = Path("accent_starts")
    output_accent_end_base_dir = Path("accent_ends")

    output_accent_start_base_dir.mkdir(exist_ok=True)
    output_accent_end_base_dir.mkdir(exist_ok=True)

    person_dirs = sorted(Path("aligned_labels_openjtalk").glob("jvs*"))
    persons = [p.stem for p in person_dirs]

    phonemes = [
        s.split()
        for s in (
            Path("voiceactoress100_phoneme_openjtalk.txt")
            .read_text()
            .strip()
            .splitlines()
        )
    ]
    accent_starts = [
        s.split()
        for s in Path("voiceactoress100_accent_start.txt")
        .read_text()
        .strip()
        .splitlines()
    ]
    accent_ends = [
        s.split()
        for s in Path("voiceactoress100_accent_end.txt")
        .read_text()
        .strip()
        .splitlines()
    ]

    for person_dir, person in tqdm(zip(person_dirs, persons)):
        label_paths = sorted(person_dir.glob("*.lab"))

        output_accent_start_dir = output_accent_start_base_dir.joinpath(person)
        output_accent_end_dir = output_accent_end_base_dir.joinpath(person)
        output_accent_start_dir.mkdir(exist_ok=True)
        output_accent_end_dir.mkdir(exist_ok=True)
        for label_path in label_paths:
            i_label = int(label_path.stem[-3:]) - 1
            phoneme = phonemes[i_label]
            accent_start = accent_starts[i_label]
            accent_end = accent_ends[i_label]

            label = JvsPhoneme.load_julius_list(label_path)
            label_phoneme = [l.phoneme for l in label]

            new_accent_start: List[str] = []
            new_accent_end: List[str] = []
            for tag, i1, i2, j1, j2 in SequenceMatcher(
                None, phoneme, label_phoneme
            ).get_opcodes():
                if tag == "equal":
                    new_accent_start += accent_start[i1:i2]
                    new_accent_end += accent_end[i1:i2]
                elif tag == "replace":
                    # 最初と最後だけ
                    assert i2 - i1 == 1
                    assert phoneme[i1] == "sil" and label_phoneme[j1] == "pau"
                    new_accent_start += accent_start[i1:i2]
                    new_accent_end += accent_end[i1:i2]
                elif tag == "delete":
                    assert i2 - i1 == 1
                    assert phoneme[i1] == "pau"
                else:
                    raise ValueError(tag)

            # endが2モーラ連続する場合はアクセント核を連結する
            mora_index_list = [0] + [
                i + 1 for i, p in enumerate(label_phoneme) if p in mora_end_phoneme_list
            ]
            for i in range(len(mora_index_list) - 2):
                prev_index = mora_index_list[i]
                cent_index = mora_index_list[i + 1]
                post_index = mora_index_list[i + 2]
                if (
                    new_accent_end[prev_index] == "1"
                    and new_accent_end[cent_index] == "1"
                ):
                    assert new_accent_start[cent_index] == "1"
                    for j in range(prev_index, cent_index):
                        new_accent_end[j] = "0"
                    for j in range(cent_index, post_index):
                        new_accent_start[j] = "0"

            # 保存
            output_accent_start_path = output_accent_start_dir.joinpath(
                f"{label_path.stem}.txt"
            )
            output_accent_end_path = output_accent_end_dir.joinpath(
                f"{label_path.stem}.txt"
            )
            output_accent_start_path.write_text(" ".join(new_accent_start))
            output_accent_end_path.write_text(" ".join(new_accent_end))


if __name__ == "__main__":
    main()
