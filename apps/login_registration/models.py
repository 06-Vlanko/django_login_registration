# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager (models.Manager):
    def regValidator (self, postData):
        errors = []
        backToForm = False #flag to determine if there were errors

        #verfies the length of string entered in the first_name field
        if len(postData['first_name'])<2:
            backToForm = True
            errors.append ('The "First Name" should be at least 2 characters')
        else: #verifies if all characters in first_name are letters
            for character in postData['first_name']:
                if not character.isalpha():
                    backToForm = True
                    errors.append('The "First Name" field should only contain letters')
                    break

        #verifies the first_name value
        if len(postData['last_name'])<1:
            backToForm = True
            errors.append ('The "Last Name" field cannot be empty')
        else: #verifies if all characters in last_name are letters
            for character in postData['last_name']:
                if not character.isalpha():
                    backToForm = True
                    errors.append ('The "Last Name" field should only contain letters')
                    break

        #verifies the email value
        if len(postData['email'])<1:
            backToForm = True
            errors.append ('The "Email" field cannot be empty')
        #checks if the email is in the format something@something.some
        elif not EMAIL_REGEX.match(postData['email']):
            backToForm = True
            errors.append ("The email address you entered is invalid")
        else: #checks if the email is already in use by an existing user
            try:
                User.objects.get(email = postData['email'])
                backToForm = True
                errors.append ('The email address you entered is already in use, please use a different email address')
            except:
                #do nothing
                print '----> THE EMAIL IS AVAILABLE'

        #verifies the password
        if len(postData['password'])<1:
            backToForm = True
            errors.append ('The "Password" field cannot be empty')
        #checks the length of the value entered in the password field, if its less than 8 redirects
        elif len(postData['password'])<=8:
            backToForm = True
            errors.append ('The password must be more than 8 characters')
        
        #checks the confirm_password value
        if len(postData['confirm_password'])<1:
            backToForm = True
            errors.append ('The "Confirm Password" field cannot be empty')
        #checks that the password and confirm password lengths match
        if len(postData['password']) != len(postData['confirm_password']):
            backToForm = True
            errors.append ('The password and confirm password values should match')
        else: #if the lengths match, check if characters are an exact match
            for index in range ( len(postData['password']) ):
                if postData['password'][index] != postData['confirm_password'][index]:
                    backToForm = True
                    errors.append ('The password and confirm password values must match')
                    break
        
        if backToForm:
            return (True, errors)
        else:
            encrypted_pass = bcrypt.hashpw ( postData['password'].encode(), bcrypt.gensalt() )
            print '----->HASHED PASSWORD:', encrypted_pass
            ID = self.create(
                first_name = postData['first_name'],
                last_name = postData['last_name'],
                email = postData['email'],
                password = encrypted_pass
            )
            return (False, ID.id)

    def logValidator (self, postData):
        errors = []
        backToForm = False #flag to determine if there were errors

        #verifies the email is n ot empty
        if len(postData['email'])<1:
            backToForm = True
            errors.append ('The "Email" field cannot be empty')
        #checks if the email is in the format something@something.some
        elif not EMAIL_REGEX.match(postData['email']):
            backToForm = True
            errors.append ("Invalid email address")

        #verifies the password is not empty
        if len(postData['password'])<1:
            backToForm = True
            errors.append ('The "Password" field cannot be empty')
        
        if backToForm:
            return (True, errors)
        else:
            try:
                user = User.objects.get(email=postData['email'])
                print '-----> FOUND USER: ', user
            except:
                errors.append ('The email and password combination that you entered does not match our records, please try again')
                return (True, errors)
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return (False, user.id)
            else:
                errors.append ('The email and password combination that you entered does not match our records, please try again')
                return (True, errors)
        

class User (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return self.first_name