from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render, reverse
from django.urls import reverse

from icecream import ic

from .forms import LoginForm, RegisterForm
from .models import User

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL or reverse("login")


def login(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        ic(form.is_valid)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user = User.objects.get(email=email)
                user = authenticate(email=email, password=password)

                if user is not None:
                    auth_login(request, user)
                    messages.success(request, "Logged in successfully")
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    ic("Invalid")
                    messages.error(request, "Invalid email or password.")

            except User.DoesNotExist:
                ic("User not existws")
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request=request, message="Invalid email or password.")
            return redirect(reverse("login"))

    context = {"form": form}
    return render(request=request, template_name="login.html", context=context)


def register_user(request):
    form = RegisterForm(request.POST or None)

    if request.method == "GET":
        context = {"form": form}
        return render(request=request, template_name="register.html", context=context)

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.set_password(password)
            user.save()
            messages.success(request, "User registered successfully")
            return redirect("login")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )

    context = {"form": form}
    return render(request, "register.html", context)


def logout(request):
    auth_logout(request)
    return redirect("/")
