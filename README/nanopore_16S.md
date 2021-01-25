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
# cat *.fastq > all.fastq


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

#### QC済の配列をblastする

```
DB=/home/t16965tw/data/blastDB/SILVA_138_SSURef_NR99_tax_silva/SILVA_138_SSURef_NR99_tax_silva.fasta
QUERY=/home/t16965tw/github/NPP/analysis/2021-01-25/all.trimmed.porechop.fastq
PROGRAM=blastn

DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM

mkdir $DIR; cd $DIR
perl /home/t16965tw/scripts/tom/q_blast_2020-10-11.pl $QUERY $DB -program $PROGRAM -evalue 5 -max_target_seqs 1 -outfmt 6 -num_threads 1 -nseq 2000

# jobの実行
for i in *.sh; do qsub $i; done
```

結果の集計

```
DB=/home/t16965tw/data/blastDB/SILVA_138_SSURef_NR99_tax_silva/SILVA_138_SSURef_NR99_tax_silva.fasta
QUERY=/home/t16965tw/github/NPP/analysis/2021-01-25/all.trimmed.porechop.fastq
PROGRAM=blastn

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
join -1 2 -2 1 -t "$(printf '\011')" file_join_1.txt $QUERY-header > file_join_2.txt

echo -e "query id\tsubject id\t% identity\talignment length\tmismatches\tgap opens\tq. start\tq. end\ts. start\ts. end\tevalue\tbit score\tsubject\tquery" > $PROGRAM-$(basename $QUERY .fasta)-$(basename $DB .fasta)-annotation.txt
cat file_join_1.txt | perl -pe 's/(UniRef50|UniRef90|UniRef100)_//g;' >> $PROGRAM-$(basename $QUERY .fasta)-$(basename $DB .fasta)-annotation.txt
```


#### blastの集計結果の形式

何行目にどの情報が書いてあるのかを表示する．

`head -n1 blastn-all-SILVA_138_SSURef_NR99_tax_silva-annotation.txt  | tr "\t" "\n" | n`

```
     1	query id
     2	subject id
     3	% identity
     4	alignment length
     5	mismatches
     6	gap opens
     7	q. start
     8	q. end
     9	s. start
    10	s. end
    11	evalue
    12	bit score
    13	subject
    14	query
```

