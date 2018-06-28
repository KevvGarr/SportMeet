from __future__ import unicode_literals
from django.db import models
import bcrypt 
from django.core.validators import validate_email
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


class UserManager(models.Manager):
    def validateRegistration(self, postData):
        result = {}
        errors =[]

        if len(postData["first_name"]) < 1:
            errors.append("Please enter a first name")
            
        if len(postData["last_name"]) < 1:
            errors.append("Please enter a last name")

        if len(postData["email"]) < 2:
            errors.append("Please enter a valid email")
        
        if len(postData["password"]) < 8:
            errors.append("Password must be greater than 8 characters")
        
        if not EMAIL_REGEX.match(postData["email"]):
            errors.append("Please enter a valid email address")

        if postData["password"] != postData["confirm-password"]:
            errors.append("Passwords don't match")

        if len(User.objects.filter(email=postData["email"])) > 0:
            errors.append("Email already exists")

        if len(errors) > 0:            
            result["errors"] = errors
        
        else:
            result["user_id"] = User.objects.create(
                first_name = postData["first_name"],
                last_name = postData["last_name"],
                email = postData["email"],
                password = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()),              
            ).id
        return result


    def validateLogin(self, postData):
        result = {}
        errors = []
        existing_user_list = User.objects.filter(email=postData["email"])

        if len(existing_user_list) > 0:
            if bcrypt.checkpw(postData["password"].encode(), existing_user_list[0].password.encode()):
                result["user_id"] = existing_user_list[0].id
            else:
                errors.append("Invalid email/password")
        else:
            errors.append("Invalid email/password")
        if len(errors) > 0:
            result["errors"] = errors
        return result


class TeamManager(models.Manager):
    def validateTeam(self, postData, user_id):
        errors = []
        if len(postData["name"]) < 1:
            errors.append("Name is too short")
        if len(postData["sport"]) < 1:
            errors.append("Sport type is too short")
        # if postData["start"] > postData["end"]:
        #     errors.append("End date must be after start date")
        if len(errors) == 0:
            Team.objects.create(
                name=postData["name"],
                sport=postData["sport"],
                # start=postData["start"],
                # end=postData["end"],
                uploader=User.objects.get(id=user_id)
            )
        return errors



class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"[User object for {self.user}]"


class Team(models.Model):
    name = models.CharField(max_length = 255)
    sport = models.CharField(max_length = 255)
    uploader = models.ForeignKey(User, related_name = "teams", null=True)
    joined_by = models.ManyToManyField(User, related_name = "join")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TeamManager()

    def __repr__(self):
        return f"[Team object for {self.team}]"

    def __str__(self):
        return f"[Team object for {self.team}]"



# class UserManager(models.Manager):
#     def validateRegistration(self, postData):
#         response ={
#             'isValid':False,
#             'errors': []
#         }
#         errors = []
#         # user_regex = re.compile(r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',re.IGNORECASE)


#         if len(postData['full_name']) <2:
#             errors.append("first name is too short.  need more than 2 characters")
            
#         if len(postData['alias']) <2:
#             errors.append("Alias is too short. need more than 2 characters")

#         if postData['pw'] != postData['cw']:
#             errors.append("Password and Confirm Password don't match")
        
#         if len(postData['pw']) < 8:
#             errors.append("Password must be greater than 8")
        
#         # if not validate_email(postData['email']):       
#         #     errors.append("enter valid email")
#         if len(errors):            
#             response['errors'] = errors
#             return response        
#         else:
#             response['isValid'] = True
#             response['user'] = User.objects.create(                
#                 full_name = postData['full_name'],
#                 alias = postData['alias'],
#                 email = postData['email'],
#                 passwordHash = bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt()),              
#             )
#         return response


#     def validateLogin(self, postData):
#         response ={
#             'isValid': False,
#         }
#         errors =[]

#         if len(postData['email']) <1:
#             errors.append("please enter email")
            
#         if len(postData['pw']) <1:
#             errors.append("please enter password")
        
#         if len(errors):            
#             response['login_errors'] = errors
#             return response

#         user_list = User.objects.filter(email=postData['email'])

#         if len(user_list):
#             #succesful Login
#             if bcrypt.checkpw(postData['pw'].encode(), user_list[0].passwordHash.encode()):
#                 response['isValid'] = True
#                 response['user'] = user_list[0]                
#                 return response
#             else: #Invalid Login                
#                 errors.append("Login email/password is wrong. please try again")
#                 response['login_errors'] = errors
#             return response 

#         errors.append("please enter valid email/password")
#         response['login_errors'] = errors
#         return response




# class User(models.Model):
#     full_name = models.CharField(max_length = 255)
#     alias = models.CharField(max_length = 255)
#     email = models.CharField(max_length = 255)
#     passwordHash = models.CharField(max_length = 255)     
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)    
#     objects = UserManager()
#     def __repr__(self):
#         return f"[User for {self.first_name}]"




# class Book(models.Model):
#     title = models.CharField(max_length = 255)
#     author  = models.TextField(max_length = 1000) 
#     # reviewers = models.ManyToManyField(User, related_name="book_reviews") 
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     def __repr__(self):
#         return f"[Book for {self.name}]"


# class Review(models.Model):    
#     review = models.TextField(null= True)
#     rating = models.IntegerField(default = 1)     
#     book = models.ForeignKey(Book, null=True, related_name="book_reviews")
#     user = models.ForeignKey(User, null=True, related_name="user_reviews")
      
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)    
#     def __repr__(self):
#         return f"[Review for {self.review}]"