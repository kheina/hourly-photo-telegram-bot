# Telegram Photo Channel Controller Bot
## About
This bot was designed and built to control the telegram channel Flickr Sneps https://t.me/flickrsneps

It works by taking the file IDs of photos sent to it by an admin, and keeping them in a queue.
By default, the delay is set to 60 minutes. Meaning, at the top of every hour, a file ID is popped
from the queue and sent to the telegram channel specified and forwarded to all the groups the bot
has been added to.

## Usage
Start by cloning the repo into your desired folder.

Take the admins.json, delay.json, fileIDs.json, forwardList.json, timeZone.json, and usedIDs.json
and move them into the app folder made by dropbox (create one of these on dropbox.com). Once you
have done this, edit the first few lines of bot.py and change dbx, token, channel, and botID to
your own information.

The bot uses telegram's getUpdates method, so you can safely send it images and add it to groups while
it isn't running and it will add them all to the proper files once it is launched.

You may also run the http call https://api.telegram.org/bot[botToken]/getUpdates in your browser to
determine what your bot id and channel id are.

I'd also recommend looking through https://core.telegram.org/bots/api this resource for more information
on telegram bots and how they work.

Once you start the bot, admins should get a message on telegram from the bot with some information
including the current delay and number of photos in the queue.

## etc

If you have any questions about how the bot works or are having trouble setting it up, feel free to
send me an email and I'd be happy to help.