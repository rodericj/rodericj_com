from datetime import datetime
from django.conf import settings

class util:
	pass

def sendMail(sender, receiver, subject, message):
	from email.MIMEText import MIMEText
	import smtplib,sys

	from django.core.mail import send_mail

	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [receiver])
	#msg = MIMEText(message)
	#msg['From'] = sender
	#msg['To'] = receiver
	#msg['Subject'] = subject
	#server = smtplib.SMTP("smtp.gmail.com", 587)
	#server.ehlo()
	#server.starttls()
	#server.ehlo()
	#server.login('hollrin', 'ThlE1I8X')
	#server.sendmail(sender, receiver, msg.as_string())
def populatecreatepage(user):
		hours = range(1,13)
		minutes = ["00", "15", "30", "45"]
		days = range(1,32)
		ampm = ['am', 'pm']
		months = ['january', 'february', 'march', 'april',
 			'may', 'june', 'july', 'august',
 			'september', 'october', 'november', 'december']
		this_year = datetime.now().year
		nowday = datetime.now().day-1
		nowmonth = months[datetime.now().month-1]
		years = range(this_year, this_year+5)	
		profile = user.get_profile()
		return {'hours':hours, 'minutes':minutes, 
					'ampm':ampm, 'days':days, 
					'months':months, 'years':years, 
					'user':user, 'profile':profile,
					'nowday':nowday, 'nowmonth':nowmonth}
