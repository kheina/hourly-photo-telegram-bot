import requests
import json
import sched, time
import dropbox

#initialize the dropbox folder
dbx = dropbox.Dropbox('iPVSiTTotuYAAAAAAAEu9Wd6M_ltY0K0amq3pGvEB6NAUAcvVBOUllG4ErHFM8sq')
#enter your dropbox access token in the ('') above

#telegram bot auth token (given by @BotFather upon your bot's creation)
token = '394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c'
#enter your telegram bot's auth token in the '' above

#the chat_id of the channel where all the pictures will be posted
channel = -1001084745741
#enter your telegram channel's chat_id after the = above

#the id of the bot itself
botID = 394580059
#enter your telegram bot's id after the = above

#initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

#initialize all the lists and variables
admins = [118819437]	#this is in case the admin download from dropbox fails
fileIDs = []
usedIDs = []
forwardList = []
delay = 180
timezone = -5
report = ''
sendReport = False



def update():
	print('update()')
	#reinitialize all the lists and variables as global
	global token
	global botID
	global admins
	global fileIDs
	global usedIDs
	global forwardList
	global delay
	global timezone
	global report
	global sendReport	
	report = ''
	
	print('reading admins.json')
	dbxadmins = dbx.files_download('/admins.json')
	admins = dbxadmins[1].json()
	print(len(admins), 'admins')
	
	print('reading fileIDs.json')
	dbxfileIDs = dbx.files_download('/fileIDs.json')
	fileIDs = dbxfileIDs[1].json()
	print(len(fileIDs), 'file ids')
	
	print('reading usedIDs.json')
	dbxusedIDs = dbx.files_download('/usedIDs.json')
	usedIDs = dbxusedIDs[1].json()
	print(len(usedIDs), 'used ids')
	
	print('reading forwardList.json')
	dbxforward = dbx.files_download('/forwardList.json')
	forwardList = dbxforward[1].json()
	print(len(forwardList), 'forwards')
	
	print('reading delay.json')
	dbxdelay = dbx.files_download('/delay.json')
	delay = dbxdelay[1].json()
	print(delay, 'minute delay')

	print('reading timezone.json')
	dbxtime = dbx.files_download('/timezone.json')
	timezone = dbxtime[1].json()
	print('UTC', timezone)

	print()
	
	print("getUpdates")
	request = 'https://api.telegram.org/bot' + token + '/getUpdates'
	response = requests.get(request)
	#print(response.url)
	response = response.json()
	if response['ok'] :
		print('response:', 'ok')
		updateList = response['result']
	else :
		print('response not ok')
		#BREAK

	print(' updates:', len(updateList))


	while len(updateList) > 0 :
		for i in range(len(updateList)):
			#print()
			print('update_id:', updateList[i]['update_id'], '|', end=' ')
			if 'message' in updateList[i] :
				#print('  chat id:', updateList[i]['message']['chat']['id'])
				if updateList[i]['message']['chat']['id'] in admins :
					if 'photo' in updateList[i]['message']:
						#print('photo ids:', len(updateList[i]['message']['photo']))
						largestfile = 0
						largestfileid = 0
						for j in range(len(updateList[i]['message']['photo'])):
							if updateList[i]['message']['photo'][j]['file_size'] > largestfile :
								largestfileid = updateList[i]['message']['photo'][j]['file_id']
								#print('new largest file:', largestfileid)
						
						#print('largest file from update', updateList[i]['update_id'], ':', largestfileid)
						if largestfileid in fileIDs :
							print('fileIDs already contains this photo')
						else:
							fileIDs.append(largestfileid)
							print('file_id added', end=' ') 
							if 'from' in updateList[i]['message'] :
								if 'username' in updateList[i]['message']['from'] :
									print('(from ', updateList[i]['message']['from']['username'], ')', sep='')
								else :
									print('(from ', updateList[i]['message']['from']['first_name'], ' (', updateList[i]['message']['from']['id'], '))', sep='')
							else :
								print('')
					else :
						#MESSAGE DOESN'T CONTAIN A PICTURE, PUT PARSE CODE HERE
						print('message does not contain a picture', end=' ') 
						if 'from' in updateList[i]['message'] :
							if 'username' in updateList[i]['message']['from'] :
								print('(from ', updateList[i]['message']['from']['username'], ')', sep='')
							else :
								print('(from ', updateList[i]['message']['from']['first_name'], ' (', updateList[i]['message']['from']['id'], '))', sep='')
						else :
							print('')
				else :
					print('update not from admin', end=' ')
					if    'new_chat_member' in updateList[i]['message'] :
						if  updateList[i]['message']['new_chat_member']['id'] == botID :
							forwardList.append(updateList[i]['message']['chat']['id'])
							print('added ', updateList[i]['message']['chat']['title'], ' (', updateList[i]['message']['chat']['id'], ') to forwardList by ', str(updateList[i]['message']['from']['username']), ' (', updateList[i]['message']['from']['id'], ')', sep='')
							report = report + '`added `' + str(updateList[i]['message']['chat']['title']) + '` to forwardList by `' + str(updateList[i]['message']['from']['username']) + '\n'
							sendReport = True
					elif 'left_chat_member' in updateList[i]['message'] :
						if updateList[i]['message']['left_chat_member']['id'] == botID :
							if updateList[i]['message']['chat']['id'] in forwardList :
								forwardList.remove(updateList[i]['message']['chat']['id'])
								print('\nremoved', updateList[i]['message']['chat']['title'], 'from forwardList')
								report = report + '`removed `' + str(updateList[i]['message']['chat']['title']) + ' `from forwardList`\n'
								sendReport = True
					else :			
						if 'from' in updateList[i]['message'] :
							if 'username' in updateList[i]['message']['from'] :
								print('(from ', updateList[i]['message']['from']['username'], ')', sep='')
							else :
								print('(from ', updateList[i]['message']['from']['first_name'], ' (', updateList[i]['message']['from']['id'], '))', sep='')
						else :
							print('')
						print('   ', updateList[i]['message'])
			else :
				print('update not does not contain message')
				print(updateList[i])
		if len(updateList) > 0 :
			mostrecentupdate = updateList[len(updateList) - 1]['update_id']
			print('clearing updateList through to update_id', mostrecentupdate + 1)
			request = 'https://api.telegram.org/bot' + token + '/getUpdates'
			response = requests.get(request, {'offset': mostrecentupdate + 1})
			response = response.json()
			if response['ok'] :
				updateList = response['result']
				print(' updates:', len(updateList))
				if len(updateList) <= 0 :
					print('...success')
				else :
					print('updateList not empty, repeating...')
			else :
				print('failed')
				sendReport = True
	else :
		print('updateList empty')

	print()



