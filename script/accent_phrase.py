from copy import deepcopy
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

text_list = (
    Path("hiho_output_modified_modified.txt")
    .read_text()
    .replace("\t", " ")
    .splitlines()
)[0::4]


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

mora_end_phoneme_list = vowel_list + other_list + pause_list


def accent_phrase():
    output_text = ""

    for phoneme, accent_start, accent_end, text in zip(
        phoneme_list, accent_start_list, accent_end_list, text_list
    ):
        phoneme = phoneme.split()
        accent_start = [bool(int(a)) for a in accent_start.split()]
        accent_end = [bool(int(a)) for a in accent_end.split()]

        mora_indexs = [i for i, p in enumerate(phoneme) if p in mora_end_phoneme_list]

        accent_phrase_start = [False] * len(mora_indexs)
        accent_phrase_end = [False] * len(mora_indexs)

        # 決定的
        for i_mora, i_phoneme in enumerate(mora_indexs):
            # 無音はアクセント句の境界
            if phoneme[i_phoneme] in pause_list:
                if i_mora < len(mora_indexs) - 1:
                    accent_phrase_start[i_mora + 1] = True
                if i_mora > 0:
                    accent_phrase_end[i_mora - 1] = True

            # startとendが別れている場合は、startの1つ前にアクセント句始まり
            if accent_start[i_phoneme] and not accent_end[i_phoneme]:
                accent_phrase_start[i_mora - 1] = True

        # 条件付き
        base_accent_phrase_start = []
        base_accent_phrase_end = []
        while (
            base_accent_phrase_start != accent_phrase_start
            or base_accent_phrase_end != accent_phrase_end
        ):
            base_accent_phrase_start = deepcopy(accent_phrase_start)
            base_accent_phrase_end = deepcopy(accent_phrase_end)

            # start/end箇所
            # そこがアクセント句終わりの場合、前がアクセント句始まり
            # 前がアクセント句終わりの場合、そこはアクセント句始まり
            for i_mora, i_phoneme in enumerate(mora_indexs):
                if accent_start[i_phoneme] and accent_end[i_phoneme]:
                    if accent_phrase_end[i_mora]:
                        accent_phrase_start[i_mora - 1] = True
                    if accent_phrase_end[i_mora - 1]:
                        accent_phrase_start[i_mora] = True

            # アクセント始まりの前はアクセント終わり
            for i_mora, start in enumerate(accent_phrase_start):
                if start:
                    i_candidate = i_mora - 1
                    if phoneme[mora_indexs[i_candidate]] in pause_list:
                        i_candidate = i_candidate - 1
                    if i_candidate >= 0:
                        accent_phrase_end[i_candidate] = True

        # start/end箇所で、そこか前がアクセント句始まりでない場所は、アクセント句始まりが不明
        for i_mora, i_phoneme in enumerate(mora_indexs):
            if accent_start[i_phoneme] and accent_end[i_phoneme]:
                if (
                    not accent_phrase_start[i_mora]
                    and not accent_phrase_start[i_mora - 1]
                ):
                    accent_phrase_start[i_mora] = accent_phrase_start[i_mora - 1] = None

        # output
        new_accent_phrase_start = ["-" for _ in range(len(phoneme))]
        new_accent_phrase_end = ["-" for _ in range(len(phoneme))]

        for i_mora, (start, end) in enumerate(
            zip(accent_phrase_start, accent_phrase_end)
        ):
            new_accent_phrase_start[mora_indexs[i_mora]] = (
                str(int(start)) if start is not None else "?"
            )
            new_accent_phrase_end[mora_indexs[i_mora]] = str(int(end))

        output_text += text + "\n"
        output_text += "\t".join(phoneme) + "\n"
        output_text += "\t".join([str(int(f)) for f in accent_start]) + "\n"
        output_text += "\t".join([str(int(f)) for f in accent_end]) + "\n"
        output_text += "\t".join(new_accent_phrase_start) + "\n"
        output_text += "\t".join(new_accent_phrase_end) + "\n"

    Path("hiho_output_modified_modified_modified.txt").write_text(output_text)


accent_phrase()
