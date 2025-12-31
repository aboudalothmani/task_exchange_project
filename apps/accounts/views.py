from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm
from apps.web.utils import send_onesignal_notification


def register_view(request):
    if request.user.is_authenticated:
        return redirect("web:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح.")
            send_onesignal_notification("🎉 مرحبًا بك! تم إنشاء حسابك بنجاح، نتمنى لك تجربة رائعة معنا", segments=["All"])
            return redirect("web:home")
    else:
        form = RegisterForm()

    return render(request, "web/auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("web:home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح.")
            return redirect("web:home")
    else:
        form = LoginForm()

    return render(request, "web/auth/login.html", {"form": form})


@login_required
def logout_view(request):
    request.session.pop("admin_gate_ok", None)
    logout(request)
    messages.success(request, "تم تسجيل الخروج.")
    return redirect("accounts:login")
