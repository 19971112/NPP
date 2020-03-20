# blastの分散処理


```
#DB=/bio/db/blast/db/refseq_genomic
DB=/bio/db/blast/db/nt
#QUERY=/home/t16965tw/projects/Wolbachia/data/Wolbachia_phage_WO.txt.faa
QUERY=/home/t16965tw/github/NPP/analysis/2020-03-20/test.fna
PROGRAM=blastn
DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM
mkdir $DIR; cd $DIR
perl /home/t16965tw/scripts/tom/q_blast2.pl $QUERY $DB -program $PROGRAM -evalue 1e-05 -max_target_seqs 1 -outfmt 6 -num_threads 1 -nseq 1
for i in *.sh; do qsub $i; done

qstat
```
