from pathlib import Path

phoneme_list = (
    Path("voiceactoress100_phoneme_openjtalk.txt")
    .read_text()
    .replace("\t", " ")
    .splitlines()
)

accent_start_list = (
    Path("voiceactoress100_accent_start.txt")
    .read_text()
    .replace("\t", " ")
    .splitlines()
)

accent_end_list = (
    Path("voiceactoress100_accent_end.txt").read_text().replace("\t", " ").splitlines()
)

accent_phrase_start_list = (
    Path("voiceactoress100_accent_phrase_start.txt")
    .read_text()
    .replace("\t", " ")
    .splitlines()
)

accent_phrase_end_list = (
    Path("voiceactoress100_accent_phrase_end.txt")
    .read_text()
    .replace("\t", " ")
    .splitlines()
)


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


def hiho_accent_phrase_checker():
    for (
        phoneme,
        accent_start,
        accent_end,
        accent_phrase_start,
        accent_phrase_end,
    ) in zip(
        phoneme_list,
        accent_start_list,
        accent_end_list,
        accent_phrase_start_list,
        accent_phrase_end_list,
    ):
        phoneme = phoneme.split()
        accent_start = [bool(int(a)) for a in accent_start.split()]
        accent_end = [bool(int(a)) for a in accent_end.split()]
        accent_phrase_start = [bool(int(a)) for a in accent_phrase_start.split()]
        accent_phrase_end = [bool(int(a)) for a in accent_phrase_end.split()]

        # 最初はアクセント句開始
        expected_is_start = True

        for i in range(len(phoneme)):
            # 無音にアクセント句区切りは来ない
            if phoneme[i] in pause_list:
                assert not accent_phrase_start[i]
                assert not accent_phrase_end[i]

            # アクセント句開始と終了は同時に来ない
            assert not accent_phrase_start[i] or not accent_phrase_end[i]

            # 母音でかつ手前が子音のとき、アクセント句区切りラベルは一致する
            if phoneme[i] in vowel_list:
                if phoneme[i - 1] in conso_list:
                    assert accent_phrase_start[i] == accent_phrase_start[i - 1]
                    assert accent_phrase_end[i] == accent_phrase_end[i - 1]

            # 子音のとき、後ろとアクセント句区切りラベルが一致する
            if phoneme[i] in conso_list:
                assert accent_phrase_start[i] == accent_phrase_start[i + 1]
                assert accent_phrase_end[i] == accent_phrase_end[i + 1]

            if phoneme[i] in (vowel_list + other_list):
                # アクセント句開始後に開始は来ない
                if accent_phrase_start[i]:
                    assert expected_is_start
                    expected_is_start = False

                # アクセント句終了後に終了は来ない
                if accent_phrase_end[i]:
                    assert not expected_is_start
                    expected_is_start = True

                # アクセント句終了は連続しない
                if accent_phrase_end[i]:
                    assert not accent_phrase_end[i + 1]

        # アクセントはアクセント句外で来ない
        in_accent_phrase = False
        for i in range(len(phoneme)):
            if phoneme[i] not in (vowel_list + other_list):
                continue

            if accent_phrase_start[i]:
                in_accent_phrase = True

            if accent_start[i] or accent_end[i]:
                assert in_accent_phrase

            if accent_phrase_end[i]:
                in_accent_phrase = False

        # 最後はアクセント句終了
        assert expected_is_start

        # アクセント句開始と終了の数は一緒
        a = sum(
            accent_phrase_start[i]
            for i in range(len(phoneme))
            if phoneme[i] in (vowel_list + other_list)
        )
        b = sum(
            accent_phrase_end[i]
            for i in range(len(phoneme))
            if phoneme[i] in (vowel_list + other_list)
        )
        assert a == b


hiho_accent_phrase_checker()
