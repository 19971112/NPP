# blastの分散処理


```
DB=/bio/db/fasta/nt/nt
QUERY=/home/t16965tw/github/NPP/analysis/2020-03-20/blast/sequences.fasta
PROGRAM=blastn

DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM

mkdir $DIR; cd $DIR
perl /home/t16965tw/scripts/tom/q_blast_2020-03-20.pl $QUERY $DB -program $PROGRAM -evalue 1e-05 -max_target_seqs 1 -outfmt 6 -num_threads 1 -nseq 20

for i in *.sh; do qsub $i; done
qstat
```


## 実行が完了したら，実行ファイルがあるディレクトリに移動して，以下のコマンドを実行する
```
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
cat file_join_2.txt | perl -pe 's/(UniRef50|UniRef90|UniRef100)_//g;' >> $PROGRAM-$(basename $QUERY .fasta)-$(basename $DB .fasta)-annotation.txt

```
