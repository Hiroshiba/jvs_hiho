from copy import deepcopy
from pathlib import Path
from typing import List

pause_list = ("pau", "sil")
mora_end_phoneme_list = (
    ("a", "i", "u", "e", "o", "A", "I", "U", "E", "O") + ("cl", "N") + pause_list
)

text_list = (
    Path("hiho_output_modified_modified_modified.txt")
    .read_text()
    .replace("\t", " ")
    .splitlines()
)

phoneme_list = [s.split() for s in text_list[1::6]]
accent_start_list = [s.split() for s in text_list[2::6]]
accent_end_list = [s.split() for s in text_list[3::6]]
accent_phrase_start_list = [s.split() for s in text_list[4::6]]
accent_phrase_end_list = [s.split() for s in text_list[5::6]]

# 修正
for phoneme, accent_start, accent_end, accent_phrase_start, accent_phrase_end in zip(
    phoneme_list,
    accent_start_list,
    accent_end_list,
    accent_phrase_start_list,
    accent_phrase_end_list,
):
    mora_indexs = [i for i, p in enumerate(phoneme) if p in mora_end_phoneme_list]

    # アクセント始まりの前はアクセント終わり
    for i_mora, i_phoneme in enumerate(mora_indexs):
        if accent_phrase_start[i_phoneme] == "1":
            i_candidate = i_mora - 1
            if phoneme[mora_indexs[i_candidate]] in pause_list:
                i_candidate = i_candidate - 1
            if i_candidate >= 0:
                accent_phrase_end[mora_indexs[i_candidate]] = "1"

    # 未定のところは子音で、母音の値をコピー
    for i_phoneme, p in enumerate(phoneme):
        if accent_phrase_start[i_phoneme] == "-":
            assert p not in mora_end_phoneme_list
            accent_phrase_start[i_phoneme] = accent_phrase_start[i_phoneme + 1]
        if accent_phrase_end[i_phoneme] == "-":
            assert p not in mora_end_phoneme_list
            accent_phrase_end[i_phoneme] = accent_phrase_end[i_phoneme + 1]


text = "\n".join([" ".join(s) for s in accent_phrase_start_list])
Path("voiceactoress100_accent_phrase_start.txt").write_text(text)

text = "\n".join([" ".join(s) for s in accent_phrase_end_list])
Path("voiceactoress100_accent_phrase_end.txt").write_text(text)
