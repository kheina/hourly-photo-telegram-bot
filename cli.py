import requests
import json
import sched, time
import dropbox
import os
import random

def cls():
	os.system('cls' if os.name=='nt' else 'clear')
	print('(c) 2017 Snep Corporation. All rights reserved.\n')

#initialize the dropbox folder
dbx = dropbox.Dropbox('iPVSiTTotuYAAAAAAAEgnRwVETJXdTYNZ_b5QdezBhSF9QN97HhzU6EqObRElMaM')
#enter your dropbox access token in the ('') above

#telegram bot auth token (given by @BotFather upon your bot's creation)
token = '394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c'
#enter your telegram bot's auth token in the '' above

#the id of the bot itself
botID = 394580059
#enter your telegram bot's id after the = above

#initialize all the lists and variables
fileIDs = []
usedIDs = []
forwardList = []
forwardInfoList = []
newForwardList = []
lastUpdateID = 000
rand = random.seed()

command = ''
commandList = ['>refresh CLI', 'getMe', 'getChat', 'getChatAdministrators', 'getUpdates', 'sendMessage', 'sendPhoto']
optionalCommandsList = {}
optionalCommandsList['getChat'] = ['>send request', 'chat_id']
optionalCommandsList['getChatAdministrators'] = ['>send request', 'chat_id']
optionalCommandsList['getUpdates']  = ['>send request', '>clear updates', 'offset', 'limit', 'timeout']
optionalCommandsList['sendMessage'] = ['>send request', 'chat_id', 'text', 'parse_mode', 'disable_web_page_preview', 'disable_notification', 'reply_to_message_id', 'reply_markup', ]
optionalCommandsList['sendPhoto']   = ['>send request', 'chat_id', 'photo', 'caption', 'disable_notification', 'reply_to_message_id']
optionalCommandsList['parse_mode'] = ['Markdown', 'HTML']
optionalCommandsList['disable_web_page_preview'] = ['true', 'false']
optionalCommandsList['disable_notification'] = ['true', 'false']





def startup() :
	cls()

	currenttime = (time.time())
	
	noowtime = ''
	if time.localtime(currenttime).tm_hour < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_hour) + ':'
	if time.localtime(currenttime).tm_min  < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_min)
	
	print('current time:', noowtime)
	
	#reinitialize all the lists and variables as global
	global token
	global botID
	global fileIDs
	global usedIDs
	global forwardList
	global newForwardList
	
	print('downloading fileIDs.json')
	dbxfileIDs = dbx.files_download('/fileIDs.json')
	fileIDs = dbxfileIDs[1].json()
	print(len(fileIDs), 'file ids')
	
	print('downloading usedIDs.json')
	dbxusedIDs = dbx.files_download('/usedIDs.json')
	usedIDs = dbxusedIDs[1].json()
	print(len(usedIDs), 'used ids')
	
	optionalCommandsList['photo'] = usedIDs
	optionalCommandsList['photo'].insert(0, 'random')
	optionalCommandsList['photo'].append('random')
	report_forwards()
	print()
#





def report_forwards() :
	#print('report_forwards()')
	global token
	global forwardList
	global forwardInfoList
	
	forwardInfoList = []
	print('downloading forwardList.json')
	dbxforward = dbx.files_download('/forwardList.json')
	forwardList = dbxforward[1].json()
	print(len(forwardList), 'forwards')
	newForwardList = ['send request']
	for i in range(len(forwardList)):
		newForwardList.append(str(forwardList[i]))
	optionalCommandsList['chat_id']  = newForwardList

	request = 'https://api.telegram.org/bot' + token + '/getChat'
	
	print()
	for i in range(len(forwardList)):
		response = requests.get(request, {'chat_id': forwardList[i]})
		response = response.json()
		if response['ok'] :
			print('forward[', str(i+1),']: (', str(response['result']['id']), ') ', response['result']['title'], sep='')
			forwardInfoList.append('(' + str(response['result']['id']) + ') ' + response['result']['title'])
		else :
			print('forward[', str(i+1),']: (', str(forwardList[i]), ') ', response['description'], sep='')
			forwardInfoList.append('(' + str(forwardList[i]) + ') ' + response['description'])
	print('done.')
#





def parse_request() :
	#print('parse_request()')
	global command
	global lastUpdateID

	print()
	areyousure = request = ''
	areyousure = input('Are you sure? Y/n>')
	if areyousure == 'y' or areyousure == '' :
		response = requests.get(command)
		response = response.json()
		if '/getUpdates' in command and response['ok'] and len(response['result']) > 0:
			lastUpdateID = response['result'][len(response['result']) - 1]['update_id']
		print('\nresponse:')
		print_json_formatted(response)
	print('done.')
#





