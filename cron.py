from callme.models import CAction, CUser
import logging
from datetime import datetime
import util

class cron():
	def execute(self):
		q1 = CAction.objects.filter(date_to_be_executed__lte =datetime.now())
		q2 = q1.exclude(finished=True)
		for i in q2:
			logging.debug(i)
			self.send(i)

	def send(self, a):
		logging.debug( "this is the caction essentially: "+str(a))
		logging.debug("1: sender phone number "+a.sender.phone_number)
		logging.debug("2: phone number "+a.phone_number)
		logging.debug("3: message "+a.message)
		sendEmailTo = a.sender.phone_number.replace('-', '')+"@txt.att.net"
		util.sendMail(sendEmailTo, sendEmailTo, "reminder", a.message)
		
