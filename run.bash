JVSDIR=/path/to/jvs_ver1/
OUTDIR=./aligned_labels/
JULIUS_HMM_PATH=/path/to/jnas-mono-16mix-gid.binhmm

TMPDIR=/tmp/jvs_alignment

mkdir -p $OUTDIR
mkdir -p $TMPDIR

# download segmentation code
git clone https://github.com/Hiroshiba/julius4seg

# get file names
names=$(ls $JVSDIR/jvs001/parallel100/wav24kHz16bit | sed -E 's/.wav//g')
paste <(echo "$names") <(cat ./voiceactoress100_spaced_julius.txt) |\
    while read name text; do
        echo $text > $TMPDIR/$name.txt
    done

# align phonemes each person
for person in $(ls -d $JVSDIR/jvs*/ | grep -o 'jvs[0-9][0-9][0-9]'); do
    find $JVSDIR/$person/parallel100/wav24kHz16bit -name '*.wav' |\
        parallel sox {} $TMPDIR/{/} channels 1 rate 16k

    echo "$names" |\
    parallel --progress \
        PYTHONPATH=./julius4seg/ python ./julius4seg/sample/run_segment.py \
            $TMPDIR/{}.wav \
            $TMPDIR/{}.txt \
            $TMPDIR/{}.lab \
            --hmm_model $JULIUS_HMM_PATH \

    mkdir $OUTDIR/$person
    mv $TMPDIR/*.lab $OUTDIR/$person/
done
