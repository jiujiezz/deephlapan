#!/usr/bin/perl-w
use strict;

my $in=$ARGV[0];
my $out;
if ($in=~/(\S+)\.csv/){
	$out=$1."_rank.csv";
}
open IN, "<$in" or die "cannot open $in:$!";
open OUT, ">$out" or die "cannot open $out:$!";

my @head=split/,/,<IN>;
my ($Annotation,$HLA,$peptide,$bs,$is);
foreach my $count (0..$#head){
	$Annotation = $count if ($head[$count]=~'Annotation');
	$HLA = $count if ($head[$count]=~'HLA');
	$peptide = $count if ($head[$count]=~'Peptide');
	$bs = $count if ($head[$count]=~'binding score');
	$is = $count if ($head[$count]=~'immunogenic score');
}

my (%mark,%mark1);
while (<IN>){
	chomp;
	my @line=split/,/,$_;
	if ($line[$is]>0.5){
		my $info=join",",@line[$HLA,$peptide,$bs,$is];
		$mark{length($line[$peptide])}{$info}=$line[$bs];
		$mark1{length($line[$peptide])}{$info}=$line[$Annotation];
	}
}

print OUT"Annotation,HLA,Peptide,binding score,immunogenic score,rank\n";

foreach my $j (8..11){
	my $i=0;
	foreach my $mut (sort {$mark{$j}{$b}<=>$mark{$j}{$a}} keys %{$mark{$j}}){
		print OUT "$mark1{$j}{$mut},$mut,$i\n";
		$i++;
	}
}
