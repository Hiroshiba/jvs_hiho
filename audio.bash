#!/usr/bin/env bash

JVSDIR=/path/to/jvs_ver1/
OUTDIR=/path/to/jvs_hiho_ver1/

mkdir $OUTDIR

# link all wave file
for speaker in jvs{001..100}; do
    echo $speaker
    for corpus in falset10 nonpara30 parallel100 whisper10; do
        mkdir -p $OUTDIR/$speaker/$corpus/wav24kHz16bit
        find $JVSDIR/$speaker/$corpus/wav24kHz16bit -name '*.wav' | parallel ln {} $OUTDIR/$speaker/$corpus/wav24kHz16bit/{/}
    done
done

# move known mistake
mv $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_021.wav $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_022.wav
mv $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_020.wav $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_021.wav
mv $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_019.wav $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_020.wav
mv $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_018.wav $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_019.wav
mv $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_017.wav $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_018.wav
mv $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_016.wav $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_017.wav
mv $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_015.wav $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_016.wav

# remove known mistake
rm $OUTDIR/jvs009/parallel100/wav24kHz16bit/VOICEACTRESS100_086.wav
rm $OUTDIR/jvs009/parallel100/wav24kHz16bit/VOICEACTRESS100_095.wav
rm $OUTDIR/jvs017/parallel100/wav24kHz16bit/VOICEACTRESS100_082.wav
rm $OUTDIR/jvs018/parallel100/wav24kHz16bit/VOICEACTRESS100_072.wav
rm $OUTDIR/jvs022/parallel100/wav24kHz16bit/VOICEACTRESS100_047.wav
rm $OUTDIR/jvs024/parallel100/wav24kHz16bit/VOICEACTRESS100_088.wav
rm $OUTDIR/jvs036/parallel100/wav24kHz16bit/VOICEACTRESS100_057.wav
rm $OUTDIR/jvs038/parallel100/wav24kHz16bit/VOICEACTRESS100_006.wav
rm $OUTDIR/jvs038/parallel100/wav24kHz16bit/VOICEACTRESS100_041.wav
rm $OUTDIR/jvs043/parallel100/wav24kHz16bit/VOICEACTRESS100_085.wav
rm $OUTDIR/jvs047/parallel100/wav24kHz16bit/VOICEACTRESS100_085.wav
rm $OUTDIR/jvs048/parallel100/wav24kHz16bit/VOICEACTRESS100_043.wav
rm $OUTDIR/jvs048/parallel100/wav24kHz16bit/VOICEACTRESS100_076.wav
rm $OUTDIR/jvs051/parallel100/wav24kHz16bit/VOICEACTRESS100_025.wav
rm $OUTDIR/jvs055/parallel100/wav24kHz16bit/VOICEACTRESS100_056.wav
rm $OUTDIR/jvs055/parallel100/wav24kHz16bit/VOICEACTRESS100_076.wav
rm $OUTDIR/jvs055/parallel100/wav24kHz16bit/VOICEACTRESS100_099.wav
rm $OUTDIR/jvs058/parallel100/wav24kHz16bit/VOICEACTRESS100_014.wav
rm $OUTDIR/jvs059/parallel100/wav24kHz16bit/VOICEACTRESS100_061.wav
rm $OUTDIR/jvs059/parallel100/wav24kHz16bit/VOICEACTRESS100_064.wav
rm $OUTDIR/jvs059/parallel100/wav24kHz16bit/VOICEACTRESS100_066.wav
rm $OUTDIR/jvs059/parallel100/wav24kHz16bit/VOICEACTRESS100_074.wav
rm $OUTDIR/jvs060/parallel100/wav24kHz16bit/VOICEACTRESS100_082.wav
rm $OUTDIR/jvs074/parallel100/wav24kHz16bit/VOICEACTRESS100_062.wav
rm $OUTDIR/jvs098/parallel100/wav24kHz16bit/VOICEACTRESS100_060.wav
rm $OUTDIR/jvs098/parallel100/wav24kHz16bit/VOICEACTRESS100_099.wav
