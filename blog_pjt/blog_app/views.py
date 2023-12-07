from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from .forms import BlogForm

# Create your views here.


def sample(request):
    return HttpResponse("Welcome to Django")


def index(request):
    return HttpResponse("Hello World")


def demo(request):
    return render(request, 'demo.html')


def demo2(request):
    context = {'name': 'John'}
    return render(request, 'demo2.html', context)


def demo3(request):
    context = {'name': ['james', 'john', 'arya']}
    return render(request, 'demo3.html', context)


def demo4(request):
    data = [
        {'name': 'john', 'place': 'Calicut'},
        {'name': 'Arya', 'place': 'Tvm'},
        {'name': 'James', 'place': 'Kochi'},
    ]
    context = {'data': data}
    return render(request, 'demo4.html', context)


def demo5(request):
    return render(request, 'demo5.html')

@login_required(login_url='login')
def home(request):
    try:
        blog = Blog.objects.filter(is_published=True)
    except:
        blog = None
    if request.method=='GET':
        search = request.GET.get('search')
    if search:
        blog = Blog.objects.filter(title__icontains=search)

    context = {'blog':blog}
    return render(request, 'home.html',context)


@login_required(login_url='login')
def create_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        genre = request.POST.get('genre')
        blog = Blog.objects.create(title=title,content=content,author=request.user,image=image,genre=genre)
        blog.save()
        return redirect('home')
    context = {'cat':Blog.gener_choices}
    return render(request,"create_blog.html",context)


@login_required(login_url='login')
def edit_blog(request,id):
    try:
        blog_obj = Blog.objects.get(id=id)
    except:
        blog = None
    if request.user != blog_obj.author:
        return HttpResponse('Permission Denied')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        genre = request.POST.get('genre')
        blog_obj.title = title
        blog_obj.content = content
        blog_obj.image = image
        blog_obj.genre = genre
        blog_obj.author = request.user

        blog_obj.save()
        return redirect('home')

    context = {'blog':blog_obj}
    return render(request,"edit_blog.html",context)


@login_required(login_url='login')
def delete_blog(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog = None
    if request.user != blog_obj.author:
        return HttpResponse('Permission Denied')
    if request.method == "POST":
        blog.delete()
        return redirect('home')
    context = {'blog':blog}
    return render(request,'delete_blog.html',context)


@login_required(login_url='login')
def detail(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog = None
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(
            user = request.user,
            blog=blog,
            comment=comment
        )
    comments = Comment.objects.filter(blog=blog)

    context = {'blog':blog,'comments':comments,'edit':None}
    return render(request,'detail.html',context)



def comment_delete(request,id):
    comment = Comment.objects.get(id=id)
    if request.user != comment.user:
        return HttpResponse('Permission Denied')
    blog_id = comment.blog.id
    comment.delete()
    return redirect('detail',blog_id)


def comment_edit(request,id):
    comment = Comment.objects.get(id=id)
    blog = comment.blog
    if request.method == 'POST':
        edit_comment = request.POST.get('comment')
        comment.comment = edit_comment
        comment.save()
        return redirect('detail',blog.id)
    comments = Comment.objects.filter(blog=blog)
    context = {'comment':comment,'blog':blog,'comments':comments,'edit':None}
    return render(request,'detail.html',context)





def register(request):
    print('data',request.META)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2 :
            myuser = User.objects.create_user(username=username,email=email,password=password2)
            myuser.save()
            messages.success(request,'Registraion Succesfully Completed')
            return redirect('home')

        messages.error(request,"Password does not match, Pls try again")
        return redirect('register')

    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            if user.is_superuser:
                messages.success(request,'logged succesfully')
                return redirect('admin_home')
            else:
                messages.success(request,'logged succesfully')
                return redirect('home')

        messages.info(request,'Plz register')
        return redirect('register')
    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username)
        if user:
            email = user.first().email
            otp = random.randrange(1000,9999)
            subject = "Password Reset"
            messages = f'Here is your one time password {otp}'
            from_mail = 'shameemshah097@gmail.com'
            to = [email]
            send_mail(
                subject = subject,
                message = messages,
                from_email = from_mail,
                recipient_list = to,
                fail_silently = False,
            )
            UserOTP.objects.update_or_create(
                user = user.first(),
                defaults = {
                    'otp' : otp
                }
            )
            return redirect('otp_verify',user.first().id)

    return render(request,'forget_password.html')



def otp_verify(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        submitted_otp = request.POST.get('otp')
        send_otp_obj = UserOTP.objects.filter(user=user)
        if submitted_otp == send_otp_obj.first().otp:
            messages.success(request,' otp verified succesfully')
            return redirect('password_reset',user.id)
        messages.error(request,'otp doesnt match')
        return redirect('forget_password')

    return render(request,'otp_verify.html',{'email':user.email})

        




def password_reset(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        password1 = request.POST.get('password1')
        print(password1)

        password2 = request.POST.get('password2')
        print(password2)

        if password2 == password1 :
            user.set_password(password1)
            user.save()
            messages.success(request,'password reset Successfully')
            return redirect('login')
        messages.error(request,'password doesnt match...pls try again')
    return render(request,'password_reset.html')



@login_required(login_url='login')
def create_new(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        form.save()
        return redirect('home')
    messages.error(request,form.errors)

    context = {'form':form}
    return render(request,'create_new.html',context)

    
@login_required(login_url='login')
def edit_new(request,id):
    blog = Blog.objects.get(id=id)
    form = BlogForm(instance=blog)
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES,instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            form.save()
            return redirect('detail',blog.id)
        messages.error(request,form.errors)

    return render(request,'edit_new.html',{'form':form})



@login_required(login_url='login')
def admin_home(request):
    if request.user.is_superuser:
        blog = Blog.objects.all()
        context = {'blog':blog}
    else:
        return HttpResponse('Permission Denied')
    return render(request,'admin.html',context)

def change_status(request,id):
    if request.user.is_superuser:
        blog = Blog.objects.get(id=id)
        blog.is_published = not blog.is_published
        blog.save()
    else:
        return HttpResponse('Permission Denied')
    return redirect('admin_home')


