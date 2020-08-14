# メタゲノムのアセンブルを行う．

## table of contents



---

## まずはショートリードの

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

解凍してリードを同期する．
```
gunzip *.gz
fastq_pair file1.fastq file2.fastq
```

# bias5の実行ファイル
```
#PBS -q smps
#PBS -l ncpus=32
##PBS -l mem=495G
#PBS -V

cd ${PBS_O_WORKDIR}

F1='/home/t16965tw/data/metagenome/illumina_whole/202005-08-01-1/Sequence/NW/NW_FDDP202390766-1a_HJVV3DRXX_L1_1.fq.gz'
F2='/home/t16965tw/data/metagenome/illumina_whole/202005-08-01-1/Sequence/NW/NW_FDDP202390766-1a_HJVV3DRXX_L1_2.fq.gz'

metaspades.py -1 $F1 -2 $F2 -o metaspades \
 -t 32 -k auto -m 490
```
