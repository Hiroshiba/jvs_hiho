# jvs_hiho
[JVS (Japanese versatile speech) ](https://sites.google.com/site/shinnosuketakamichi/research-topics/jvs_corpus)コーパスの、[@Hiroshiba](http://github.com/Hiroshiba)作のラベルです。

## aligned_labels_openjtalk
JVSコーパスのpalallel100（話者間で共通する読み上げ音声100発話）を、読み仮名を音声に合うように修正した上で、Juliusによる自動アライメントを行った音素系列ラベルです。

## 詳細
### 音声に関して
@Hiroshibaが見つけた音声の間違いをもとに、一部の音声ファイルを修正・削除しています。
実行コードは[audio.bash](./audio.bash)です。

### テキストに関して
[voiceactoress100_spaced_julius.txt](./voiceactoress100_spaced_julius.txt)がテキストです。

JVSコーパス内にある日本語テキストを元に、以下の修正を加えました。

* カタカナ表記にする
* 読み仮名を音声に合わせる
* 句読点の位置を音声に合わせ、スペースにする

これらの修正を加えたテキストが[voiceactoress100_spaced.txt](voiceactoress100_spaced.txt)です。

この修正に加えて、更に以下の修正を加えました。

* 珍しい読みの`ツュ`と`ヴュ`を、`チュ`と`ビュ`に変える

この修正を加えたテキストが[voiceactoress100_spaced_julius.txt](voiceactoress100_spaced_julius.txt)です。

### Julius音素系列ラベルに関して
[aligned_labels_julius](./aligned_labels_julius/)がJulius音素系列ラベルです。

テキスト[voiceactoress100_spaced_julius.txt](voiceactoress100_spaced_julius.txt)を音素系列にし、Juliusのmonophone音素モデルを用いて音素をアライメントしました。
この際、ショートポーズ`sp`の有無もJuliusで推定しました。

実行コードは[phoneme.bash](./phoneme.bash)です。

### OpenJTalk音素系列ラベルに関して
[aligned_labels_openjtalk](./aligned_labels_openjtalk/)がOpenJTalk音素系列ラベルです。

Julius音素系列をOpenJTalk用に変更しました。
[OpenJTalk label getter](https://github.com/Hiroshiba/openjtalk-label-getter/tree/6435aa49dcfc9b06160f61552043a9a01ab9f359)を用いてOpenJTalk用の音素を取得し、一部を修正しました。
変更後の音素が[voiceactoress100_phoneme_openjtalk](voiceactoress100_phoneme_openjtalk.txt)です。

その後、音素をJulius用のものに変換し、Juliusのmonophone音素モデルを用いて音素をアライメントしました。

実行コードは[phoneme.bash](./phoneme.bash)です。

## ライセンス
### 使用ライブラリに関して
[Julius](https://github.com/julius-speech/julius)
[Open JTalk](http://open-jtalk.sourceforge.net/)

### テキスト・音素系列ラベルに関して
CC BY-SA 4.0（[声優統計コーパス](https://voice-statistics.github.io/)の音素バランス文のライセンスを継承しています）

### 実行コード（Bashスクリプト）に関して
MIT LICENSE
