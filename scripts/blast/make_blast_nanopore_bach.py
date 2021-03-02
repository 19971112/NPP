import glob
import sys
import os

data_path = sys.argv[1]
work_path = sys.argv[2]
data_dirs = glob.glob(data_path)


original_script1 = """\
#PBS -q small
#PBS -l ncpus=1
#PBS -V
#PBS -l mem=95G

cd ${PBS_O_WORKDIR}

N_THREADS='1'
PATH1='$working_dir'
PATH2='$data_dir'


# pathの設定
echo $(date "+%Y/%m/%d %H:%M:%S") Start program

## 解析ディレクトリのホーム
home_path=$PATH1
echo $home_path

## シークエンスデータのパス
dir_path=$PATH2
echo $dir_path

## fastqファイルの結合
PREFIX=$(basename $dir_path)
mkdir $PREFIX
cd $PREFIX
cat $dir_path/*.fastq > $PREFIX.fastq

# サンプルQC
echo $(date "+%Y/%m/%d %H:%M:%S") Start QC
## アダプターのトリミング
porechop -i $PREFIX.fastq -o $PREFIX.porechop.fastq

## リードのstatisticsの取得
NanoStat --fastq $PREFIX.porechop.fastq

## Nanoplotでクオリティとリード長の分布
NanoPlot --fastq $PREFIX.porechop.fastq --loglength -t $N_THREADS -o qc_result -f pdf

## クオリティフィルタリング
cat $PREFIX.porechop.fastq |NanoFilt -q 10 -l 1200 --maxlength 1800 > $PREFIX.trimmed.porechop.fastq

## Nanoplotでクオリティとリード長の分布
NanoPlot --fastq $PREFIX.trimmed.porechop.fastq --loglength -t $N_THREADS -o qc_result_trimmed -f pdf

## fasta形式に変換
awk '(NR - 1) % 4 < 2' $PREFIX.trimmed.porechop.fastq | sed 's/@/>/' > $PREFIX.trimmed.porechop.fasta


# リード数の調整
echo $(date "+%Y/%m/%d %H:%M:%S") Start QC
# 10万配列以上ある場合にはランダムサンプリングする
L_NUM=$(cat $PREFIX.trimmed.porechop.fasta| awk 'END{print NR}')
if [ $L_NUM -ge 400000 ]; then
  echo $(date "+%Y/%m/%d %H:%M:%S") Start Random sampling
  seqkit sample -n 100000 $PREFIX.trimmed.porechop.fasta > $PREFIX.trimmed.porechop_.fasta
else
  cat $PREFIX.trimmed.porechop.fasta > $PREFIX.trimmed.porechop_.fasta
  echo $(date "+%Y/%m/%d %H:%M:%S") Numbers of reads is under 100000
fi


# blastの一括処理
echo $(date "+%Y/%m/%d %H:%M:%S") Start qblast

## qsubファイルの作成
DB=/home/t16965tw/data/blastDB/SILVA_138_SSURef_NR99_tax_silva/SILVA_138_SSURef_NR99_tax_silva.fasta
QUERY=$home_path/$PREFIX/$PREFIX.trimmed.porechop_.fasta
PROGRAM=blastn
DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM
mkdir $DIR; cd $DIR
perl /home/t16965tw/github/NPP/scripts/q_blast.pl $QUERY $DB -program $PROGRAM -evalue 5 -max_target_seqs 1 -outfmt 6 -num_threads 1 -nseq 5000

## qsubの実行
for i in *.sh; do qsub $i; done

echo $(date "+%Y/%m/%d %H:%M:%S") Done
"""

original_script2 = """\
#PBS -q medium
#PBS -l ncpus=1
#PBS -V

cd ${PBS_O_WORKDIR}

N_THREADS='1'
PATH1='$working_dir'
PATH2='$data_dir'

home_path=$PATH1
dir_path=$PATH2
PREFIX=$(basename $dir_path)

cd $PREFIX

DB=/home/t16965tw/data/blastDB/SILVA_138_SSURef_NR99_tax_silva/SILVA_138_SSURef_NR99_tax_silva.fasta
QUERY=$home_path/$PREFIX/$PREFIX.trimmed.porechop_.fasta
PROGRAM=blastn
DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM

cd $DIR

# blastが終了したら
OUT=$PROGRAM-$(basename $QUERY .fasta)-$(basename $DB .fasta).txt
cat *.bl > $OUT
grep "^>" $QUERY | perl -pe 's/(>(\S+) (.+))/$2\t$1/;' | sort > $QUERY-header
cp $OUT $QUERY-header ..
cd ..

# Extracting data from BLAST databases with _blastdbcmd_
SEQ=$PROGRAM-$(basename $QUERY .fasta)-$(basename $DB .fasta).fasta
grep -v '#' $OUT | awk '{print $2}' | sort -u | blastdbcmd -db $DB -entry_batch - > $SEQ

# Create BLAST output with annotation
echo; echo $OUT; echo $SEQ
sort -k2,2 $OUT > $OUT-sorted
grep "^>" $SEQ | perl -pe 's/(>(\S+) (.+))/$2\t$1/;' > $SEQ-header
join -1 2 -2 1 -t "$(printf '\011')" $OUT-sorted $SEQ-header | sort -k2,2 > file_join_1.txt
grep "^>" $QUERY | perl -pe 's/(>(\S+) (.+))/$2\t$1/;' | sort > $QUERY-header

# ファイル名の変換
python /home/t16965tw/github/NPP/scripts/tools/rename.py /home/t16965tw/github/NPP/data/database/SILVA_138_Taxonomy.txt file_join_1.txt > rename_$PREFIX.txt

python /home/t16965tw/github/NPP/scripts/make_taxbarplot.py $PREFIX
"""

for dir_name in data_dirs:
  file_name = 'nanopore_16S_1_' + os.path.basename(dir_name) + '.job'
  dir_path = data_path + dir_name
  custom_script = original_script1.replace("$working_dir", work_path)
  custom_script = custom_script.replace("$data_dir", dir_path)
  file = open(file_name, 'w')
  file.write(custom_script)
  file.close()

for dir_name in data_dirs:
  file_name = 'nanopore_16S_2_' + os.path.basename(dir_name) + '.job'
  dir_path = data_path + dir_name
  custom_script = original_script2.replace("$working_dir", work_path)
  custom_script = custom_script.replace("$data_dir", dir_path)
  file = open(file_name, 'w')
  file.write(custom_script)
  file.close()
