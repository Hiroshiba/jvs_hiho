#!/usr/bin/env bash

JVSDIR=/path/to/jvs_hiho_ver1/
OUTDIR_JULIUS=./aligned_labels_julius/
OUTDIR_OPENJTALK=./aligned_labels_openjtalk/
JULIUS_HMM_PATH=/path/to/jnas-mono-16mix-gid.binhmm

TMPDIR=/tmp/jvs_alignment

mkdir -p $OUTDIR_JULIUS
mkdir -p $OUTDIR_OPENJTALK
mkdir -p $TMPDIR

# install libraries
pip install git+https://github.com/Hiroshiba/julius4seg@0e01f546bf4aa1329c9ee7a39df8630c066e63e3

# get file names
names=$(ls $JVSDIR/jvs001/parallel100/wav24kHz16bit | sed -E 's/.wav//g')

mkdir $TMPDIR/text
paste <(echo "$names") <(cat ./voiceactoress100_spaced_julius.txt) |\
    while read name text; do
        echo $text > $TMPDIR/text/$name.txt
    done

# for julius label
for person in $(ls -d $JVSDIR/jvs*/ | grep -o 'jvs[0-9][0-9][0-9]'); do
    echo $person

    mkdir $TMPDIR/audio
    find $JVSDIR/$person/parallel100/wav24kHz16bit -name '*.wav' |\
        parallel sox {} $TMPDIR/audio/{/} channels 1 rate 16k

    mkdir $OUTDIR_JULIUS/$person
    echo "$names" |\
    parallel julius4seg_segment \
        $TMPDIR/audio/{}.wav \
        $TMPDIR/text/{}.txt \
        $OUTDIR_JULIUS/$person/{}.lab \
        --hmm_model $JULIUS_HMM_PATH \

    # for failed files
    join -v 1 <(echo "$names") <(ls $OUTDIR_JULIUS/$person | xargs basename -s .lab) |\
    parallel julius4seg_segment \
        $TMPDIR/audio/{}.wav \
        $TMPDIR/text/{}.txt \
        $OUTDIR_JULIUS/$person/{}.lab \
        --hmm_model $JULIUS_HMM_PATH \
        --only_2nd_path \

    rm -r $TMPDIR/audio
done

# for OpenJTalk label
mkdir $TMPDIR/openjtalk_phoneme

echo "$names" |\
while read name; do
    echo "
        openjtalk_label_getter \
            '$(cat $TMPDIR/text/$name.txt | nkf --hiragana)' \
            --output_wave_path /tmp/openjtalk_label_getter_$name.wav \
            --output_log_path /tmp/openjtalk_label_getter_$name.txt |\
        awk '{print \$3}' \
        > $TMPDIR/openjtalk_phoneme/$name.lab
    "
done |\
parallel --progress {}

for person in $(ls -d $JVSDIR/jvs*/ | grep -o 'jvs[0-9][0-9][0-9]'); do
    echo $person
    mkdir $OUTDIR_OPENJTALK/$person

    mkdir $TMPDIR/audio
    find $JVSDIR/$person/parallel100/wav24kHz16bit -name '*.wav' |\
        parallel sox {} $TMPDIR/audio/{/} channels 1 rate 16k

    mkdir $TMPDIR/julius_phoneme
    echo "$names" |\
    parallel julius4seg_segment \
        $TMPDIR/audio/{}.wav \
        $TMPDIR/text/{}.txt \
        $TMPDIR/julius_phoneme/{}.lab \
        --hmm_model $JULIUS_HMM_PATH \
        --like_openjtalk \

    # for failed files
    join -v 1 <(echo "$names") <(ls $TMPDIR/julius_phoneme | xargs basename -s .lab) |\
    parallel julius4seg_segment \
        $TMPDIR/audio/{}.wav \
        $TMPDIR/text/{}.txt \
        $TMPDIR/julius_phoneme/{}.lab \
        --hmm_model $JULIUS_HMM_PATH \
        --like_openjtalk \
        --only_2nd_path \

    echo "$names" |\
    while read name; do
        lab_julius=$TMPDIR/julius_phoneme/$name.lab
        lab_openjtalk=$TMPDIR/openjtalk_phoneme/$name.lab
        if [ ! -e "$lab_julius" ]; then continue; fi

        diff -y \
            <(cat $lab_julius | awk '{print $3}') \
            $lab_openjtalk |\
        grep -v '>' | awk '{print $NF}' > /tmp/openjtalk_label.txt

        paste $lab_julius /tmp/openjtalk_label.txt | awk '{print $1, $2, $4}' \
        > $OUTDIR_OPENJTALK/$person/$name.lab
    done

    rm -r $TMPDIR/audio
    rm -r $TMPDIR/julius_phoneme
done
