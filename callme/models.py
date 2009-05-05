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
	verified = models.BooleanField()

	class Admin:
		pass

	def __str__(self):
		ret = self.user.username + " "
		ret += self.phone_number + " "
		ret += self.verified and "verified" or "unverified"
		#ret += self.last_name + " "
		return ret

class CAction(models.Model):
	sender = models.ForeignKey(CUser)
	phone_number = models.PhoneNumberField()
	message = models.IntegerField() #This will be in a template. Referenced to save space
	date_created = models.DateTimeField('date published')
	date_finished = models.DateTimeField('date finished')
	date_to_be_executed = models.DateTimeField('date to be executed')
	finished = models.BooleanField()

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
