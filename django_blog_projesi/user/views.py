from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.


def register(request):
    form = RegisterForm(request.POST or None) # GET ve POST durumlarının ikisini de kontrol ediyoruz.
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid(): # POST Metodu çağrılırsa burası çalışacak - clean() metodunun çalıştığı alan
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # 'User' modelini 'django.contrib.auth.models'den import edip kullanıcı kaydını oluşturuyoruz.

            newUser = User(username=username)
            newUser.set_password(password)
            newUser.save()

            # Kayıt olduktan sonra 'login' olmasını istiyorsak, 'django.contrib.auth'dan 'login'i import ediyoruz.

            login(request,newUser)
            messages.info(request, "Başarıyla kayıt oldunuz!")

            # 'Kayıt' ettikten sonra 'Login' işlemini de gerçekleştirdik. Daha sonra 'Anasayfa'ya dönüş yapalım.
            # 'django.shortcuts'dan 'redirect' modelini import edelim.

            return redirect("index")
        
    # GET metoduyla burası çalışacak, formu görüntüleyeceğiz.

    context = {
        "form" : form,
    }
    return render(request,"register.html", context)


def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form,
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola hatalı!")
            return render(request, "login.html",context)
        
        messages.success(request,"Başarıyla giriş yaptınız!")
        login(request,user)
        return redirect("index")
    
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız!")
    return redirect("index")

def dashboard(request):
    return render(request, "dashboard.html")
