from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
class Survey(models.Model):
	id = models.UUIDField(primary_key=True, default = uuid.uuid4)
	title = models.CharField(max_length = 250)
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('complete-form', args=[str(self.id)])


class Template_question(models.Model):
	question = models.TextField()
	question_number = models.IntegerField()
	question_type = models.IntegerField()
	form = models.ForeignKey(Survey, on_delete = models.SET_NULL, null = True)
	class Meta:
		abstract = True
	def __str__(self):
		return self.question

class Line(Template_question):
	question_valid = models.IntegerField()

class Para(Template_question):
	pass

class Single(Template_question):
	pass

class Multi(Template_question):
	pass

class Slider(Template_question):
	pass

class Toggle(Template_question):
	pass

class Drop(Template_question):
	pass

class File(Template_question):
	question_valid = models.IntegerField()

class Template_option(models.Model):
	option = models.TextField()
	option_number = models.IntegerField()
	class Meta:
		abstract = True

class Single_option(Template_option):
	template = models.ForeignKey(Single, on_delete=models.SET_NULL, null = True)

class Multi_option(Template_option):
	template = models.ForeignKey(Multi, on_delete=models.SET_NULL, null = True)

class Drop_option(Template_option):
	template = models.ForeignKey(Drop, on_delete=models.SET_NULL, null = True)

class Line_response(models.Model):
	parent_question = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True)
	question_type = 1
	answer = models.CharField(max_length =250)
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Para_response(models.Model):
	parent_question = models.ForeignKey(Para , on_delete=models.SET_NULL, null=True)
	question_type = 2
	answer = models.TextField()
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Single_response(models.Model):
	parent_question = models.ForeignKey(Single, on_delete=models.SET_NULL, null=True)
	parent_option = models.ForeignKey(Single_option,on_delete=models.SET_NULL, null=True)
	question_type = 3
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Multi_response(models.Model):
	parent_question = models.ForeignKey(Multi, on_delete=models.SET_NULL, null=True)
	parent_option = models.ForeignKey(Multi_option,on_delete=models.SET_NULL, null=True)
	question_type = 4
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Toggle_response(models.Model):
	parent_question = models.ForeignKey(Toggle, on_delete=models.SET_NULL, null = True)
	answer = models.IntegerField()
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	question_type = 7

class Drop_response(models.Model):
	parent_question = models.ForeignKey(Drop, on_delete = models.SET_NULL, null = True)
	parent_option = models.ForeignKey(Drop_option, on_delete = models.SET_NULL, null=True)
	question_type = 5
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class File_response(models.Model):
	parent_question = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
	question_type = 6
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	answer = models.FileField()

class Slider_response(models.Model):
	parent_question = models.ForeignKey(Slider, on_delete= models.SET_NULL, null = True)
	question_type = 8
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	answer = models.IntegerField()
