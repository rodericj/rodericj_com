import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CUser(models.Model):
	user = models.ForeignKey(User, unique=True)
	phone_number = models.PhoneNumberField(unique=True)
	clients = models.CommaSeparatedIntegerField(maxlength=10)
	date_last_used = models.DateTimeField('date used')
	secret = models.IntegerField()

	def __str__(self):
		#ret = self.username + " "
		#ret += self.first_name + " "
		#ret += self.last_name + " "
		return self.phone_number

class CAction(models.Model):
	sender = models.ForeignKey(CUser)
	phone_number = models.PhoneNumberField()
	message = models.IntegerField() #This will be in a template. Referenced to save space
	date_created = models.DateTimeField('date published')
	date_finished = models.DateTimeField('date finished')
	date_to_be_executed = models.DateTimeField('date to be executed')

	def __str__(self):
		ret = "message: "+ str(self.message)
		ret += " to " + str(phone_number)
		ret += " at " +str(date_to_be_executed)
		return ret