def report_forwards() :
	print('report_forwards()')
	global token
	global forwardList
	global report
	global admins
	report = ''
	
	print('reading forwardList.json')
	dbxforward = dbx.files_download('/forwardList.json')
	forwardList = dbxforward[1].json()
	print(len(forwardList), 'forwards')
	print()
	
	request = 'https://api.telegram.org/bot' + token + '/getChat'
	
	for i in range(len(forwardList)):
		response = requests.get(request, {'chat_id': forwardList[i]})
		response = response.json()
		if response['ok'] :
			print('forward[', str(i),']: (', str(response['result']['id']), ') ', response['result']['title'], sep='')
			report = report + '`forward[' + str(i) + ']: `' + response['result']['title'] + '\n'
		else :
			print('forward[', str(i),']: (', str(forwardList[i]), ') ', response['description'], sep='')
	
	#print('uploading forwardList.json to Dropbox')
	#dbx.files_upload(json.dumps(forwardList).encode('utf-8'), '/forwardList.json',   dropbox.files.WriteMode('overwrite', None))
	
	#request = 'https://api.telegram.org/bot' + token + '/sendMessage'
	#for i in range(len(admins)):
	#	requests.get(request, {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})
	
	#print(report)
	print()



def update_dropbox() :
	print('update_dropbox()')
	#reinitialize all the lists and variables as global
	global fileIDs
	global usedIDs
	global forwardList
	global delay

	print('uploading fileIDs.json to Dropbox')
	dbx.files_upload(json.dumps(fileIDs    ).encode('utf-8'), '/fileIDs.json',       dropbox.files.WriteMode('overwrite', None))
	print('uploading usedIDs.json to Dropbox')
	dbx.files_upload(json.dumps(usedIDs    ).encode('utf-8'), '/usedIDs.json',       dropbox.files.WriteMode('overwrite', None))
	print('uploading delay.json to Dropbox')
	dbx.files_upload(json.dumps(delay      ).encode('utf-8'), '/delay.json',         dropbox.files.WriteMode('overwrite', None))
	print('uploading forwardList.json to Dropbox')
	dbx.files_upload(json.dumps(forwardList).encode('utf-8'), '/forwardList.json',   dropbox.files.WriteMode('overwrite', None))
	print()



