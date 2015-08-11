#!/usr/bin/perl
use strict;
use warnings;

my $continue =  "";
eval{
	local $SIG{ALRM} = sub {
			print "Timeout";
			exit(0);
		};
	alarm 3;
	$continue = <STDIN>;
	alarm 0;
};

print "Continue";
exit (0);
