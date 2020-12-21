# 岡本さんの解析

last-update 2020-12-21
wt

## fastaの整形

あまりにも汚い形式なので、一度biopythonで読み込んで、書き出す。

```
cd '/Volumes/GoogleDrive/マイドライブ/projectF/analysis/20201205_鉄腐食の解析'

from Bio import SeqIO
box  = []
for record in SeqIO.parse("q.fasta.txt" , "fasta"):
    box.append(record)
SeqIO.write(box, "query.fasta", "fasta")
```