def post_photo():
	print('post_photo()')
	#reinitialize all the lists and variables as global
	global token
	global channel
	global fileIDs
	global usedIDs
	global forwardList
	global report
	global sendReport	
	removeList = []
	
	print('sending photo to chat_id:', channel, '...', sep='')
	if len(fileIDs) > 0 :
		phototosend = fileIDs.pop(0)
		request = 'https://api.telegram.org/bot' + token + '/sendPhoto'
		sentPhoto = requests.get(request, {'chat_id': channel, 'photo': phototosend})
		if sentPhoto.json()['ok'] :
			sentPhoto = sentPhoto.json()
			if len(fileIDs) < 10 :
				report = report + '`photo sent successfully.`\n` channel post: `' + str(sentPhoto['result']['message_id'])
			else :
				report = report + '`photo sent successfully.`\n` channel post: `' + str(sentPhoto['result']['message_id'])
			usedIDs.append(phototosend)
			print('success.')
			
			#FORWARDING PHOTO
			print('forwarding photo to', len(forwardList), 'chats')
			successfulForwards = 0
			request = 'https://api.telegram.org/bot' + token + '/forwardMessage'
			for i in range(len(forwardList)) :
				response = requests.get(request, data = {'chat_id': forwardList[i], 'from_chat_id': channel, 'message_id': sentPhoto['result']['message_id']})
				if response.json()['ok'] :
					successfulForwards = successfulForwards + 1
					print('forward[' + str(i) + '] ok')
				else :
					getchat = requests.get('https://api.telegram.org/bot' + token + '/getChat', {'chat_id': forwardList[i]})
					getchat = getchat.json()
					if getchat['ok'] :
						print('forward[' + str(i) + '] failed (chat_id: ' + str(forwardList[i]) + ') ' + getchat['result']['title'])
						report = report + '\n`forward[`' + str(i) + '`] failed (chat_id: `' + str(forwardList[i]) + '`) ` ' + getchat['result']['title']
					else :
						if 'description' in getchat :
							print('forward[' + str(i) + '] failed (chat_id: ' + str(forwardList[i]) + ') ' + getchat['description'])
							report = report + '\n`forward[`' + str(i) + '`] failed (chat_id: `' + str(forwardList[i]) + '`) `' + getchat['description']
							if 'Forbidden' in getchat['description'] :
								removeList.append(forwardList[i])
								report = report + '\n` removed `' + str(forwardList[i]) + '` from forward list`'
						else :
							print('forward[' + str(i) + '] failed (chat_id: ' + str(forwardList[i]) + ')')
							report = report + '\n`forward[`' + str(i) + '`] failed (chat_id: `' + str(forwardList[i]) + '`)`'
					print('raw response:', response.json())
					print('raw command:', response.url)
					sendReport = True
			report = report + '\n` forwarded to: `' + str(successfulForwards) + '` chats`'
		else :
			print('sentPhoto not ok, skipping forwards')
			fileIDs.append(phototosend)
			report = report + '`post failed.`\n`photo re-added to queue.`'
			print('failed.')
			sendReport = True
	else :
		report = report + '`post failed.`\n`no photos in queue.`\nADD PHOTOS IMMEDIATELY'
		sendReport = True
	if len(removeList) > 0 :
		for i in range(len(removeList)) :
			forwardList.remove(removeList[i])



