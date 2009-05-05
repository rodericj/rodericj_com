from rodericj_com.callme.models import CAction, CUser
from datetime import datetime
import util

class cron():
	def execute(self):
		q1 = CAction.objects.filter(date_to_be_executed__lte =datetime.now())
		q2 = q1.exclude(finished=True)
		for i in q2:
			print i
			self.send(i)

	def send(self, a):
		print "this is the caction essentially: "+str(a)
		print "1: sender phone number "+a.sender.phone_number
		print "2: phone number "+a.phone_number
		print "3: message "+a.message
		sendEmailTo = a.sender.phone_number.replace('-', '')+"@txt.att.net"
		util.sendMail(sendEmailTo, sendEmailTo, "reminder", a.message)
		
