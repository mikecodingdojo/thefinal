from django.shortcuts import render, redirect
from .models import * 
from django.contrib import messages
from django.conf import settings




def index(request):
        
    return render(request, 'index.html')

def profile(request, id):
    context = {
            'user': User.objects.get(id=id)

        }
    return render(request, 'profile.html', context)

def success(request): 
    if 'user' not in request.session:
        return redirect('/')
    
    context = {
        'wall_messages': Wall_Message.objects.all(), 
        
    }
    return render(request, 'feed.html', context)

def register(request): 
    
    # Create a user object
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'])
        request.session['user'] = new_user.first_name
        request.session['id'] = new_user.id
    return redirect('/linklogin')

def login(request):
    if request.method=="POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        # retrieving a user from the db
        logged_user = User.objects.filter(email=request.POST['email'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if logged_user.password == request.POST['password']:
                request.session['user'] = logged_user.first_name
                request.session['id'] = logged_user.id
                
                return redirect('user', logged_user.id)
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def post_mess(request):
    Wall_Message.objects.create(message=request.POST['mess'], poster=User.objects.get(id=request.session['id']))
    return redirect('/success')

def post_comment(request, id):
    #create
    poster = User.objects.get(id=request.session['id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect('/success')

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')
    
def delete_message(request, id):
    destroyed = Wall_Message.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')

def linklogin(request):
    return render(request, 'login.html')

def regpage(request):
    return render(request, 'register.html')

def add_images(request):
        get_user_id = User.objects.all()
        new_file = Upload(file=request.FILES['image'], user=get_user_id)
        new_file.save()
        return redirect("/")





