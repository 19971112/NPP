# mockの解析

last-update 2020-12-29
wt

# rep-seqをblastに当てる

```
DB=/home/t16965tw/data/blastDB/SILVA_138_SSURef_NR99_tax_silva/SILVA_138_SSURef_NR99_tax_silva.fasta
QUERY=/home/t16965tw/github/NPP/analysis/2020-12-12/mock_sequences.fasta
PROGRAM=blastn
DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM
mkdir $DIR; cd $DIR

perl ~/github/NPP/scripts/blast/q_blast_2020-12.pl $QUERY $DB -program $PROGRAM -evalue 1e-05 -max_target_seqs 1 -outfmt 6 -num_threads 1 -nseq 10
for i in *.sh; do qsub $i; done
```
