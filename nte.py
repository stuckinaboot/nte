from sys import argv
import datetime
from os.path import expanduser
import os
import sys

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
		stdPrint('NTE: Take Note:')
		title = input('Enter note title:')
	if len(msg) == 0:
		msg = input('Enter note message:')
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
	stdPrint('NTE: note recorded')

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

def clear(components, lines):
	confirm = input('Are you sure you would like to clear all notes? This can NOT be undone (y/n)')
	if confirm == 'y':
		return []
	elif confirm == 'n':
		return lines

def exit(*argsThatWontBeUsed):
	return [EXIT_STR]

cmds = {'d': delete, 'm': move, 'clr': clear, 'x': exit}

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
	clr - clear notes file
	x - exit''')

def viewNotes():
	stdPrint('NTE: View Notes')
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
				stdPrint(str(i) + '-> ' + line)
				i += 1
		printDivider()
		showCommandHelp()
		cmdStr = input('Enter a command:')
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

			stdPrint('NTE: View Notes')
			printDivider()
			
			i = 0
			for line in lines:
				line = line.strip('\n')
				if len(line) >= 1:
					stdPrint(str(i) + '-> ' + line)
					i += 1
			
			printDivider()
			showCommandHelp()
			cmdStr = input('Enter a command:')

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
	else:
		stdPrint('Invalid arguments')

if __name__ == "__main__":
    main()