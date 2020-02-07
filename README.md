[JVS (Japanese versatile speech) ](https://sites.google.com/site/shinnosuketakamichi/research-topics/jvs_corpus)コーパスの、自作のラベルです。

# aligned_labels
JVSコーパスのpalallel100（話者間で共通する読み上げ音声100発話）を、読み仮名を音声に合うように修正した上で、[Julius](https://julius.osdn.jp/)による自動アライメントを行った音素系列ラベルです。

## 詳細
JVSコーパス内にある日本語テキストを元に、以下の修正を加えました。

* 読み仮名を音声に合わせる
* 句読点の位置を音声に合わせる

修正を加えた読み仮名テキストは[voiceactoress100_spaced_julius.txt](voiceactoress100_spaced_julius.txt)です。

その後、読み仮名を音素系列にし、Juliusのmonophone音素モデルを用いて音素をアライメントしました。
この際、ショートポーズ`sp`の有無もJuliusで推定しました。

実行コードは[run.bash](./run.bash)です。

## ライセンス
CC BY-SA 4.0（[声優統計コーパス](https://voice-statistics.github.io/)の音素バランス文のライセンスを継承しています）
