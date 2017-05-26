
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
class UserManager(models.Manager):
    def isValid(self, form_data):
        print "Inside isValid method."
        result = {"pass": True}
        errors = []

        if len(form_data['first_name'])<2 or len(form_data['last_name'])<2:
            errors.append("First and last name must be at least 2 characters long.")
            result["pass"]=False
        if not NAME_REGEX.match(form_data['first_name']) or not NAME_REGEX.match(form_data['last_name']):
            result["pass"]=False
            errors.append("Please enter a name using letters only.")
        if not EMAIL_REGEX.match(form_data['email']):
            result["pass"]=False
            errors.append("Please enter a valid email address.")
        if User.objects.filter(email = form_data['email']).first():
            result["pass"]=False
            errors.append("That email is already taken.")
        if len(form_data['password'])<8:
            result["pass"]=False
            errors.append("Password must be at least 8 characters.")
        if str(form_data['password']) != str(form_data['password_confirmation']):
            result["pass"]=False
            errors.append("Password confirmation does not match password.")
        result['errors'] = errors
        return result

    def createUser(self, form_data):
        password = form_data['password'].encode()
        #Encrypt user's password
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create(first_name=form_data['first_name'], last_name=form_data['last_name'], email=form_data['email'], password=encryptedpw)
        return user

    def logging_in(self, form_data):
        errors = []
        result = {"pass": True}
        user = User.objects.filter(email = form_data['email']).first()
        if user:
            password = form_data['password'].encode()
            user_pass = user.password.encode()
            if bcrypt.hashpw(password, user_pass) == user_pass:
                result['user'] = user
                return result
        #if user doesnt exist, return this error message and prevent login
        if user == None:
            errors.append("That email does not exist")
        #if user exists but password is incorrects return error
        elif user.password != form_data['password']:
            errors.append('Invalid password')
        result["pass"] = False
        result['errors'] = errors
        return result

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    password_confirmation = models.CharField(max_length=25)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()

class Secret(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='secrets')

class Like(models.Model):
    secret = models.ForeignKey(User, related_name='likes')
