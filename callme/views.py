# -*- coding: utf-8 -*-
import logging
from datetime import datetime
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
		if user in dir(user):
			ret = HttpResponseRedirect('/callme/create/')
		else:
			return render_to_response(request, 'createprofile.html', {'number':123})#args)
			#ret = HttpresponseRedirect('callme/createaccount/')
	else:
		logging.debug("not authenticated")
		ret =  HttpResponseRedirect('/account/register/')
	return ret

def sendConfirmation(user, phone_number):
	num = phone_number.replace('-', '')+"@txt.att.net"
	subject = "Validation"
	message = "Please type in " + str(user.secret) + " at the site"
	callmeutil.sendMail('hollrin@gmail.com', num, subject, message)
	
def resend(request):
	logging.debug('resending the phone number')
	user = request.user.get_profile()
	sendConfirmation(user, user.phone_number)
	args = callmeutil.populatecreatepage(request.user)
	args['numbersent'] = True
	return render_to_response(request, 'createprofile.html', args)

def createprofile(request):
	logging.debug('entering createprofile')
	templatepage = 'createprofile.html'
	args = {}
	post = request.POST

	#if phone number entered
	if post.has_key('phone_number1') and post.has_key('phone_number2') and post.has_key('phone_number3'):
		#create profile and send the code
		p1 = request.POST.get('phone_number1', '')
		p2 = request.POST.get('phone_number2', '')
		p3 = request.POST.get('phone_number3', '')
		phone_number = p1+"-"+p2+"-"+p3
		logging.debug('phone number posted')
		logging.debug(phone_number)

		now = datetime.now()
		secret = int(random()*100000)
		userProfile = CUser(phone_number=phone_number, date_last_used=now,
			verified=False, clients=1, secret=secret)
		
		#if there are test results then something is wrong, need to send that
		#otherwise profile looks good so far, we can send the sms
		logging.debug("testing user")
		if not userProfile.validate():
			args['val'] = 1
			args['response'] = "error in input"# userProfile.popitem()
			logging.error('error in validation of phone number')

		else:
			logging.debug("saving user")
			user = request.user
			userProfile = CUser(user=user, phone_number=phone_number, date_last_used=now,
			verified=False, clients=1, secret=secret)
			userProfile.save()
			#request.user.user = userProfile
			request.user.save()
			sendConfirmation(userProfile, phone_number)
			args['val'] = 0
			args['numbersent'] = True
			logging.debug('looks good, sent email')
			if not request.user.get_profile():
				logging.error("Not get_profile()")
				request.user.get_profile()
				

	elif post.has_key('code'):
		#see if it is the correct code
		code = request.POST.get('code', '')
		logging.debug("has key: Comparing " + code + " and  " + str(request.user.get_profile().secret))
		if str(request.user.get_profile().secret) == str(code):
			logging.debug("codes match")
			request.user.get_profile().verified = True
			templatepage = 'create.html'
		else:
			logging.debug("codes do not match")
			args['numbersent'] = True
	args.update(callmeutil.populatecreatepage(request.user))
		
	logging.debug('ending and going to ' + templatepage)
	#for i in args:
		#logging.debug(i+": " +str(args[i]))
	#return render_to_response(args, 'createprofile.html' )
	return render_to_response(request, templatepage, args)
		
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
	args = {}
	rc={'val':0, 'response':'success'}
	months_map = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
	
	#validate
	name = request.POST.get('name', '')
	hour = request.POST.get('hour', '')
	minute = request.POST.get('minute', '')
	day = request.POST.get('day', '')
	ampm = request.POST.get('ampm', '')
	year = request.POST.get('year', '')

	#adjustments
	#month
	month = request.POST['month']
	month = months_map[month]
		
	date = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=0)
	now = datetime.now()
	logging.debug( "date: "+str(date))
	logging.debug("now: "+str(now))
			
	email = request.POST.get('email', '')
	phone_number = request.POST.get('phone_number', '')

	if not validate_phone(phone_number):
		response = "invalid phone number"
		rc={'val':1, 'response':response}

	#Do not really need email address here
	#elif not validate_email(email):
		#response = "invalid email"
		#rc={'val':1, 'response':response}
		
	#TODO this is for testing purposes. Need to uncomment this when it goes live
	#elif date < datetime.now():
		#response = "date is before now"
		#rc={'val':1, 'response':response}

	if rc['val'] == 1:
		args = callmeutil.populatecreatepage(request.user)
		rc.update(args)
		logging.debug("fail to create: "+rc['response'])
		return render_to_response('create.html', rc)
		
	#Find the user if he exists
	#list = CUser.objects.filter(phone_number=phone_number)
		
	#create the action
	logging.debug( "creating the action")
	message = "You need to call "+ phone_number 
	action = CAction()
	if users.get_current_user():
		action.sender = users.get_current_user()

	action.phone_number = phone_number
	action.message = 1#message
	action.date_to_be_executed = date
	action.date_created = now
	action.date_finished = now
	action.finished = False
	action.put()

	#request.user.get_profile().caction_set.create(phone_number=phone_number, message=message, date_created=now, date_to_be_executed=date, date_finished=now, finished = False)
	#print user.action_set.all()
	logging.debug( "done")

	args.update(callmeutil.populatecreatepage(request.user))
	return render_to_response(request, templatepage, args)

@login_required
def create(request):
	logging.debug( "create")
	for action in dir(request.user):
		logging.debug( action)
	print request.user.get_profile()
	return HttpResponseRedirect('/account/register/')
	
def validate_phone(phone_number):
	return len(phone_number) > 0

def validate_email(email):
	return len(email) > 0

