# Create your views here.
from datetime import datetime
import os
from random import random
from rodericj_com.callme.models import CAction, CUser
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.views import change_password
from django.contrib.auth.decorators import login_required
#from django.core.mail import send_mail
from django.contrib.auth.models import User

def start(request):
	print "view:start"
	if request.user.is_authenticated():
		print "User is logged in"
		ret = HttpResponseRedirect('/callme/create/')
	else:
		print "user in NOT logged in"
		ret =  HttpResponseRedirect('/accounts/login/')
	return ret
	
def Clogin(request):
	print "view:Clogin"
	rc={'val':0, 'response':"Success"}
	if request.user.is_authenticated():
		print "already logged in"
		# Redirect to a success page.
		args = populatecreatepage(request.user)
		return render_to_response('create.html', args)
	#Are we getting here from the login page?
	if request.POST.has_key('userName'):
		print "has userName entered"
		username = request.POST['userName']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				print "user is active"
				login(request, user)
				# Redirect to a success page.
				args = populatecreatepage(user)
				return render_to_response('create.html', args)
				
			else:
				rc={'val':1, 'response':"This account is not active"}
				# Return a 'disabled account' error message
		else:
			# Return an 'invalid login' error message.
			print "invalid login error"
			rc={'val':1, 'response':"invalid login error"}
	return render_to_response('registration/login.html', {'response':rc['response']})

def validate(request):
	print "views:validate"
	code = request.POST.get('code', '-1')
	if len(code) == 0:
		code = 0
	
	userlist = User.objects.filter(username=request.user.username)
	
	if len(userlist) != 1:
		args = populatecreatepage(request.user)
		args['response'] = "we have a problem: not 1 user with this username"
		return render_to_response('create.html', args)
	
	profile = userlist[0].get_profile()
	if profile.secret != int(code):
		args = populatecreatepage(request.user)
		args['response'] = "wrong code"
	else:
		profile.verified = True
		profile.save()
		
	args = populatecreatepage(request.user)
	return render_to_response('create.html', args)

def createaccount(request):
	print "view:createaccount"
	rc={'val':0, 'response':"Success"}
	username = request.POST.get('userName', '')
	password = request.POST.get('password', '')
	confirmpassword = request.POST.get('confirmpassword', '')
	email = request.POST.get('email', '')
	phone_number = request.POST.get('phone_number', '')
	first_name = request.POST.get('first_name', '')
	last_name = request.POST.get('last_name', '')

	#error checking
	if len(username) < 1:
		response = "Must enter a username"
		rc={'val':1, 'response':response}
	
	elif not validate_phone(phone_number):
		response = "Must enter a phone number"
		rc={'val':1, 'response':response}

	elif len(password) < 1:
		response = "Must enter a password"
		rc={'val':1, 'response':response}

	elif len(password) < 1:
		response = "Must enter a password"
		rc={'val':1, 'response':response}

	elif password != confirmpassword:
		response = "Passwords do not match"
		rc={'val':1, 'response':response}

	#finally hit DB to see if we can use this name
	elif len(User.objects.filter(username=username)) > 0:
		print User.objects.filter(username=username)
		response = "User name already exists"
		rc={'val':1, 'response':response}

	if rc['val']:
		return render_to_response('registration/login.html', {'response':response})
	else:
		#We are good to create a new user
		now = datetime.now()
		secret = int(random()*100000)
		user = User.objects.create_user(username, email, password)
		user.first_name = first_name
		user.last_name = last_name
		my_CUser = CUser(user=user, phone_number=phone_number, 
						clients=1, date_last_used=now, secret=secret, 
						verified=False)
		my_CUser.save()
		user = authenticate(username=username, password=password)
		login(request, user)

		receiver = str(phone_number) + "@txt.att.net"
		subject = "confirmation of account"
		message = "type in this number on the site: "+ str(secret)
		sender = "roderic@gmail.com"
		sendMail(sender, receiver, subject, message)
		args = populatecreatepage(user)
		
		return render_to_response('create.html', args)

#def sendSecret(user):
	#recipient = "5858020632@txt.att.net"
	#destination = "5858020632"
	#message = "You've set up a reminder to call"+destination
	#message = "type in the following on the callme app " + str(user.secret)
	#print "sending"
	#send_mail('Callme Reminder', message, [recipient], recipient, fail_silently=False)
	#print "sent"

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

@login_required
def change_password_view(request):
	print "view:change_password_view"
	change_password()
	args = populatecreatepage(request.user)
	return render_to_response('create.html', args)
@login_required
def logout_view(request):
	print "view:logout_view"
	logout(request)
	return HttpResponseRedirect('/accounts/login/')

def populatecreatepage(user):
	hours = range(1,13)
	minutes = ["00", "15", "30", "45"]
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
				'months':months, 'years':years, 'user':user, 'profile':profile}
	
@login_required
def create(request):
	print "view:create"
	args = populatecreatepage(request.user)
	user = request.user
	return render_to_response('create.html', args)
						
def validate_phone(phone_number):
	return len(phone_number) > 0

def validate_email(email):
	return len(email) > 0

def newaction(request):
	print "view:newaction"
	rc={'val':0, 'response':'success'}
	months_map = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
	
	#validate
	name = request.POST.get('name', '')
	if len(name) > 0:
		middle = name + " at "
	else:
		middle = ''
	
	hour = request.POST.get('hour', '')
	minute = request.POST.get('minute', '')
	day = request.POST.get('day', '')
	ampm = request.POST.get('ampm', '')
	year = request.POST.get('year', '')

	#adjustments
	#month
	month = request.POST['month']
	month = months_map[month]
		
	date = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
	now = datetime.now()
			
	email = request.POST.get('email', '')
	phone_number = request.POST.get('phone_number', '')

	if not validate_phone(phone_number):
		response = "invalid phone number"
		rc={'val':1, 'response':response}

	elif not validate_email(email):
		response = "invalid email"
		rc={'val':1, 'response':response}
		
	elif date < datetime.now():
		response = "date is before now"
		rc={'val':1, 'response':response}

	if rc['val'] == 1:
		args = populatecreatepage(request.user)
		rc.update(args)
		return render_to_response('create.html', rc)
		
	#Find the user if he exists
	list = CUser.objects.filter(phone_number=phone_number)
		

	#create the action
	print "creating the action"
	message = "You need to call "+ middle + phone_number + " now"
	request.user.get_profile().caction_set.create(phone_number=phone_number, message=message, date_created=now, date_to_be_executed=date, date_finished=0)
	#print user.action_set.all()
	print "done"

	args = populatecreatepage(request.user)
	return render_to_response('create.html', args)
