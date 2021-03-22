from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import book
from .forms import bookForm
from django.core.paginator import Paginator, EmptyPage
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.


def search(request):
    search = request.GET['search']
    items = book.objects.filter(bookname__icontains = search)
    context = {
            'items': items, 
        }
    return render(request, 'search.html', context)

def home(request):
    return render(request, 'home.html')

def logoutUser(request):
    return redirect("/login")

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, 'Login Successfull!')
            return redirect("/index")

        else:
            #No backend authenticated the credentials
            messages.success(request, 'Invalid Details!')
            return render(request, 'login.html')
    return render(request, 'login.html')


def register(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.success(request, 'Username Already Exists!')
                return render(request, 'register.html')

            elif User.objects.filter(email=email).exists():
                    messages.success(request, 'Email Already Exists!')
                    return render(request, 'register.html')

            else:
                user = User.objects.create_user(email=email, last_name=last_name, first_name=first_name,username=username, password=password1)
                user.save()
                messages.success(request, 'Your Details has been submitted!')
                return render(request, 'login.html')
        else:
            messages.success(request, 'Your Password is incorrect!')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')

def borow(request, item_id):
    item = get_object_or_404(book, pk=item_id)
    
    if request.method == "POST":
        emailid = request.POST['emailid']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        template = render_to_string('email.html', {'bookname': item.bookname, 'name': name ,'email': email, 'phone': phone})
        send_mail(
        'BOOK BORROW',
        template,
        settings.EMAIL_HOST_USER,
        [emailid],
        fail_silently=False,
        )   
        messages.success(request, 'Book Borrow successfully!')
        return render(request, 'borow.html', {'item': item,})
    return render(request, 'borow.html', {'item': item,})

def details(request, item_id):
    item = get_object_or_404(book, pk=item_id)
    return render(request, 'details.html', {'item': item,})

def add(request):   
    if request.method == 'POST':
        form = bookForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                item = book(
                    name=form.cleaned_data['name'],
                    bookname=form.cleaned_data['bookname'], 
                    description=form.cleaned_data['description'], 
                    email_id=form.cleaned_data['email_id'], 
                    pub_date=timezone.now(), 
                    picture = form.cleaned_data['picture'], 
                )
            except:
                raise Http404('Some error happened')
            else:
                item.save()
                messages.success(request, 'Form submission successful!')
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'form.html', {
                'form': form, 
            })
    return render(request, 'form.html', {
        'form': bookForm(), 
    })


def index(request):
        if request.user.is_anonymous:
            return redirect("/")
        items = book.objects.all()
        p = Paginator(items,3)
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {
            'items': page, 
            'header': 'BOOKS',

        }
        return render(request, 'index.html', context)


