import requests
import json
import sched, time
import dropbox

dbx = dropbox.Dropbox('iPVSiTTotuYAAAAAAAEgnRwVETJXdTYNZ_b5QdezBhSF9QN97HhzU6EqObRElMaM')
#iPVSiTTotuYAAAAAAAEgnRwVETJXdTYNZ_b5QdezBhSF9QN97HhzU6EqObRElMaM #dropbox access token

#print(dbx.users_get_current_account())
#dbx.files_upload("Potential headline: Game 5 a nail-biter as Warriors inch out Cavs", '/cavs vs warriors/game 5/story.txt')
#dbx.files_download(path, rev=None)
#files_download_to_file(download_path, path, rev=None)

scheduler = sched.scheduler(time.time, time.sleep)
admins = [118819437]
fileIDs = []
usedIDs = []
delay = 180

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
print('reading admins.json')
dbxadmins = dbx.files_download('/admins.json')
admins = dbxadmins[1].json()
print(len(admins), 'admins')
#print(dbxadmins[0])
#print(admins)
print('reading delay.json')
dbxdelay = dbx.files_download('/delay.json')
delay = dbxdelay[1].json()
print(delay, 'minute delay')
#print(dbxdelay[0])

print()
#fileIDs.pop(0)

nextupdate = currenttime = (time.time() - 14400)
nextupdate = (nextupdate - (nextupdate % (delay * 60))) + (delay * 60)
#print(time.localtime(currenttime).tm_hour % 3)
#if time.localtime(currenttime).tm_hour % 3 == 2 : 
#	nextupdate = nextupdate - 7200
#else : nextupdate = nextupdate + 3600

noowtime = 'current time: '
if time.localtime(currenttime).tm_hour < 10 : noowtime = noowtime + '0'
noowtime = noowtime + str(time.localtime(currenttime).tm_hour) + ':'
if time.localtime(currenttime).tm_min  < 10 : noowtime = noowtime + '0'
noowtime = noowtime + str(time.localtime(currenttime).tm_min)

nexttime = ' next update: '
if time.localtime(nextupdate).tm_hour < 10 : nexttime = nexttime + '0'
nexttime = nexttime + str(time.localtime(nextupdate).tm_hour) + ':'
if time.localtime(nextupdate).tm_min  < 10 : nexttime = nexttime + '0'
nexttime = nexttime + str(time.localtime(nextupdate).tm_min)

print(noowtime)
print(nexttime)
response = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/getUpdates')
#print(response.url)
response = response.json()
print()
if response['ok'] :
	print('response:', 'ok')
	updateList = response['result']
else :
	print('response not ok')
	#CRASH

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
			print()
			print('response:', 'ok')
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
dbx.files_upload(json.dumps(fileIDs).encode('utf-8'), '/fileIDs.json', dropbox.files.WriteMode('overwrite', None))
print('uploading usedIDs.json to Dropbox')
dbx.files_upload(json.dumps(usedIDs).encode('utf-8'), '/usedIDs.json', dropbox.files.WriteMode('overwrite', None))
print('uploading admins.json to Dropbox')
dbx.files_upload(json.dumps(admins ).encode('utf-8'), '/admins.json',  dropbox.files.WriteMode('overwrite', None))
print('uploading delay.json to Dropbox')
dbx.files_upload(json.dumps(delay  ).encode('utf-8'), '/delay.json',   dropbox.files.WriteMode('overwrite', None))
print()

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
for i in range(len(admins)):
	requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})
	if len(fileIDs) > 0 :
		requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendPhoto', {'chat_id': admins[i], 'photo': fileIDs[0]})
	else :
		requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': 'NO PHOTOS IN QUEUE', 'parse_mode': 'Markdown'})

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

def update_event():
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
	print('reading admins.json')
	dbxadmins = dbx.files_download('/admins.json')
	admins = dbxadmins[1].json()
	print(len(admins), 'admins')
	#print(dbxadmins[0])
	#print(admins)
	print('reading delay.json')
	dbxdelay = dbx.files_download('/delay.json')
	delay = dbxdelay[1].json()
	print(delay, 'minute delay')
	#print(dbxdelay[0])

	print()

	response = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/getUpdates')
	print(response.url)
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
	print('sending photo to Flickr Sneps (id:-1001084745741)...')
	if len(fileIDs) > 0 :
		phototosend = fileIDs.pop(0)
		sentPhoto = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendPhoto', {'chat_id': -1001084745741, 'photo': phototosend})
		sentPhoto = sentPhoto.json()
		if sentPhoto['ok'] :
			if len(fileIDs) < 10 :
				report = '`photo sent successfully.`\n` channel post: `' + str(sentPhoto['result']['message_id'] - 42)
			else :
				report = '`photo sent successfully.`\n` channel post: `' + str(sentPhoto['result']['message_id'] - 42)
			usedIDs.append(phototosend)
			print('success.')
		else :
			fileIDs.append(phototosend)
			report = '`post failed.`\n`photo re-added to queue.`'
			print('failed.')
	else :
		report = '`post failed.`\n`no photos in queue.`\nADD PHOTOS IMMEDIATELY'

	#for i in range(len(admins)):
	#	requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})

	#118819437 my ID

	print()	
	print('uploading fileIDs.json to Dropbox')
	dbx.files_upload(json.dumps(fileIDs).encode('utf-8'), '/fileIDs.json', dropbox.files.WriteMode('overwrite', None))
	print('uploading usedIDs.json to Dropbox')
	dbx.files_upload(json.dumps(usedIDs).encode('utf-8'), '/usedIDs.json', dropbox.files.WriteMode('overwrite', None))
	print('uploading delay.json to Dropbox')
	dbx.files_upload(json.dumps(delay  ).encode('utf-8'), '/delay.json',   dropbox.files.WriteMode('overwrite', None))
	print()

	nextupdate = currenttime = (time.time() - 14400)
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

	
	#print('scheduling update for', nexttime)
	print('scheduling update for', (delay), 'minutes from now')
	scheduler.enter((delay * 60), 1, update_event, ())
	report = report + '\n`current delay: `' + str(delay) + '` minutes\ncurrent queue: `' + str(len(fileIDs)) + '`\n current time: `' + noowtime + '`\n  next update: `' + nexttime
	if len(fileIDs) < 10 : report = report + '\nLOW ON PHOTOS'
	report = report + '\n`next photo in queue: `'
	for i in range(len(admins)):
		requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})
		if len(fileIDs) > 0 :
			requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendPhoto', {'chat_id': admins[i], 'photo': fileIDs[0]})
		else :
			requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': 'NO PHOTOS IN QUEUE', 'parse_mode': 'Markdown'})



			
			
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
print('flickrsneps started. scheduling first post...')
print('scheduling update for', nexttime)
scheduler.enterabs((nextupdate + 14400), 1, update_event, ())

scheduler.run()


























