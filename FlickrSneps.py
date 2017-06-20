import requests
import json
import sched, time
import dropbox

#initialize the dropbox folder
dbx = dropbox.Dropbox('iPVSiTTotuYAAAAAAAEgnRwVETJXdTYNZ_b5QdezBhSF9QN97HhzU6EqObRElMaM')
#iPVSiTTotuYAAAAAAAEgnRwVETJXdTYNZ_b5QdezBhSF9QN97HhzU6EqObRElMaM #dropbox access token

#initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

#initialize all the lists and variables
admins = [118819437]
fileIDs = []
usedIDs = []
forwardList = []
delay = 180
timezone = -5
report = 'temp'





def update():
	#reinitialize all the lists and variables as global
	global admins
	global fileIDs
	global usedIDs
	global forwardList
	global delay
	global timezone
	global report
	global scheduler
	
	#print('update()')
	print('reading admins.json')
	dbxadmins = dbx.files_download('/admins.json')
	admins = dbxadmins[1].json()
	print(len(admins), 'admins')
	#print(dbxadmins[0])
	#print(admins)
	print('reading fileIDs.json')
	dbxfileIDs = dbx.files_download('/fileIDs.json')
	fileIDs = dbxfileIDs[1].json()
	print(len(fileIDs), 'file ids')
	#print(dbxfileIDs[0])
	#print(fileIDs)
	print('reading usedIDs.json')
	dbxusedIDs = dbx.files_download('/usedIDs.json')
	usedIDs = dbxusedIDs[1].json()
	print(len(usedIDs), 'used ids')
	#print(dbxusedIDs[0])
	#print(usedIDs)
	print('reading forwardList.json')
	dbxdelay = dbx.files_download('/forwardList.json')
	forwardList = dbxdelay[1].json()
	print(len(forwardList), 'forwards')
	#print(forwardList)
	print('reading delay.json')
	dbxdelay = dbx.files_download('/delay.json')
	delay = dbxdelay[1].json()
	print(delay, 'minute delay')
	#print(dbxdelay[0])
	print('reading timezone.json')
	dbxtime = dbx.files_download('/timezone.json')
	timezone = dbxtime[1].json()
	print('UTC', timezone)
	#print(dbxtime[0])

	print()
	print("getUpdates")
	response = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/getUpdates')
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
						if  updateList[i]['message']['new_chat_member']['id'] == 394580059 : #THIS IS THE BOT'S ID
							forwardList.append(updateList[i]['message']['chat']['id'])
							print('\nadded', updateList[i]['message']['chat']['title'], 'to forwardList')
					elif 'left_chat_member' in updateList[i]['message'] :
						if updateList[i]['message']['left_chat_member']['id'] == 394580059 :
							if updateList[i]['message']['chat']['id'] in forwardList :
								forwardList.remove(updateList[i]['message']['chat']['id'])
								print('\nremoved', updateList[i]['message']['chat']['title'], 'from forwardList')
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
			response = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/getUpdates', {'offset': mostrecentupdate + 1})
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
	else :
		print('updateList empty')

	print()
	
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
	print('running post_photo()')
	#reinitialize all the lists and variables as global
	global fileIDs
	global usedIDs
	global forwardList
	global report
	global scheduler
	
	print('sending photo to Flickr Sneps (id:-1001084745741)...')
	if len(fileIDs) > 0 :
		phototosend = fileIDs.pop(0)
		sentPhoto = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendPhoto', {'chat_id': -1001084745741, 'photo': phototosend})
		sentPhoto = sentPhoto.json()
		if sentPhoto['ok'] :
			if len(fileIDs) < 10 :
				report = '`photo sent successfully.`\n` channel post: `' + str(sentPhoto['result']['message_id'])
			else :
				report = '`photo sent successfully.`\n` channel post: `' + str(sentPhoto['result']['message_id'])
			usedIDs.append(phototosend)
			print('success.')
			
			#FORWARDING PHOTO
			print('forwarding photo to', len(forwardList), 'chats')
			for i in range(len(forwardList)):
				requests.post('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/forwardMessage', {'chat_id': forwardList[i], 'from_chat_id': -1001084745741, 'message_id': sentPhoto['result']['message_id']})
			report = report + '\n` forwarded to: `' + str(len(forwardList)) + '` chats`'
			
		else :
			fileIDs.append(phototosend)
			report = '`post failed.`\n`photo re-added to queue.`'
			print('failed.')
	else :
		report = '`post failed.`\n`no photos in queue.`\nADD PHOTOS IMMEDIATELY'





def schedule_nextupdate():
	print('schedule_nextupdate()')
	#reinitialize all the lists and variables as global
	global admins
	global fileIDs
	global usedIDs
	global forwardList
	global delay
	global timezone
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

	print('current time:', noowtime)
	print(' next update:', nexttime)
	print()
	print('scheduling update for', (delay), 'minutes from now')
	scheduler.enter((delay * 60), 1, scheduled_post, ())
	report = report + '\n`current delay: `' + str(delay) + '` minutes\ncurrent queue: `' + str(len(fileIDs)) + '`\n current time: `' + noowtime + '`\n  next update: `' + nexttime
	if len(fileIDs) < 10 : report = report + '\nLOW ON PHOTOS'
	report = report + '\n`next photo in queue: `'





def schedule_firstupdate():
	print('schedule_firstupdate()')
	#reinitialize all the lists and variables as global
	global admins
	global fileIDs
	global usedIDs
	global forwardList
	global delay
	global timezone
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
	
	report = '`flickrsneps started\ncurrent delay: `' + str(delay) + '` minutes\ncurrent queue: `' + str(len(fileIDs)) + '`\n current time: `' + noowtime + '`\n  next update: `' + nexttime
	report = report + '\n`next photo in queue: `'
		
	print('current time:', noowtime)
	print(' next update:', nexttime)
	print('flickrsneps started. scheduling first post...')
	print('scheduling update for', nexttime)
	scheduler.enterabs((nextupdate - ((60*60) * timezone)), 1, scheduled_post, ())





def send_report():
	print('send_report()')
	#reinitialize all the lists and variables as global
	global admins
	global fileIDs
	global usedIDs
	global forwardList
	global delay
	global timezone
	global report
	global scheduler
	
	for i in range(len(admins)):
		requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})
		if len(fileIDs) > 0 :
			requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendPhoto', {'chat_id': admins[i], 'photo': fileIDs[0]})
		else :
			requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': 'NO PHOTOS IN QUEUE', 'parse_mode': 'Markdown'})
	
	print('report sent')





def initial_startup():
	print('initial_startup()')
	#reinitialize all the lists and variables as global
	global admins
	global fileIDs
	global usedIDs
	global forwardList
	global delay
	global timezone
	global report
	global scheduler
	
	update()
	schedule_firstupdate()
	send_report()
	
	scheduler.run()





def scheduled_post():
	print('scheduled_post()')
	#reinitialize all the lists and variables as global
	global admins
	global fileIDs
	global usedIDs
	global forwardList
	global delay
	global timezone
	global report
	global scheduler
	
	update()
	post_photo()
	schedule_nextupdate()
	send_report()
	
	scheduler.run()





initial_startup()






















