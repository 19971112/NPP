# メタゲノムのアセンブルを行う．

## 生データ
```
# NW
/home/t16965tw/data/metagenome/illumina_whole/202005-08-01-1/Sequence/NW2

# Wagu
/home/t16965tw/data/metagenome/illumina_whole/202005-08-01-1/Sequence/Wagu2
```


## ペアエンド リードを同期する

Fastq-pair  
http://kazumaxneo.hatenablog.com/entry/2019/02/26/073000

https://github.com/linsalrob/fastq-pair  

リード数の4分の1を `-t` の値として設定する
```
fastq_pair -t 50021 file1.fastq file2.fastq
```
