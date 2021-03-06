'''
    Here is the model class. This class is the Model portion of the MVC Architecture. We will have 4 different 
    models. 
'''
from django.db import models
from .zipcodes import zipcode as ZipcodeParser
import json

'''
    Here is the Address Class. Hold an address based on there credentials in the form.
    Here is the following ERD Table:
                {
                    ID (PK),
                    Number,
                    City,
                    State,
                    Zipcode
                }
    We are assuming that the clients all stay in the US

    The isCorrect() function findds out if the Address is correct or not by sending an HTTP 
    Request to a ZipCode API and returns the address value in JSON
'''
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(null = False)
    name = models.CharField(max_length = 40, null = False)
    zipcode = models.CharField(max_length=9, null = False)
    city = models.CharField(max_length = 40, null = False)
    state = models.CharField(max_length = 2, null = False)

    def isCorrect(self):
        jsonFile = ZipcodeParser.getAddressInformation(zipcode)
        if jsonFile["city"] != self.city or jsonFile["state"]!= self.state:
            return False
        return True



'''
    Here is the Individual Class. Hold an Individual based on there credentials in the form.
    Here is the following ERD Table:
                {
                    ID (PK),
                    First Name,
                    Last Name,
                    Email,
                    phoneNumber,
                    Address,
                    Policy
                }
    We are assuming that the Individual all stay in the US
'''

class Individual(models.Model):
    licenseNumber = models.CharField(primary_key=True, max_length = 30, default = '000000')
    firstName = models.CharField(max_length = 50, verbose_name = 'INDIVIDUAL_FIRST_NAME')
    lastName = models.CharField(max_length = 50, verbose_name = "INDIVIDUAL_LAST_NAME")
    email = models.CharField(max_length = 120, verbose_name = "INDIVIDUAL_EMAIL")
    phoneNumber = models.CharField(max_length=10,  verbose_name = "INDIVIDUAL_PHONE_NUMBER")
    address = models.OneToOneField(Address,on_delete=models.PROTECT,  related_name='INDIVIDUAL_ADDRESS')

'''
    Here is the Company Class. Hold an Company based on there credentials in the form.
    Here is the following ERD Table:
                {
                    ID (PK),
                    Name,
                    Email,
                    phoneNumber,
                    Address,
                    Policy
                }
    We are assuming that the Company all stay in the US
'''

class Company(models.Model):
    nameOfCompany = models.CharField(max_length = 50, verbose_name = 'COMPANY_NAME')
    email = models.CharField(max_length = 120, verbose_name = "EMAIL")
    phoneNumber = models.CharField(max_length=10, verbose_name = "COMPANY_PHONE_NUMBER")
    address = models.OneToOneField(Address,on_delete=models.PROTECT, related_name='COMPANY_ADDRESS')

'''
    Here is the Policy Class. Hold an Policy based on there credentials in the form.
    Here is the following ERD Table:
                {
                    Type,
                    City,
                    State,
                    Zipcode
                }
'''

class Policy(models.Model):
    types = [('PT1','Policy Type 1'),('PT2','Policy Type 2')]
    policyNumber = models.CharField(max_length = 11, primary_key = True)
    typeOfPolicy = models.CharField(choices = types, max_length = 3)
    effectiveDate = models.DateField()
    individualNumber = models.ForeignKey(Individual, on_delete= models.CASCADE, null=True)
    companyNumber = models.ForeignKey(Company, on_delete = models.CASCADE, null=True)

    def hasBoth(self):
        if self.individualNumber and self.companyNumber:
            return True
        return False