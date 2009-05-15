# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
from callme import callmeutil
from random import random
from callme.models import CUser, CAction
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from google.appengine.api import users

from ragendja.template import render_to_response

def start(request):
	logging.debug("start")
	user = request.user
	if user.is_authenticated():
		logging.debug("authenticated")
		if user.get_profile():
			logging.debug("there is a profile")
			ret =  render_to_response(request, 'create.html', callmeutil.populatecreatepage(request.user))
		else:
			logging.debug("there is no profile")
			ret = render_to_response(request, 'createprofile.html', {})
	else:
		logging.debug("not authenticated")
		ret =  HttpResponseRedirect('/account/register/')
	return ret

def sendConfirmation(user, phone_number):
	num = phone_number.replace('-', '')+"@txt.att.net"
	subject = "Validation"
	message = "Please type in " + str(user.secret) + " at the site"
	callmeutil.sendMail('hollrin@gmail.com', num, subject, message)
	
@login_required
def resend(request):
	logging.debug('resending the phone number')
	user = request.user.get_profile()
	sendConfirmation(user, user.phone_number)
	rc = callmeutil.populatecreatepage(request.user)
	rc['numbersent'] = True
	return render_to_response(request, 'createprofile.html', rc)

def extractPhoneNumber(thePost):
		p1 = thePost.get('phone_number1', '')
		p2 = thePost.get('phone_number2', '')
		p3 = thePost.get('phone_number3', '')
		return p1+"-"+p2+"-"+p3
	
@login_required
def createprofile(request):
	logging.debug('entering createprofile')
	templatepage = 'createprofile.html'
	rc = {}
	rc.update(callmeutil.populatecreatepage(request.user))
	post = request.POST

	if request.user.get_profile():
		logging.warn("We DO NOT want to create the new user")

	#if phone number entered then we set up the new CUser
	if post.has_key('phone_number1') and post.has_key('phone_number2') and post.has_key('phone_number3'):
		phone_number = extractPhoneNumber(post)
		now = datetime.now()
		secret = int(random()*100000)
		userProfile = CUser(phone_number=phone_number, date_last_used=now,
			verified=False, clients=1, secret=secret)
		
		#if there are test results then something is wrong, need to send that
		#otherwise profile looks good so far, we can send the sms
		if not userProfile.validate():
			rc['val'] = 1
			rc['response'] = "error in input"# userProfile.popitem()
			logging.error('error in validation of phone number')

		else:
			user = request.user
			userProfile = CUser(user=user, phone_number=phone_number, date_last_used=now,
			verified=False, clients=1, secret=secret)
			userProfile.save()
			#user.save()
			request.user = user
			sendConfirmation(userProfile, phone_number)
			rc['val'] = 0
			rc['numbersent'] = True
			rc['profile'] = userProfile

	elif post.has_key('code'):
		#see if it is the correct code
		code = post.get('code', '')
		if str(request.user.get_profile().secret) == str(code):
			user = request.user.get_profile()
			user.verified = True
			user.save()
			templatepage = 'create.html'
		else:
			rc['numbersent'] = True
		
	return render_to_response(request, templatepage, rc)
		
@login_required
def logout_view(request):
	print "view:logout_view"
	logout(request)
	ret =  HttpResponseRedirect('/account/register/')
	return ret

@login_required
def newaction(request):
	logging.debug("new request")
	templatepage = 'create.html'
	rc={'val':0, 'response':'success'}
	months_map = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
	
	#validate
	post = request.POST
	name = post.get('name', '')
	hour = post.get('hour', '')
	minute = post.get('minute', '')
	day = post.get('day', '')
	ampm = post.get('ampm', '')
	year = post.get('year', '')

	#adjustments
	#month
	month = post.get('month', 'january')
	month = months_map[month]
	if ampm == 'pm' and int(hour) != 12:
		hour = int(hour) +12 
			
	date = None
	try:
		date = datetime(year=int(year), month=int(month), 
						day=int(day), hour=int(hour), 
						minute=int(minute), second=0)
	except ValueError:
		response = "invalid date, please try another"
		rc = {'val':1, 'response':response}

	now = datetime.now()
			
	email = post.get('email', '')
	phone_number = extractPhoneNumber(post)
	#phone_number = post.get('phone_number', '')

	adjustedNow = datetime.now() 
	adjustedNow = adjustedNow + timedelta(hours=-7)
	logging.debug("now "+str(datetime.now()))
	logging.debug("now adjusted "+ str(adjustedNow))
	if not validate_phone(phone_number):
		response = "invalid phone number"
		rc={'val':1, 'response':response}

	#Do not really need email address here
	#elif not validate_email(email):
		#response = "invalid email"
		#rc={'val':1, 'response':response}
		
	elif date and date < adjustedNow:
		logging.debug("date: "+ str(date) + " " + str(adjustedNow))
		response = "date is before now"
		rc={'val':1, 'response':response}

	if rc['val'] != 0:
		rc.update(callmeutil.populatecreatepage(request.user))
		logging.debug("fail to create: "+rc['response'])
		return render_to_response(request, 'create.html', rc)
		
	#create the action
	message = "You need to call "+ phone_number 
	action = CAction()
	if users.get_current_user():
		action.sender = users.get_current_user()

	action.phone_number = phone_number
	action.message = 1#message
	action.date_to_be_executed = date
	action.date_created = now
	action.date_finished = now
	action.memo = 'this is the memo of the note'
	action.finished = False
	action.sender = request.user.get_profile()
	action.put()

	rc.update(callmeutil.populatecreatepage(request.user))
	return render_to_response(request, templatepage, rc)

@login_required
def create(request):
	logging.debug( "create")
	for action in dir(request.user):
		logging.debug( action)
	print request.user.get_profile()
	return HttpResponseRedirect('/account/register/')
	
def validate_phone(phone_number):
	return len(phone_number) == 12

def validate_email(email):
	return len(email) > 0

def cron(request):
		logging.debug("entering cron")
		q = CAction.all()
		q1 = q.filter('date_to_be_executed <', datetime.now())
		q2 = q1.filter('finished =', False)
		results = q2.fetch(1000)
		for i in results:
			#i.perform()
			message = i.memo+ " " + i.phone_number
			callmeutil.sendMail(i.sender.phone_number, i.sender.phone_number.replace('-','')+"@txt.att.net", 'Call Reminder', message)
			i.finished = True
			i.save()
		return HttpResponseRedirect('/')
