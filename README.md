# 20x4 LCD Terminal
<pre>
For those who have no monitor to connect to their raspberry pi, this code creates
an lcd terminal for basic bash commands.  It is assumed that files associated with the 
terminal wil be located in the "/etc" folder.  Make sure that "command.py" and "pass.pl" 
are excecutable by typing the following command in the terminal:
</pre>
<code>chmod +x /etc/command.py; chmod +x /etc/pass.pl</code>
<pre>
In order to get terminal access on boot, In the "/etc/init.d" folder create an excecutable script 
with these contents:

#!/bin/sh
python /etc/command.py

On boot, or when this script is run with "python /etc/command.py" It will print the output of
the "hostname" to the first line of the lcd. the output of "hostname -I" will be printed to
the 2nd and 3rd lines. If these are empty it's because the pi hasn't finished it's boot
sequence and obtained an ip address.  The 4th line will ask for the current user's
password.  Typing won't display output, but If you type the correct password the word
"SUCCESS!" will appear and pressing "Enter" will take you to the terminal.  Otherwise the 
word "Incorrect." will appear and pressing "Enter" will repeat the previous sequence.

It will ask for the password of the current user
NOTE: I have root user enabled on my raspberry pi.  This script has not been tested for pi's that 
don't have a root user.

After a successful password submission,the present working directory will be shown with a blinking 
cursor. You can now type commands.  After pressing "Enter" the command will be excecuted.  This 
script strictly supports commands that simply print information. Commands that open a prompt, 
require extra input, or open a program should be avoided.  They will crash the terminal.  
Some examples include: bash,less,more,top,perl,python,vim,nano,ssh,lynx...etc.  Most commands 
have the ability to strictly print output if you pass in the correct arguments. Clever usage of 
commands such as "yes","echo","cat","sed", and "awk" can replace the need for certain comands.

For example, instead of using "less" or "more" I could simply "cat" a file and get the same 
result.  If I need to add something to a file I can use "echo 'content to be added' >> file.name"
To see the result of "top" i could use "top -n 1" for a static output. "sed" and "awk" can be
used instead of "vim" and "nano" to make edits to a file.

Note that the script will execute a command, and then present the output. If a command has a large 
output, such as "apt-get update" or "apt-get upgrade", then nothing will be shown on the display 
until the command has finished running, and the output has been parsed by the script.  

Output is split at whitespace and separated into 20 character long strings.  Duplicate whitespace 
is ignored. Each string is printed onto it's own line. 3 newlines are inserted before the 
sequence and 4 newlines are appended afterwards.  These are to prevent commands that have 
little output from crashing the terminal.

Output can be traversed by pressing the "j" and "k" keys folwing the vim model of movement.  "g" 
can be used to jump to the beginning of output and "G" can be used to jump to the end.
pressing "/" while looking at output switches to search mode and asks for a regular expression 
pattern. After entering a pattern and pressing "Enter" you can use "n" and "N" to search
forwards and backwards for matches to that pattern.  If no matches were found then it will
return you to the beginning of input.

Press "Enter" or "q" to exit the output viewing mode and go back into command mode.

If this script is run on boot, you will also need to type "exit" and press "Enter" from 
command mode to resume the normal boot sequence of the raspberry pi.

WARNING:  If you don't have an LCD screen, and this script is run on boot, then it will 
still expect you to type a password and "exit" before finishing the boot sequence and 
continuing to the desktop.

After exiting, the raspberry pi will print the output of the "hostname" command to the first line
of the lcd and the output of "hostname -I" to the remaining lines
</pre>

