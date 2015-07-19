#!/usr/bin/env python3
import re
import string
import subprocess
import os
from getch import getch
import getpass
import time
from sys import stdin
import RPi.GPIO as GPIO
from RPLCD import CharLCD,CursorMode,cursor,ShiftMode,cleared
GPIO.setwarnings(False)
lcd = CharLCD(cols=20, rows=4,
                pin_rw=None,
                pin_rs=21,
                pin_e=20,
                pins_data=[25,24,23,18],
				#d4, d5, d6, d7
                numbering_mode=GPIO.BCM)
lcd.cursor_mode = CursorMode.blink
my_cmd = ""
while my_cmd != 'exit':
	my_cmd = ""
	lcd.clear();
	my_pwd = os.getcwd();
	lcd.cursor_pos = (0,0)
	lcd.write_string(getpass.getuser())
	lcd.write_string('@')
	my_hostname = subprocess.check_output("hostname",shell=True)
	hostname = my_hostname.split()
	lcd.write_string(hostname[0])
	lcd.write_string(':')
	lcd.write_string(os.getcwd())
	lcd.write_string('$');
	my_char = 'c'
	while my_char != '\r' and my_char != '\n':
		my_char = getch()
	#handle Backspace
	#	if my_char == '\b' or my_char == '\x08' or my_char == '\x7f':
	#		my_cmd[:-1]
	#	else:
		if my_char != '\r' and my_char != '\n':
			my_cmd += my_char
			lcd.write_string(my_char)
	lcd.clear()
	if my_cmd !='exit':
		my_output = subprocess.check_output(my_cmd,shell=True)
		#cut tabs down to spaces or new lines
		#re.sub("\s+","\n",my_output)
		lines =	my_output.split()
		my_length = len(lines)
		if my_length <= 4:
			# cover cases with short list
			lines.append("\n");
			lines.append("\n");
			lines.append("\n");
			lines.append("\n");
		my_char = 'c' 
		a = 0;
		b = 1;
		c = 2; 
		d = 3;
		#Scroll through text using letters 'j' and 'k'
		while my_char != '\r' and my_char != '\n' and my_char != 'q':
			lcd.clear()
			lcd.cursor_pos = (0,0)
			lcd.write_string(lines[a])
			lcd.cursor_pos = (1,0)
			lcd.write_string(lines[b])
			lcd.cursor_pos = (2,0)
			lcd.write_string(lines[c])
			lcd.cursor_pos = (3,0)
			lcd.write_string(lines[d])
			my_char = getch()
			if my_char == 'j' and d < (my_length-1):
				a += 1;
				b += 1;
				c += 1;
				d += 1;
			elif my_char =='k' and a > 0:
				a -= 1;
				b -= 1;
				c -= 1;
				d -= 1;
			elif my_char == 'G':
				a = my_length-4;
				b = my_length-3;
				c = my_length-2;
				d = my_length-1;
			elif my_char == 'g':
				a = 0;
				b = 1;
				c = 2;
				d = 3;
	else:
		lcd.write_string("Goodbye")
