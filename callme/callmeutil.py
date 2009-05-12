from datetime import datetime
class util:
	pass

def sendMail(sender, receiver, subject, message):
	from email.MIMEText import MIMEText
	import smtplib,sys

	msg = MIMEText(message)
	msg['From'] = sender
	msg['To'] = receiver
	msg['Subject'] = subject
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('hollrin', 'ThlE1I8X')
	server.sendmail(sender, receiver, msg.as_string())
def populatecreatepage(user):
		hours = range(1,13)
		minutes = ["00", "15", "30", "45"]
		minutes = range(60)
		days = range(1,32)
		ampm = ['am', 'pm']
		months = ['january', 'february', 'march', 'april',
 			'may', 'june', 'july', 'august',
 			'september', 'october', 'november', 'december']
		this_year = datetime.now().year
		years = range(this_year, this_year+5)	
		profile = user.get_profile()
		return {'hours':hours, 'minutes':minutes, 
					'ampm':ampm, 'days':days, 
					'months':months, 'years':years, 
					'user':user, 'profile':profile}
