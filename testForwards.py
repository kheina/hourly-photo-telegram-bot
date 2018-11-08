import requests
import json
import dropbox

# credentials = {
# 	'dropboxAccessToken' : 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
# 	'telegramAccessToken' : 'yyyyyyyyy:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
# 	'telegramChannel' : -yyyyyyyyyyyyy,
# 	'telegramBotID' : yyyyyyyyy,
# 	'twitter' : {
# 		'consumerKey' : 'xxxxxxxxxxxxxxxxxxxxxxxxx',
# 		'consumerSecret' : 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
# 		'accessTokenKey' : 'yyyyyyyyyyyyyyyyyyy-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
# 		'accessTokenSecret' : 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# 	}
# }
# credentials are now saved in credentials.json in the format above

# initialize the dropbox folder
dbx = ''
# enter your dropbox access token in the ('') above

# telegram bot auth token (given by @BotFather upon your bot's creation)
token = ''
# enter your telegram bot's auth token in the '' above

# the chat_id of the channel where all the pictures will be posted
channel = 0
# enter your telegram channel's chat_id after the = above

# the id of the bot itself
botID = 0
# enter your telegram bot's id after the = above

# initialize twitter
api = ''

print('loading credentials.', end='')
with open('credentials.json') as userinfo :
	credentials = json.load(userinfo)
	dbx = dropbox.Dropbox(credentials['dropboxAccessToken'])
	token = credentials['telegramAccessToken']
	channel = credentials['telegramChannel']
	botID = credentials['telegramBotID']
print('..success.')

print('downloading forwardList.json')
dbxforward = dbx.files_download('/forwardList.json')
forwardList = dbxforward[1].json()
print(len(forwardList), 'forwards')

request = 'https://api.telegram.org/bot' + token + '/getChat'

print()
for i in range(len(forwardList)):
	response = requests.get(request, {'chat_id': forwardList[i]})
	response = response.json()
	if response['ok'] :
		print('forward[', str(i+1),']: (', str(response['result']['id']), ') ', response['result']['title'], sep='')
	else :
		print('forward[', str(i+1),']: (', str(forwardList[i]), ') ', response['description'], sep='')
print('done.')
print()
