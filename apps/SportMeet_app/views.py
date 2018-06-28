from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Team
import bcrypt

# from .models import Book
# from .models import Review


def index(request):
    return render(request, "index.html")

def registerUser(request):    
    response = User.objects.validateRegistration(request.POST)
    if "errors" in response:
        for error in response["errors"]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = response['user_id']
        return redirect('/home_page')

def loginUser(request):
    response = User.objects.validateLogin(request.POST)
    if "errors" in response:
        for error in response["errors"]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = response['user_id']
        return redirect('/home_page')

def logout(request):
    request.session.clear()
    return redirect('/')


def home_page(request):
    context = {
        "user" : User.objects.get(id=request.session["user_id"]),
        "teams" : Team.objects.filter(uploader=User.objects.get(id=request.session["user_id"])) | Team.objects.filter(joined_by=User.objects.get(id=request.session["user_id"])),
        "otherteams" : Team.objects.exclude(uploader=User.objects.get(id=request.session["user_id"])) | Team.objects.filter(joined_by=User.objects.get(id=request.session["user_id"])),
    }
    return render(request, "home_page.html", context)


def addTeam(request):
    context = {
        "user" : User.objects.get(id=request.session["user_id"]),
    }
    return render(request, "createTeam.html", context)


def createTeam(request):
    errors = Team.objects.validateTeam(request.POST, request.session["user_id"])
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/addTeam')
    else:
        return redirect('/home_page')

def viewTeam(request, team_id):
    thisTeam = Team.objects.get(id=team_id)
    context = {
        "team" : thisTeam,
        "users" : User.objects.filter(join=thisTeam)
    }
    return render(request, "viewTeam.html", context)

def joinTeam(request, team_id):
    me = User.objects.get(id=request.session["user_id"])
    team = Team.objects.get(id=team_id)
    team.joined_by.add(me)
    team.save()
    return redirect("/home_page")

def deleteTeam(request, team_id):
    Team.objects.get(id=team_id).delete()
    return redirect("/home_page")

def cancelTeam(request, team_id):
    me = User.objects.get(id=request.session["user_id"])
    team = Team.objects.get(id=team_id)
    team.joined_by.remove(me)
    team.save()
    return redirect("/home_page")




# def index(request):    
#     return render(request, "SportMeet/index.html")


# def register(request):    #POST
#     # print("inside Create User Route**********************")
#     result = User.objects.validateRegistration(request.POST)
#     if result['isValid']: #response==result where isValid =True, user object exists
#         request.session['user_id'] = result['user'].id #result.id
#         request.session['alias'] = result['user'].alias
#         return redirect('home_page')
#     # print(result['errors'])
#     request.session['reg_errors'] = result['errors']
#     return redirect('/') #where isValid =False, errors exist, user object Doesn't exists  


# def login(request): 
#     print("inside Login Route **********************")
#     result = User.objects.validateLogin(request.POST)
#     #succesful login response
#     if result['isValid']: #response==result where isValid =True, user object exists
#         request.session['user_id'] = result['user'].id #result.id
#         request.session['alias'] = result['user'].alias
#         return redirect('/home_page')
#     #invalid login response
#     request.session['login_errors'] = result['login_errors']
#     return redirect('/')

# def logout(request): 
#     print("inside logout Route **********************")
#     request.session.clear() 
#     return redirect('/')




# def books(request): 
#     print("inside books Route **********************")
#     #need all the books and recent 3 reviews.
#     context = {
#             'reviews':Review.objects.all().order_by("-updated_at")[:3],
#             'books':Book.objects.all()
#         }


#     return render(request, 'SportMeet/books.html', context)

# def add(request): 
#     print("inside add Route **********************")
#     context={
#         'books': Book.objects.all()
#     }
#     return render(request, 'SportMeet/add.html', context)


# def addBook(request): #processing book
#     print("inside addBook Route **********************")

#     author=''
#     if len(request.POST['author_added'])<1:
#         author=request.POST['author_selected']

#     if len(request.POST['author_added'])>0:
#         author=request.POST['author_added']

#     if not Book.objects.filter(title=request.POST['title'], author=author):
#         Book.objects.create(title=request.POST['title'], author=author)
#         book = Book.objects.get(title=request.POST['title'])
#         book.book_reviews.create(review=request.POST['review'], rating = request.POST['rating'], user_id=request.session['user_id'])
#         return redirect(f'books/{book.id}')       
    
#     return render(request, 'SportMeet/add.html')

# def bookReviews(request, book_id): 
#     print("inside bookReviews Route **********************")
#     book = Book.objects.get(id=book_id)
#     reviews = book.book_reviews.all()
#     context = {
#         'book': book,  #book object currently added
#         'reviews':reviews #all of the current books reviews
#     }
#     return render(request, 'SportMeet/bookReviews.html', context)

# def newReview(request, book_id): 
#     print("inside newReview Route **********************")   
#     Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book_id=book_id, user_id=request.session['user_id'])
#     # book = Book.objects.get(title=request.POST['title'])
#     return redirect(f'/books/{book_id}')




# def userReviews(request, user_id): 
#     print("inside userReviews Route **********************")
#     user = User.objects.get(id=user_id)
#     reviews = user.user_reviews.all()
#     total = len(reviews)
#     context = {
#         'user':user,
#         'reviews':reviews,
#         'total':total
#     }
#     return render(request, 'SportMeet/userReviews.html', context)

# def destroy(request, review_id):
#     Review.objects.get(id=review_id).delete()
#     return redirect('/books')

