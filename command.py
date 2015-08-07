#!/usr/bin/env python3
import re
import string
import subprocess
import os
from os.path import expanduser
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
                pins_data=[18,23,24,25],
				#d4, d5, d6, d7
                numbering_mode=GPIO.BCM)
lcd.cursor_mode = CursorMode.blink
my_cmd = ""
#ASK FOR ROOT LOGIN BEFORE EXECUTING ANY COMMANDS
#VERIFY ROOT PASSWORD
my_username = getpass.getuser()
my_perl = ""
while my_perl != "Success!":
	lcd.clear()
	my_name = subprocess.check_output("hostname",shell=True)
	lcd.write_string(my_name)
	lcd.cursor_pos = (1,0)
	my_ip = subprocess.check_output("hostname -I",shell=True)
	lcd.write_string(my_ip)
	lcd.cursor_pos = (3,0)
	lcd.write_string(my_username)
	lcd.write_string("\'s password:")
	my_perl = subprocess.check_output("/root/developement/pi_scripts/pass.pl ",shell=True)
	lcd.clear()
	lcd.write_string(my_perl)
	my_char = getch()
my_history = list()
my_hist_file = expanduser("~") + "/.pi_history"
with open(my_hist_file, 'w+') as f:
	my_history = [x.strip('\n') for x in f.readlines()]
