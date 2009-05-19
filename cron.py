from callme.models import CAction
from datetime import datetime, timedelta
import logging
from callme import callmeutil

q = CAction.all()
q1 = q.filter('date_to_be_executed <', datetime.now())
q2 = q1.filter('finished =', False)
results = q2.fetch(1000)
logging.debug("sentering cron "+str(len(results)))

for i in results:
	message = i.memo+ " " + i.phone_number
	callmeutil.sendMail(i.sender.phone_number, i.sender.phone_number.replace('-','')+"@txt.att.net", 'Call Reminder', message)
	i.finished = True
	i.date_finished = datetime.now()
	i.save()

