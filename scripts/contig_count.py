import sys
from Bio import SeqIO

fasta_in = sys.argv[1]

for record in SeqIO.parse(fasta_in, 'fasta'):
    id_part = record.id
    desc_part = record.description
    seq = record.seq
    seq_len = len(seq)
    print(id_part, seq_len)
