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