my_history.append("")
#create a bashrc alias to run this script
#have it detect a device on the GPIO pins and boot with the 
#LCD terminal only if a device is detected
while my_cmd != 'exit':
	my_cmd = ""
	lcd.clear();
	my_pwd = os.getcwd()
	lcd.cursor_pos = (0,0)
	lcd.write_string(getpass.getuser())
	lcd.write_string('@')
	my_hostname = subprocess.check_output("hostname",shell=True)
	hostname = my_hostname.split() 
	lcd.write_string(hostname[0])
	lcd.write_string(':')
	lcd.write_string(os.getcwd())
	lcd.write_string('$')
	my_char = 'c'
	#history variables
	hist_length = len(my_history)
	my_place = hist_length -1
	while my_char != '\r' and my_char != '\n':
		my_char = getch()
		#handle Backspace
		if my_char == '\x7f':
			my_cmd = my_cmd[:-1]
			lcd.clear()
			my_pwd = os.getcwd()
			lcd.cursor_pos = (0,0)
			lcd.write_string(getpass.getuser())
			lcd.write_string('@')
			my_hostname = subprocess.check_output("hostname",shell=True)
			hostname = my_hostname.split() 
			lcd.write_string(hostname[0])
			lcd.write_string(':')
			lcd.write_string(os.getcwd())
			lcd.write_string('$')
			lcd.write_string(my_cmd)
		#Go up and down through history
		elif my_char == '\033':#the escape sequence
			getch()#skip a token
			my_arrow = getch()#read arrow key value
			if (my_arrow == 'A' or my_arrow == 'C') and my_place > 0:#up/right
				my_place -= 1
			elif (my_arrow == 'B' or my_arrow == 'D') and my_place < hist_length-1:#down/left
				my_place += 1
			my_cmd = my_history[my_place]
			lcd.clear()
			my_pwd = os.getcwd()
			lcd.cursor_pos = (0,0)
			lcd.write_string(getpass.getuser())
			lcd.write_string('@')
			my_hostname = subprocess.check_output("hostname",shell=True)
			hostname = my_hostname.split() 
			lcd.write_string(hostname[0])
			lcd.write_string(':')
			lcd.write_string(os.getcwd())
			lcd.write_string('$')
			lcd.write_string(my_cmd)
		elif my_char != '\r' and my_char != '\n':
			my_cmd += my_char
			lcd.write_string(my_char)
	my_history.insert(hist_length-2,my_cmd)#commands will be the second to last item
	temp_cmd = "echo \"" + my_cmd + "\" >> ~/.pi_history"
	try:
		subprocess.check_output(temp_cmd, shell=True,stderr=subprocess.STDOUT)
	except Exception as err:
		print err.output
	lcd.clear()
	if not my_cmd:
		lcd.write_string("no command entered")
	elif re.compile("^\s*cd .+").match(my_cmd):
		my_dir = re.sub("^\s*cd\s*","",my_cmd)
		try:
			os.chdir(my_dir)
		except:
			lcd.clear()
			lcd.write_string("\"")
			lcd.write_string(my_dir)
			lcd.write_string("\" does not exist in this path")
			getch()
	elif re.compile("^\s*cd").match(my_cmd):
		lcd.clear()
		my_dir = "/"
		my_dir += getpass.getuser()
		try:
			os.chdir(my_dir)
		except:
			lcd.clear()
			lcd.write_string("\"")
			lcd.write_string(my_dir)
			lcd.write_string("\" does not exist in this path")
			getch()
	elif my_cmd !='exit':
		if re.compile("\s*history\s*").match(my_cmd):
			my_cmd ="cat ~/.pi_history"
		try:
			my_output = subprocess.check_output(my_cmd,shell=True,stderr=subprocess.STDOUT)
		except Exception as e:
		#cut tabs and spaces down new lines
			my_output = str(e.output)
		#re.sub("\s+","\n",my_output)
		my_words =	my_output.split()
		lines = list()
		searched = list()
		def chunkstring(string, length):
		    return (string[0+i:length+i] for i in range(0, len(string), length))
		##also split strings longer than 20 characters into two strings
		for item in my_words:
			for chunk in chunkstring(item,20):
				lines.append(chunk)
		lines.insert(0,"\n")
		lines.insert(0,"\n")
		lines.insert(0,"\n")
		my_length = len(lines)
		for l,k in enumerate(lines):
			if k != "\n":
				searched.append(l)
		search_length = len(searched)
		search_pos = 0
		# cover cases with short list
		lines.append("\n")
		lines.append("\n")
		lines.append("\n")
		lines.append("\n")
		my_char = 'c' 
		#Starting point for a on lcd screen
		a = 3
		#Scroll through text using letters 'j' and 'k'
		while my_char != '\r' and my_char != '\n' and my_char != 'q':
			lcd.clear()
			lcd.cursor_pos = (0,0)
			lcd.write_string(lines[a])
			lcd.cursor_pos = (1,0)
			lcd.write_string(lines[a+1])
			lcd.cursor_pos = (2,0)
			lcd.write_string(lines[a+2])
			lcd.cursor_pos = (3,0)
			lcd.write_string(lines[a+3])
			my_char = getch()
			if my_char == 'j' and (a+3) < (my_length-1):
				a += 1
			elif my_char =='k' and a > 0:
				a -= 1
			elif my_char == 'G':
				a = my_length-4
			elif my_char == 'g':
				a = 3
			#search through the output and use 'n' and 'N' to jump to those lines
			elif my_char == '/':
				new_char = 'n'
				lcd.clear()
				lcd.write_string("pattern: ")
				lcd.cursor_pos = (1,0)
				my_search = ""
				searched = list()
				while new_char != '\r' and new_char != '\n':
					new_char = getch()
				#handle Backspace
					if new_char == '\x7f':
						my_search = my_search[:-1]
						lcd.clear()
						lcd.write_string("pattern: ")
						lcd.cursor_pos = (1,0)
						lcd.write_string(my_search)
					if new_char != '\r' and new_char != '\n' and new_char != '\x7f':
						my_search += new_char
						lcd.write_string(new_char)
				#Find that string in the array of output
				for i, j in enumerate(lines):
					matchobj = None
					oust = None
					try:
						matchobj = re.match(my_search,j)
					except:
						lcd.clear()
						lcd.write_string("invalid             ")
						lcd.write_string("regular             ")
						lcd.write_string("expression          ")
						lcd.write_string(my_search)
						oust = "true"
						getch()
						break
					if matchobj:
						searched.append(i);
				search_length = len(searched)
				if search_length == 0:
					searched.append(my_length+3)
				search_pos = 0
				if oust == "true":
					a = 3
				else:
					a = searched[0]-3
			elif my_char == 'n':
				if search_pos < (search_length -1):
					search_pos += 1
				a = searched[search_pos]-3
			elif my_char == 'N':
				if search_pos > 0:
					search_pos -= 1 
				a = searched[search_pos]-3
	else:
		lcd.clear()
		my_name = subprocess.check_output("hostname",shell=True)
		lcd.cursor_pos = (0,0)
		lcd.write_string(my_name)
		my_ip = subprocess.check_output("hostname -I",shell=True)
		lcd.cursor_pos = (1,0)
		lcd.write_string(my_ip)
