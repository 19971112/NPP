
```
# ファイルをダウンロード
wget https://www.arb-silva.de/fileadmin/silva_databases/release_138/Exports/taxonomy/tax_slv_ssu_138.txt.gz
wget https://www.arb-silva.de/fileadmin/silva_databases/release_138/Exports/taxonomy/tax_slv_ssu_138.tre.gz
wget https://www.arb-silva.de/fileadmin/silva_databases/release_138/Exports/taxonomy/taxmap_slv_ssu_ref_nr_138.txt.gz
wget https://www.arb-silva.de/fileadmin/silva_databases/release_138/Exports/SILVA_138_SSURef_NR99_tax_silva_trunc.fasta.gz
wget https://www.arb-silva.de/fileadmin/silva_databases/release_138/Exports/SILVA_138_SSURef_NR99_tax_silva_full_align_trunc.fasta.gz
gunzip *.gz

python convert_rna_to_dna.py \
  -i SILVA_138_SSURef_NR99_tax_silva_trunc.fasta \
  -o SILVA_seqs.fasta
  
python convert_rna_to_dna.py \
  -i SILVA_138_SSURef_NR99_tax_silva_full_align_trunc.fasta \
  -o SILVA_align_seqs.fasta \
  -g
  
python remove_seqs_with_homopolymers.py \
  -i SILVA_seqs.fasta \
  -o SILVA_seqs_polyfilt.fasta
```