def take_input() :
	#print('take_input()')
	global command
	command = ''
	
	print('\n')
	for i in range(len(commandList)) :
		print('[' + str(i) + ']' + commandList[i])
	print('\nenter your command below or enter a number from the list.\nall requests will be formatted like so:\n    https://api.telegram.org/bot <token> /COMMAND')
	command = input('>')
	#print(command)
	if parse_command() :
		command = 'https://api.telegram.org/bot' + token + '/' + command
		print(command)
		parse_request()
#





def parse_command() :
	#print('parse_command()')
	global command
	global commandList
	global lastUpdateID
	
	tempCommand = command
	
	if tempCommand.isdigit() and int(command) < len(commandList) :
		if int(command) == 0 : 
			startup()
			return False
		command = tempCommand = commandList[int(command)]
	continueLooping = True
	while continueLooping :
		print('\n')
		if command in optionalCommandsList :
			for i in range(len(optionalCommandsList[command])) :
				print('[' + str(i) + ']' + optionalCommandsList[command][i])
		else :
			print('[0]>send request')
		print('\nenter your command below or enter a number from the list.\nall requests will be formatted like so:\n    https://api.telegram.org/bot <token> /COMMAND?OPTIONAL=VALUE&OPTIONAL=VALUE')
		print('\ncurrent command: ' + tempCommand)
		optionalCommand = input(tempCommand + '>')
		
		if optionalCommand.isdigit() and int(optionalCommand) == 0 :
			continueLooping = False
			command = tempCommand
		elif optionalCommand == '':
			continueLooping = False
			command = tempCommand
		else :
			if optionalCommand.isdigit() and int(optionalCommand) < len(optionalCommandsList[command]) :
				optionalCommand = optionalCommandsList[command][int(optionalCommand)]
				
			#PUT NONSTANDARD COMMAND LISTS HERE!		##########
			if optionalCommand == 'chat_id' :
				print()
				for i in range(len(forwardList)):
					print('forward[', str(i+1),']: ', forwardInfoList[i], sep='')
			elif optionalCommand == '>clear updates' :
				command = tempCommand = tempCommand + '?&offset=' + str(lastUpdateID + 1)
				return True
			#end nonstandard commands					##########
			if optionalCommand in optionalCommandsList :
				print()
				for i in range(len(optionalCommandsList[optionalCommand])) :
					print('[' + str(i) + ']' + optionalCommandsList[optionalCommand][i])
				print('\nenter your command below or enter a number from the list.')
				optionalCommandValue = input(tempCommand + '&' + optionalCommand + '>')
				if optionalCommandValue == '' and len(optionalCommandsList[optionalCommand]) > 0 :
					optionalCommandValue = optionalCommandsList[optionalCommand][0]
				elif optionalCommandValue.isdigit() and int(optionalCommandValue) < len(optionalCommandsList[optionalCommand]) :
					optionalCommandValue = optionalCommandsList[optionalCommand][int(optionalCommandValue)]
			else :
				optionalCommandValue = input(tempCommand + '&' + optionalCommand + '>')
			
			#PUT NONSTANDARD COMMAND LISTS HERE!		##########
			if optionalCommandValue == 'random' :
				randomint = random.randint(0, len(optionalCommandsList[optionalCommand]) - 2)
				print(randomint)
				optionalCommandValue = optionalCommandsList[optionalCommand][randomint]
			#end nonstandard commands					##########
			
			if '?' in tempCommand :
				tempCommand = tempCommand + '&' + optionalCommand + '=' + optionalCommandValue
			else :
				tempCommand = tempCommand + '?' + optionalCommand + '=' + optionalCommandValue

			optionalCommand = ''
			optionalCommandValue = ''
	#if optionalCommand.isdigit() and int(optionalCommandValue) < len(optionalCommandsList[command]) :
	#	optionalCommand = '&' + optionalCommand + '=' + optionalCommandsList[command][optionalCommandValue]
	#print(command)
	return True
#





def print_json_formatted(jsonToPrint) :
	#print('print_json_formatted(jsonToPrint)')
	#indent = ''
	#indentIncrement = '    '
	
	#stringVar = json.dumps(jsonToPrint)
	#for c in stringVar :
	#	if c == '{' :
	#		print('\n' + indent + '{\n' + indent + indentIncrement, end='')
	#		indent = indent + indentIncrement
	#	elif c == '}' :
	#		indent = indent[:-len(indentIncrement)]
	#		print('\n' + indent + '}', end='')
	#	elif c == '[' :
	#		print('\n' + indent + '[', end='')
	#		indent = indent + indentIncrement
	#	elif c == ']' :
	#		indent = indent[:-len(indentIncrement)]
	#		print('\n' + indent + ']', end='')
	#	elif c == ',' :
	#		print(',\n' + indent[:-1], end='')
	#	#elif c == '\n' :
	#	#	print(indent)
	#	else :
	#		print(c, end='')
	print(json.dumps(jsonToPrint, indent=4, sort_keys=True))
	print()
#





startup()
while True:
	take_input()