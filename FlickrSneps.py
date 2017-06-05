import requests
import json
import sched, time


scheduler = sched.scheduler(time.time, time.sleep)
admins = [118819437]
fileIDs = []
usedIDs = []
delay = 180
print('reading delay.json')
with open('delay.json') as infile :
	delay = json.load(infile)
print(delay, 'minute delay')




def update_event(butts):
	print('reading fileIDs.json')
	with open('fileIDs.json') as infile :
		fileIDs = json.load(infile)
	print(len(fileIDs), 'file ids')
	#print(fileIDs)

	print('reading usedIDs.json')
	with open('usedIDs.json') as infile :
		usedIDs = json.load(infile)
	print(len(usedIDs), 'used ids')
	print(usedIDs)

	print('reading admins.json')
	with open('admins.json') as infile :
		admins = json.load(infile)
	print(len(admins), 'admins')
	print(admins)
	
	print('reading delay.json')
	with open('delay.json') as infile :
		delay = json.load(infile)
	print(delay, 'minute delay')


	print()

	#while 

	response = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/getUpdates')
	print(response.url)
	response = response.json()
	if response['ok'] :
		print('response:', 'ok')
		updateList = response['result']
	else :
		print('response not ok')
		#BREAK

	print('updates:', len(updateList))


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
			if response['ok'] :
				r = requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/getUpdates', {'offset': mostrecentupdate + 1})
				updateList = r.json()['result']
				print('updates:', len(updateList))
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
				report = '`photo sent successfully.`\n`channel post: ' + str(sentPhoto['result']['message_id']) + '`\n`photos remaining in queue:` ' + str(len(fileIDs)) + '\nLOW ON PHOTOS, UPDATE QUEUE IMMEDIATELY'
			else :
				report = '`photo sent successfully.`\n`channel post: ' + str(sentPhoto['result']['message_id']) + '`\n`photos remaining in queue:` ' + str(len(fileIDs))
			usedIDs.append(phototosend)
			print('success.')
		else :
			fileIDs.append(phototosend)
			report = '`post failed.`\n`photo re-added to queue.`\n`photos remaining in queue:` ' + str(len(fileIDs))
			print('failed.')
	else :
		report = '`post failed.`\n`no photos in queue.`\nADD PHOTOS IMMEDIATELY'

	for i in range(len(admins)):
		requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})

	#118819437 my ID

	print()
	print('file ids:', len(fileIDs))
	print(fileIDs)
	print('writing to fileIDs.json')
	with open('fileIDs.json', 'w') as outfile :
		json.dump(fileIDs, outfile)

	print('used ids:', len(usedIDs))
	print(usedIDs)
	print('writing to usedIDs.json')
	with open('usedIDs.json', 'w') as outfile :
		json.dump(usedIDs, outfile)
		
	print('   delay:', delay)
	print(delay)
	print('writing to delay.json')
	with open('delay.json', 'w') as outfile :
		json.dump(delay, outfile)
	
	print('scheduling update for', delay * 60, 'seconds from now')
	scheduler.enter(delay * 60, 1, update_event, ('q'))
	report = '`update successful, next update in `' + str(delay) + '` minutes`'
	for i in range(len(admins)):
		requests.get('https://api.telegram.org/bot394580059:AAEw7Mo_xDNiyp_O6Zyw9gU_P4DMM8dyz6c/sendMessage', {'chat_id': admins[i], 'text': report, 'parse_mode': 'Markdown'})




print('scheduling update for 10 seconds from now')
scheduler.enter(10, 1, update_event, ('q'))

scheduler.run()


























