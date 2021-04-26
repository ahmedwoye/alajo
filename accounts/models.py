from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length =200, null=True)
	phone = models.CharField(max_length =200,null=True)
	email = models.CharField(max_length =200,null=True)
	profile_pic = models.ImageField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length =200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
				('Indoor', 'Indoor'),
				('Out Door', 'Out Door'),
			)
	name =  models.CharField(max_length =200,null=True)
	price = models.FloatField(null=True)
	category =  models.CharField(max_length =200,null=True, choices=CATEGORY)
	description=  models.CharField(max_length =200,null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags= models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


	 


class Order(models.Model):

	STATUS = (
				('pending', 'pending'),
				('out for delivery', 'out for delivery'),
				('Delivered', 'Delivered'),
			)
	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.name


class Payment(models.Model):
	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	shares = models.FloatField(null=True)
	savings = models.FloatField(null=True)
	loan = models.FloatField(null=True)
	rss = models.FloatField(null=True)
	buildingfund = models.FloatField(null=True)
	investment1 = models.FloatField(null=True)
	investment2 = models.FloatField(null= True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

	




 