def schedule_nextupdate():
	print('schedule_nextupdate()')
	#reinitialize all the lists and variables as global
	global fileIDs
	global delay
	global timezone
	global report
	global scheduler
	global sendReport
	
	nextupdate = currenttime = (time.time() + ((60*60) * timezone))
	nextupdate = (nextupdate - (nextupdate % (delay * 60))) + (delay * 60)
	
	noowtime = ''
	if time.localtime(currenttime).tm_hour < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_hour) + ':'
	if time.localtime(currenttime).tm_min  < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_min)

	nexttime = ''
	if time.localtime(nextupdate).tm_hour < 10 : nexttime = nexttime + '0'
	nexttime = nexttime + str(time.localtime(nextupdate).tm_hour) + ':'
	if time.localtime(nextupdate).tm_min  < 10 : nexttime = nexttime + '0'
	nexttime = nexttime + str(time.localtime(nextupdate).tm_min)

	report = report + '\n`current delay: `' + str(delay) + '` minutes\ncurrent queue: `' + str(len(fileIDs)) + '`\n current time: `' + noowtime + '`\n  next update: `' + nexttime
	if len(fileIDs) < 10 :
		report = report + '\nLOW ON PHOTOS'
		sendReport = True
	#report = report + '\n`next photo in queue: `'
	
	print('current time:', noowtime)
	print(' next update:', nexttime)
	print()
	print('scheduling update for', (delay), 'minutes from now')
	#scheduler.enter((delay * 60), 1, scheduled_post, ())
	scheduler.enterabs((nextupdate - ((60*60) * timezone)), 1, scheduled_post, ())



def schedule_firstupdate():
	print('schedule_firstupdate()')
	#reinitialize all the lists and variables as global
	global fileIDs
	global delay
	global timezone
	global forwardList
	global report
	global scheduler
	
	nextupdate = currenttime = (time.time() + ((60*60) * timezone))
	nextupdate = (nextupdate - (nextupdate % (delay * 60))) + (delay * 60)
	
	noowtime = ''
	if time.localtime(currenttime).tm_hour < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_hour) + ':'
	if time.localtime(currenttime).tm_min  < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_min)

	nexttime = ''
	if time.localtime(nextupdate).tm_hour < 10 : nexttime = nexttime + '0'
	nexttime = nexttime + str(time.localtime(nextupdate).tm_hour) + ':'
	if time.localtime(nextupdate).tm_min  < 10 : nexttime = nexttime + '0'
	nexttime = nexttime + str(time.localtime(nextupdate).tm_min)
	
	report = report + '`  bot started`\n`current delay: `' + str(delay) + '` minutes`\n`current queue: `' + str(len(fileIDs)) + '\n`     forwards: `' + str(len(forwardList)) + '\n` current time: `' + noowtime + '\n`  next update: `' + nexttime
	#report = report + '\n`next photo in queue: `'
		
	print('current time:', noowtime)
	print(' next update:', nexttime)
	print('bot started. scheduling first post...')
	print('scheduling update for', nexttime)
	scheduler.enterabs((nextupdate - ((60*60) * timezone)), 1, scheduled_post, ())



def send_report():
	print('send_report()')
	#reinitialize all the lists and variables as global
	global token
	global admins
	global fileIDs
	global report
	
	if len(fileIDs) > 0 :
		request1 = 'https://api.telegram.org/bot' + token + '/sendMessage'
		request2 = 'https://api.telegram.org/bot' + token + '/sendPhoto'
		for i in range(len(admins)):
			requests.get(request1, {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})
			#requests.get(request2, {'chat_id': admins[i], 'photo': fileIDs[0]})
	else :
		request = 'https://api.telegram.org/bot' + token + '/sendMessage'
		for i in range(len(admins)):
			requests.get(request, {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})
			requests.get(request, {'chat_id': admins[i], 'text': 'NO PHOTOS IN QUEUE', 'parse_mode': 'Markdown'})
	
	print('report sent')



def initial_startup():
	print('initial_startup()')
	#reinitialize all the lists and variables as global
	global scheduler
	
	#report_forwards()
	update()
	update_dropbox()
	schedule_firstupdate()
	send_report()
	
	scheduler.run()



def scheduled_post():
	print('scheduled_post()')
	#reinitialize all the lists and variables as global
	global scheduler
	global sendReport	
	
	update()
	post_photo()
	update_dropbox()
	schedule_nextupdate()
	if sendReport :
		send_report()
	sendReport = False
	scheduler.run()



initial_startup()
