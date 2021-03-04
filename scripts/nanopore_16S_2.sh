#PBS -q medium
#PBS -l ncpus=1
#PBS -V

cd ${PBS_O_WORKDIR}

N_THREADS='1'
PATH1='$working_dir'
PATH2='$data_dir'

home_path=$PATH1
dir_path=$PATH2
PREFIX=$(basename $dir_path)

cd $PREFIX

DB=/home/t16965tw/data/blastDB/SILVA_138_SSURef_NR99_tax_silva/SILVA_138_SSURef_NR99_tax_silva.fasta
QUERY=$home_path/$PREFIX/$PREFIX.trimmed.porechop_.fasta
PROGRAM=blastn
DIR=$(basename $QUERY .fna).$(basename $DB .fasta).$PROGRAM

cd $DIR

# blastが終了したら
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


# ファイル名の変換
python /home/t16965tw/github/NPP/scripts/tools/rename.py /home/t16965tw/github/NPP/data/database/SILVA_138_Taxonomy.txt file_join_1.txt > rename_$PREFIX.txt

python /home/t16965tw/github/NPP/scripts/make_taxbarplot.py $PREFIX rename_$PREFIX.txt $QUERY-header
