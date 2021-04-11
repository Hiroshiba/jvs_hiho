from difflib import SequenceMatcher
from pathlib import Path
from typing import List

from acoustic_feature_extractor.data.phoneme import JvsPhoneme
from tqdm import tqdm

mora_end_phoneme_list = (
    ("a", "i", "u", "e", "o", "A", "I", "U", "E", "O") + ("cl", "N") + ("pau", "sil")
)


def main():
    output_start_base_dir = Path("accent_phrase_starts")
    output_end_base_dir = Path("accent_phrase_ends")

    output_start_base_dir.mkdir(exist_ok=True)
    output_end_base_dir.mkdir(exist_ok=True)

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
    accent_phrase_starts = [
        s.split()
        for s in (
            Path("voiceactoress100_accent_phrase_start.txt")
            .read_text()
            .replace("\t", " ")
            .splitlines()
        )
    ]
    accent_phrase_ends = [
        s.split()
        for s in (
            Path("voiceactoress100_accent_phrase_end.txt")
            .read_text()
            .replace("\t", " ")
            .splitlines()
        )
    ]

    for person_dir, person in tqdm(zip(person_dirs, persons)):
        label_paths = sorted(person_dir.glob("*.lab"))

        output_start_dir = output_start_base_dir.joinpath(person)
        output_end_dir = output_end_base_dir.joinpath(person)
        output_start_dir.mkdir(exist_ok=True)
        output_end_dir.mkdir(exist_ok=True)
        for label_path in label_paths:
            i_label = int(label_path.stem[-3:]) - 1
            phoneme = phonemes[i_label]
            accent_phrase_start = accent_phrase_starts[i_label]
            accent_phrase_end = accent_phrase_ends[i_label]

            label = JvsPhoneme.load_julius_list(label_path)
            label_phoneme = [l.phoneme for l in label]

            new_accent_phrase_start: List[str] = []
            new_accent_phrase_end: List[str] = []
            for tag, i1, i2, j1, j2 in SequenceMatcher(
                None, phoneme, label_phoneme
            ).get_opcodes():
                if tag == "equal":
                    new_accent_phrase_start += accent_phrase_start[i1:i2]
                    new_accent_phrase_end += accent_phrase_end[i1:i2]
                elif tag == "replace":
                    # 最初と最後だけ
                    assert i2 - i1 == 1
                    assert phoneme[i1] == "sil" and label_phoneme[j1] == "pau"
                    new_accent_phrase_start += accent_phrase_start[i1:i2]
                    new_accent_phrase_end += accent_phrase_end[i1:i2]
                elif tag == "delete":
                    assert i2 - i1 == 1
                    assert phoneme[i1] == "pau"
                else:
                    raise ValueError(tag)

            # 保存
            output_start_path = output_start_dir.joinpath(f"{label_path.stem}.txt")
            output_end_path = output_end_dir.joinpath(f"{label_path.stem}.txt")
            output_start_path.write_text(" ".join(new_accent_phrase_start))
            output_end_path.write_text(" ".join(new_accent_phrase_end))


if __name__ == "__main__":
    main()
