from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from bcrypt import checkpw
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class PatientManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # FIRST NAME
        if len(postData['first_name']) < 1:
            errors['first_name'] = 'FIRST name cannot be empty'
        elif len(postData['first_name']) < 3:
            errors['first_name'] = 'FIRST name must be 3+ chars'
        # LAST NAME
        if len(postData['last_name']) < 1:
            errors['last_name'] = 'LAST name cannot be empty'
        elif len(postData['last_name']) < 3:
            errors['last_name'] = 'LAST name must be 3+'
        # EMAIL
        if len(postData['email']) < 1:
            errors['email'] = 'EMAIL cannot be empty'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'EMAIL NOT valid'
        # zip
        if len(postData['zip']) != 5:
            errors['zip'] = 'Zipcode must be 5 numbers'
        # address
        if len(postData['address']) <1:
            errors['address'] = 'please fill in an address'
        # city
        if len(postData['city']) <1:
            errors['city'] = 'Please fill in a City'
        # phone
        if len(postData['phone']) <1:
            errors['phone'] = 'enter phone #'
        # if email exists in DB 
        if Patient.objects.filter(email=postData['email']):
            errors['email'] = 'EMAIL already exists!!!'
        # PASSWORD
        if len(postData['password']) < 1:
            errors['password'] = 'Password cannot be BLANK!'
        elif len(postData['password']) <3:
            errors['password'] = 'Password has to be AT LEAST 3 characters!'
        if postData['password'] != postData['password_confirm']:
            errors['password'] = 'Pws do not match!'
        return errors

    def login_validator(self, postData):
        errors = {}
        # check if email is valid
        if len(postData['email']) < 1:
            errors['email'] = 'EMAIL cannot be empty'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'EMAIL NOT valid'
        # check if email exists in DB
        if len(Patient.objects.filter(email=postData['email'])) < 1:
            print('ss')
            # errors['email'] = 'EMAIL does not exit'
        else: # if email exists contiue to password check
            patient_check = Patient.objects.filter(email=postData['email'])
            if len(postData['password']) < 1:
                errors['password'] = 'password cannot be empty'
            elif not checkpw(postData['password'].encode(), patient_check[0].password.encode()):
                errors['password'] = 'pass doesnt match'
        return errors

    def health_validator(self, postData):
        errors = {}
        # SYS
        if len(postData['systolic']) < 1:
            errors['systolic'] = 'SYS no blanks!'
        else:
            if int(postData['systolic']) > 240:
                errors['systolic'] = 'SYS must be less than 240mm Hg'
            if int(postData['systolic']) < 50:
                errors['systolic'] = 'SYS must be MORE than 50mm Hg'
        # DIA
        if len(postData['diastolic']) < 1:
            errors['diastolic'] = 'DIA no blanks!'
        else:
            if int(postData['diastolic']) > 140:
                errors['diastolic'] = 'DIA must be less than 140 mm Hg'
            if int(postData['diastolic']) < 30:
                errors['diastolic'] = 'DIA must be more than 30 mm Hg'
        # glucose
        if len(postData['bloodsugar']) < 1:
            errors['bloodsugar'] = 'glugose no blanks!'
        else:
            if float(postData['bloodsugar']) > 12:
                errors['bloodsugar'] = 'Bloodsugar must be LESS than 12.0mM'
            if float(postData['bloodsugar']) < 3:
                errors['bloodsugar'] = 'bloodsugar must be more than 3.0mM'
        # HR
        if len(postData['heartrate']) < 1:
            errors['heartrate'] = 'no blanks!'
        else:
            if int(postData['heartrate']) < 30:
                errors['heartrate'] = 'HR must be more than 30 bbm'
            if int(postData['heartrate']) > 240:
                errors['heartrate'] = 'HR must be less than 240 bbm'
        return errors


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    weight = models.SmallIntegerField()
    height = models.SmallIntegerField()
    phone = models.BigIntegerField(default=0)
    diabetes = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor_id=models.IntegerField(default=1)
    objects = PatientManager()

class entries(models.Model):
    systolic = models.IntegerField(default=0)
    diastolic = models.IntegerField(default=0)
    bloodsugar = models.DecimalField(default=0.00, decimal_places=2, max_digits=4 )
    heartrate = models.IntegerField(default=0)
    patient_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)