from sys import argv
import datetime
from os.path import expanduser
import os
import sys
import subprocess

def write_to_clipboard(output):
	process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
	process.communicate(output.encode('utf-8'))

home = expanduser('~')
filePath = home + '/.notes.txt'
EXIT_STR = 'EXIT NOW XX__XX'

def stdPrint(txt):
	sys.stdout.write(txt + '\n')

def printDivider():
	stdPrint('_____________________________________\n')

def currTimestamp():
	return '({:%Y-%m-%d %H:%M:%S})'.format(datetime.datetime.now())

def takeNote(title, msg):
	if len(title) == 0:
		stdPrint('nte: Take Note')
		title = raw_input('Enter note title:')
	if len(msg) == 0:
		msg = raw_input('Enter note message:')
	if len(title) == 0 and len(msg) == 0:
		stdPrint('Failed Recording: Invalid title and message')
		return
	txtToWrite = currTimestamp() + ' ' + title + ': ' + msg + '\n'
	try:
		with open(filePath, 'a') as notesFile:
			notesFile.write(txtToWrite)
	except:
		with open(filePath, 'w') as notesFile:
			notesFile.write(txtToWrite)
	stdPrint('nte: Note recorded')

def areValidComponents(components, numThereShouldBe, lines):
	if len(components) == numThereShouldBe:
		for c in components:
			if c.isdigit() == False:
				stdPrint('Command: Invalid arguments')
				return False
			cInt = int(c)
			if cInt >= len(lines) or cInt < 0:
				stdPrint('Command: Invalid arguments')
				return False
	else:
		stdPrint('Command: Invalid arguments')
		return False
	return True

def delete(components, lines):
	if areValidComponents(components, 1, lines) == False:
		return lines
	lineNum = int(components[0])
	del lines[lineNum]
	return lines

def move(components, lines):
	if areValidComponents(components, 2, lines) == False:
		return lines
	lineNumA = int(components[0])
	lineNumB = int(components[1])
	line = lines.pop(lineNumA)
	lines.insert(lineNumB, line)
	return lines

def copy(components, lines):
    if areValidComponents(components, 1, lines) == False:
        return lines
    write_to_clipboard(lines[int(components[0])])
    return lines

def clear(components, lines):
	confirm = raw_input('Are you sure you would like to clear all notes? This can NOT be undone (y/n)')
	if confirm == 'y':
		return []
	elif confirm == 'n':
		return lines

def exit(*argsThatWontBeUsed):
	return [EXIT_STR]

cmds = {'d': delete, 'm': move, 'c': copy, 'clr': clear, 'x': exit}

def processCommand(cmdStr, lines):
	components = cmdStr.split(' ')
	if len(components) < 1:
		stdPrint('Invalid command')
		return lines
	cmd = components[0]
	if cmd not in cmds:
		stdPrint('Invalid command')
		return lines
	return cmds[cmd](components[1:], lines)

def showCommandHelp():
	stdPrint('''Commands: 
	d {line number A} - delete line number A
	m {line number A} {line number B} - move line number A to line number B
	c {line number A} - copy line number A to clipboard
        clr - clear notes file
	x - exit''')

def viewNotes():
	stdPrint('nte: View Notes')
	printDivider()
	with open(filePath, 'r+') as notesFile:
		lines = []
		contents = ''
		i = 0
		for line in notesFile.readlines():
			contents += line
			line = line.strip('\n')
			if len(line) >= 1:
				lines.append(line.strip('\n'))
				printDivider()
				stdPrint(str(i) + '-> ' + line)
				i += 1
		printDivider()
		showCommandHelp()
		cmdStr = raw_input('Enter a command:')
		while cmdStr != '':
			newLines = processCommand(cmdStr, lines)
			if len(newLines) == 1 and newLines[0] == EXIT_STR:
				break
			else:
				lines = newLines
			newFileContents = ''
			for line in lines:
				newFileContents += line + '\n'

			notesFile.seek(0)
			notesFile.truncate()
			notesFile.write(newFileContents)

			os.system('clear')

			stdPrint('nte: View Notes')
			printDivider()
			
			i = 0
			for line in lines:
				line = line.strip('\n')
				if len(line) >= 1:
					printDivider()
					stdPrint(str(i) + '-> ' + line)
					i += 1
			
			printDivider()
			showCommandHelp()
			cmdStr = raw_input('Enter a command:')

def main():
	if len(argv) == 1:
		#Take note
		os.system('clear')
		takeNote('', '')
	elif len(argv) == 3:
		takeNote(argv[1], argv[2])
	elif len(argv) == 2:
		if argv[1] == 'v':
			#View notes
			os.system('clear')
			viewNotes()
                elif argv[1] == 'e':
                        #Open in Vim
                        os.system ('vim ' + filePath)
        else:
		stdPrint('Invalid arguments')

if __name__ == "__main__":
	main()
