import datetime
import logging
from callme import callmeutil
import re
from google.appengine.ext import db
from google.appengine.ext.db import Model
from django.contrib.auth.models import User
from django.contrib.auth import models

# Create your models here.
class CUser(db.Model):
	#unique
	#user = db.ReferenceProperty(models.User)
	user = db.UserProperty(User)
	#unique
	phone_number = db.PhoneNumberProperty()
	#clients = db.ListProperty(str)
	date_last_used = db.DateTimeProperty('date used')
	secret = db.IntegerProperty()
	verified = db.BooleanProperty()

	class Admin:
		pass

	def validate(self):
		ret = True

		#validate the phone number is the appropriate format
		pnre = re.compile("[0-9]{3}-[0-9]{3}-[0-9]{4}")
		if not pnre.match(self.phone_number):
			ret = False	
		return ret

	def __str__(self):
		ret = self.user.username + " "
		ret += self.phone_number + " "
		ret += self.verified and "verified" or "unverified"
		#ret += self.last_name + " "
		return ret

class CAction(db.Model):
	#sender = db.ReferenceProperty(CUser)
	sender = db.ReferenceProperty(CUser)
	phone_number = db.PhoneNumberProperty()
	message = db.IntegerProperty() #This will be in a template. Referenced to save space
	memo = db.TextProperty() #a note about the thing
	date_created = db.DateTimeProperty('date published')
	date_finished = db.DateTimeProperty('date finished')
	date_to_be_executed = db.DateTimeProperty('date to be executed')
	finished = db.BooleanProperty()

	class Meta:
		ordering = ('date_to_be_executed', 'date_created', 'date_finished')

	class Admin:
		pass

	def __str__(self):
		ret = "message: "+ str(self.message)
		ret += " \nto: " + str(self.phone_number)
		ret += " \nat: " +str(self.date_to_be_executed)
		ret += self.finished and " is finished" or " is not finished"
		return ret

