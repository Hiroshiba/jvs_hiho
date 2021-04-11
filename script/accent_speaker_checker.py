from glob import glob
from pathlib import Path

from acoustic_feature_extractor.data.phoneme import JvsPhoneme
from tqdm import tqdm

label_paths = sorted(map(Path, glob("./aligned_labels_openjtalk/*/*.lab")))
accent_start_paths = sorted(map(Path, glob("./accent_starts/*/*.txt")))
accent_end_paths = sorted(map(Path, glob("./accent_ends/*/*.txt")))

vowel_list = ("a", "i", "u", "e", "o", "A", "I", "U", "E", "O")
pause_list = ("pau", "sil")
conso_list = (
    "b",
    "by",
    "ch",
    "d",
    "dy",
    "f",
    "g",
    "gy",
    "h",
    "hy",
    "j",
    "k",
    "ky",
    "m",
    "my",
    "n",
    "ny",
    "p",
    "py",
    "r",
    "ry",
    "s",
    "sh",
    "t",
    "ts",
    "v",
    "w",
    "y",
    "z",
)
other_list = ("cl", "N")


def accent_speaker_checker():
    for label_path, accent_start_path, accent_end_path in tqdm(
        zip(label_paths, accent_start_paths, accent_end_paths)
    ):
        label = JvsPhoneme.load_julius_list(label_path)
        phoneme = [l.phoneme for l in label]

        accent_start = [bool(int(a)) for a in accent_start_path.read_text().split()]
        accent_end = [bool(int(a)) for a in accent_end_path.read_text().split()]

        # アクセントの数は音素数に一致
        assert len(accent_start) == len(phoneme)
        assert len(accent_end) == len(phoneme)

        # 最初はアクセント開始
        expected_accent_is_start = True

        for i in range(len(phoneme)):
            # 無音にアクセントは来ない
            if phoneme[i] in pause_list:
                assert not accent_start[i]
                assert not accent_end[i]

            # 母音でかつ手前が子音のとき、アクセントラベルは一致する
            if phoneme[i] in vowel_list:
                if phoneme[i - 1] in conso_list:
                    assert accent_start[i] == accent_start[i - 1]
                    assert accent_end[i] == accent_end[i - 1]

            # 子音のとき、後ろとアクセントラベルが一致する
            if phoneme[i] in conso_list:
                assert accent_start[i] == accent_start[i + 1]
                assert accent_end[i] == accent_end[i + 1]

            if phoneme[i] in (vowel_list + other_list):
                # アクセント開始後に開始は来ない
                if accent_start[i]:
                    assert expected_accent_is_start
                    expected_accent_is_start = False

                # アクセント終了後に終了は来ない
                if accent_end[i]:
                    assert not expected_accent_is_start
                    expected_accent_is_start = True

                # アクセント終了は連続しない
                if accent_end[i]:
                    assert not accent_end[i + 1]

        # 最後はアクセント終了
        assert expected_accent_is_start

        # アクセント開始と終了の数は一緒
        a = sum(
            accent_start[i]
            for i in range(len(phoneme))
            if phoneme[i] in (vowel_list + other_list)
        )
        b = sum(
            accent_end[i]
            for i in range(len(phoneme))
            if phoneme[i] in (vowel_list + other_list)
        )
        assert a == b


accent_speaker_checker()
