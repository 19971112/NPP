#!/usr/bin/env perl

use strict;
use warnings;
use POSIX qw{ceil};
use Getopt::Long;

#parameters
my $program = 'blastp';
my $evalue=1e-05;
my $max_target_seqs=1;
my $outfmt=0;
my $num_threads=40;
my $nseq = 10;
my $out = 'bl';

GetOptions(
	   'program=s' => \$program,
	   'evalue=s' => \$evalue,
	   'max_target_seqs=i' => \$max_target_seqs,
	   'outfmt=i' => \$outfmt,
	   'num_threads=i' => \$num_threads,
	   'nseq=i' => \$nseq,
	   'out=s' => \$out,
	   );

if($#ARGV < 1) {
	print "Usage: $0 <fasta query> <fasta database>
Example: $0 all.fasta uniref90.fasta
Options:
    -program <>, blast program [$program]
    -evalue <>, blast E-value [$evalue]
    -max_target_seqs <>, max_target_seqs [$max_target_seqs]
    -outfmt <>, outfmt [$outfmt]
    -num_threads <>, num_threads [$num_threads]
    -nseq <>, number of query sequences per nodes [$nseq]
    -out <>, suffix used for the blast output [$out]\n";
	exit;
}

my $QUERY = $ARGV[0];
my $DB = $ARGV[1];
system("awk 'BEGIN {total=0; num=".$nseq.";} /^>/ {if(total%num==0){file=sprintf(\"%04d.fa\",total/num+1);} print >> file; total++; next;} { print >> file; close(file)}' < ".$QUERY);
my $job = `ls *.fa | wc -l`; chomp $job;
print "This script generates $job fasta files <*.fa> and $job qsub files <*.sh>\n";

for (my $i = 1; $i <= $job; ++$i) {
    my $number = sprintf("%04d",$i);
    open OUT, ">$number.sh";
    #
    print OUT
"#!/bin/bash
#PBS -q small
#PBS -l ncpus=$num_threads
#PBS -N $out.$number

cd \${PBS_O_WORKDIR}
$program -db $DB -query $number.fa -out $number.$out -evalue $evalue -max_target_seqs $max_target_seqs -outfmt $outfmt -num_threads $num_threads
#-use_sw_tback \\
echo \"$number\" >> DONE
\n";
    close OUT;
}

__END__
# prepare blast qsub script (qsub_blast.sh) for cluster
# Tomoro Warashina (Haruo Suziki)
# Last update: 2019-03-13
http://www.nibb.ac.jp/cproom/wiki # queue: small (580); medium (200); large (20)
http://togotv.dbcls.jp/20110608.html
http://togotv.dbcls.jp/20110420.html
How To Split One Big Sequence File Into Multiple Files With Less Than 1000 Sequences In A Single File https://www.biostars.org/p/13270/
