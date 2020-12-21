#PBS -q small
#PBS -l ncpus=1
#PBS -l mem=89G
#PBS -V

cd ${PBS_O_WORKDIR}

makeblastdb -in contigs.fasta -dbtype nucl -parse_seqids
