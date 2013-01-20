from django.db import models

class Routes(models.Model):
	origin = models.CharField(max_length=500)
	destination = models.CharField(max_length=500)
	origin_address = models.CharField(max_length=500)
	destination_address = models.CharField(max_length=500)
	brand = models.CharField(max_length=500)
	types = models.CharField(max_length=100)
	cost = models.CharField(max_length=100)
	time = models.CharField(max_length=100)
	
