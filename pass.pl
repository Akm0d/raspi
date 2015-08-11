#!/usr/bin/perl
use strict;
use warnings;

my $pwd = (getpwuid($<))[1];
my $word = "";
system "stty -echo";
eval{
	local $SIG{ALRM} = sub { 
			system "stty echo";
			print "Timeout";
			exit(0);
		};
	alarm 10;
	$word = <STDIN>;
	alarm 0;
	chomp $word;
};
system "stty echo";

if(crypt($word, $pwd) ne $pwd) {
	print "Incorrect";
} else {
	print "Success!";
}

exit(0);
