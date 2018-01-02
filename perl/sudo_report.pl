#!/usr/bin/perl -Twn

# This source code is original source code written by Holt Sorenson
# for the SANS GIAC GSEC practical, v1.4b Option 1.
# It was written using PERL 5.8.0 on Debian GNU/Linux 3.0.

use strict;

# globals
our ( %sudo_badpass, %sudo_success, %sudo_badpam );

# begin main loop (process a line)
LINE:
{

    chomp (my $line = $_);

    # explanation of regex operators used below:
    #
    # sudo - a literal string: 's' followed by 'u' followed by 'd' followed by 'o'
    # . - matches any character
    # * - matches zero or more of the preceding expression (greedy). greedy: match
    #     as much as  possible even if there was a match earlier in the string
    # *? - matches zero or more of the preceding expression (non-greedy)
    # ^ - cause the regex engine to match at the beginning of the line of text being considered
    # + - match one or more of the preceding expression
    # | - alternation: match the expression to the left or the right of the '|'
    # {x,y} - match the preceding expression at least x times, but no more that y times
    # {x} - match the preceding expression exactly x times
    # () - grouping: used to group regexes together such that the regex's scope 
    #      is limited to what is inside the parentheses; back reference: stores the
    #      matched text in the scalar variable $n (where n is the nth grouping matched.
    #      The possible range of n is 1...9). 
    # (?:) - same as () but doesn't create a back reference
    # \d - any digit
    # \s - any whitespace character (TAB, SPACE)
    # \w - any word character A-Z, a-z, 0-9, _
    # \[ - to match a character that is used as a regex character, one must escape the
    #      character. [] is used to denote a character class, so [ and ] must be escaped.
    #      when escaped, \[ means literal '[' and \] means literal ']', instead of denoting
    #      a character class
    #
    # These regular expressions are modified by the 'x' operator causing PERL to
    # interpret them as extended regular expressions. Extended regular expressions
    # permit comments and whitespace in the regular expression.
    #
    # These explanations are valid for PERL 5 regular expressions. Other regular expression
    # flavors may differ in there behavior.
    #
    # for more explanation see:
    # http://www.perldoc.com/perl5.8.0/pod/perlre.html
    # http://www.perldoc.com/perl5.8.0/pod/perlrequick.html
    # http://www.perldoc.com/perl5.8.0/pod/perlretut.html

    # the regex that is written in the following 'if' statement was written to match the following
    # message:
    # Jun  3 04:08:05 baz sudo:      foo : 2 incorrect password attempts ; TTY=pts/6 ; PWD=/home/foo ; USER=root ; COMMAND=/bin/bash
    if ($line =~ /^
	    (
		# month  day              time
		\w+\s    (?:\s\d|\d{2})\s  \d{2}:\d{2}:\d{2}
	    )\s

	    # hostname  sudo literal   username 
	    \w+         \ssudo:\s+     (\w+)\s:\s

	    # message
	    (\d+)\sincorrect\spassword\sattempts?\s;\s

	    # sudo invocation information
	    TTY.*?USER=(\w+)\s;\sCOMMAND=(.*)
	    /x
	)
    { $sudo_badpass{$1} = join(' ', $2, "failed password authentication", $3, "times while attempting execution of", $5, "as", $4 ); }
   
    # the regex that is written in the following 'if' statement was written to match the following
    # message:
    # Jun  3 04:07:58 baz PAM_unix[1927]: authentication failure; (uid=0) -> foo for sudo service
    if ($line =~ /^
	    (
		# month  day                time
		\w+\s    (?:\s\d|\d{2})\s   \d{2}:\d{2}:\d{2}
	    )\s

	    # hostname  pam literal
	    \w+\s       PAM_unix\[\d+\]:\sauthentication\sfailure;\s(?:\w+)?

	    # attempted uid     user 
	    \(uid=(\d)\)\s->\s  (\w+)  \sfor\ssudo\sservice
	    /x
	)
    { $sudo_badpam{$1} = join(' ', "Attempted transition to uid", $2, "by", $3); }

    # the regex that is written in the following 'if' statement was written to match the following
    # message:
    # Jun  3 04:07:53 baz sudo:      foo : TTY=pts/6 ; PWD=/home/foo ; USER=root ; COMMAND=/bin/bash
    if ($line =~ /^
	    (
		# month  day                time
		\w+\s    (?:\s\d|\d{2})\s   \d{2}:\d{2}:\d{2}
	    )
	    # hostname  sudo literal   username    sudo invocation information 
	    \s\w+\s     sudo:\s+       (\w+)\s:\s  TTY=.*(USER=\w+)\s;\s(COMMAND=.*)
	    /x
	)
    { $sudo_success{$1} = join(' ', $2, "invoked", $4, "as", $3); }

}
# end main loop



# once all the files have been processed, execute the following to make a report
END
{
    my $ctr = ();
    my $key = ();
    my $nval = ();

    # print out failed password attempts
    $nval = values(%sudo_badpass);
    if ($nval > 0)
    {
	print "\n\nsudo failed password attempts found:\n\n";
	foreach $key (keys %sudo_badpass)
	{
	    print "\t$key: $sudo_badpass{$key}.\n";
	}
    }

    # print out failed PAM sudo authentications
    $nval = values(%sudo_badpam);
    if ($nval > 0)
    {
	$ctr = 1;
	printf "\n\n%d failed PAM sudo authentications found:\n\n", $nval;
	foreach $key (keys %sudo_badpam)
	{
	    printf "\t%05d: $key - $sudo_badpam{$key}.\n", $ctr;
	    $ctr++;
	}
    }

    # print out successful sudo executions
    $nval = values(%sudo_success);
    if ($nval > 0)
    {
	$ctr = 1;
	printf "\n\n%d successful uses of sudo found:\n\n", $nval;
	foreach $key (keys %sudo_success)
	{
	    print "\t$ctr: $key\n\t\t$sudo_success{$key}\n\n";
	    $ctr++;
	}
    }
}

__END__;
