# Nanopore 16S データの処理



## nanoporeデータのQC


以下のスクリプトにて実行

```
#PBS -q small
#PBS -l ncpus=10
#PBS -l mem=95G
#PBS -V

cd ${PBS_O_WORKDIR}

N_THREADS='10'

# fastqファイルの結合

cat *.fastq > all.fastq


# アダプターのトリミング
porechop -i all.fastq -o all.porechop.fastq

# リードのstatisticsの取得
NanoStat --fastq all.porechop.fastq -t $N_THREADS

# Nanoplotでクオリティとリード長の分布
NanoPlot --fastq all.porechop.fastq --loglength -t $N_THREADS -o qc_result -f pdf

# クオリティフィルタリング
# 5'末端50-bpのトリミング、平均クオリティ10以下のリードを捨てるクオリティフィルタリング、500bp以下のリードを捨てる
cat all.porechop.fastq |NanoFilt -q 10 -l 1200 --maxlength 1800 > all.trimmed.porechop.fastq

# Nanoplotでクオリティとリード長の分布
NanoPlot --fastq all.trimmed.porechop.fastq --loglength -t $N_THREADS -o qc_result_trimmed -f pdf

```
