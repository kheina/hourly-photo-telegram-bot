import sched, time

scheduler = sched.scheduler(time.time, time.sleep)
delay = 180
print(delay, 'minute delay')


nextupdate = currenttime = time.time()
for i in range(100):
	print()
	nextupdate = currenttime = time.time() + (3690 * i)
	nextupdate = (nextupdate - (nextupdate % (delay * 60))) + (delay * 60)
	#print(time.localtime(currenttime).tm_hour % 3)
	if time.localtime(currenttime).tm_hour % 3 == 2 : 
		nextupdate = nextupdate - 7200
	else : nextupdate = nextupdate + 3600
	
	noowtime = 'current test time: '
	if time.localtime(currenttime).tm_hour < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_hour) + ':'
	if time.localtime(currenttime).tm_min  < 10 : noowtime = noowtime + '0'
	noowtime = noowtime + str(time.localtime(currenttime).tm_min)

	nexttime = ' next test update: '
	if time.localtime(nextupdate).tm_hour < 10 : nexttime = nexttime + '0'
	nexttime = nexttime + str(time.localtime(nextupdate).tm_hour) + ':'
	if time.localtime(nextupdate).tm_min  < 10 : nexttime = nexttime + '0'
	nexttime = nexttime + str(time.localtime(nextupdate).tm_min)

	print(noowtime)
	print(nexttime)