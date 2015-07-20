#!/usr/bin/perl
use strict;
use warnings;

my $pwd = (getpwuid($<))[1];
system "stty -echo";
chomp (my $word = <STDIN>);
system "stty echo";

if(crypt($word, $pwd) ne $pwd) {
	print "Incorrect";
} else {
	print "Success!";
}
exit(0);
