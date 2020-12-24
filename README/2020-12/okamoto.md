# 岡本さんの解析

last-update 2020-12-21
wt

## fastaの整形

形式を統一するため、一度biopythonで読み込んで、書き出す。

```
cd '/Volumes/GoogleDrive/マイドライブ/projectF/analysis/20201205_鉄腐食の解析'

from Bio import SeqIO
box  = []
for record in SeqIO.parse("q.fasta.txt" , "fasta"):
    box.append(record)
SeqIO.write(box, "query.fasta", "fasta")
```

## blast用のDBの作成

```
cd /home/t16965tw/github/NPP/analysis/2020-12-21
qsub ~/github/NPP/scripts/blast/mkblastDB.sh

mkdir db
mv *fasta.* db/
```


## tblastnの実行

```
DB=/home/t16965tw/github/NPP/analysis/2020-12-21/db/contigs.fasta
QUERY=/home/t16965tw/github/NPP/analysis/2020-12-24/query.fasta
DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM
PROGRAM=tblastx
mkdir $DIR; cd $DIR

perl /home/t16965tw/scripts/tom/q_blast_2020-10-11.pl $QUERY $DB -program $PROGRAM -evalue 1e-05 -max_target_seqs 1 -outfmt 6 -num_threads 1 -nseq 1
for i in *.sh; do qsub $i; done
```
