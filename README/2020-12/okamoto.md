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

```
