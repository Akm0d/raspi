# 20x4 LCD Terminal
<pre>
For those who have no monitor to connect to their raspberry pi, this code gives access to a terminal. 
It is assumed that files associated with the terminal wil be located in the "/etc" folder.  Make sure
that "command.py" and "pass.py" are excecutable by typing the following command in the terminal:
</pre>
<code>chmod +x command.py; chmod +x pass.pl</code>
<pre>
In order to get terminal access on boot, In the "/etc/init.d" folder create an excecutable script 
with these contents:

#!/bin/sh
python /etc/command.py

On boot, or when this script is run with "python /etc/command.py"

It will ask for the password of the current user
NOTE: I have root user enabled on my raspberry pi.  This script has not been tested for pi's that 
don't have a root user.

After a successful password submission,the present working directory will be shown with a blinking 
cursor. You can now type commands.  After pressing "Enter" the command will be excecuted.  This 
script strictly supports commands that simply print information. Commands that open a prompt, 
require extra input, or open a program should be avoided.  They will crash the terminal.  
Some examples include: bash,vim,nano,firefox,lynx...etc.  

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

If this script is run on boot, you will also need to type "exit" and press "Enter" from command mode to resume the normal boot sequence of the raspberry pi.

WARNING:  If you don't have an LCD screen, and this script is run on boot, then it will still expect you to type a password and "exit" before finishing the boot sequence and continuing to the desktop.

</pre>

