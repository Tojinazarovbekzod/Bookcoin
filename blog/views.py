from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from .models import User
import json


def main(request):
    return render(request, "main.html")

def forgot(request):
    return render(request, "forgot.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        account = User.objects.filter(username=username).first()

        if account and check_password(password, account.password):
            return render(request, "main.html", {"user": account})
        else:
            return render(request, "index.html", {"error": "Username yoki parol noto'g'ri!"})

    return render(request, "index.html")

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            account = User.objects.filter(username=username).first()

            if account and check_password(password, account.password):
                return JsonResponse({"success": True, "username": account.username})
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Username yoki parol noto'g'ri!"
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Noto'g'ri JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": "Server xatosi"}, status=500)

    return JsonResponse({"error": "Faqat POST ruxsat etilgan"}, status=405)


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        surname = request.POST.get("surname")  
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            User.objects.create(
                username=username,
                surname=surname,
                email=email,
                password=make_password(password)
            )
            return redirect("blog:login")

        except IntegrityError:
            return render(request, "createAccaunt.html", {"error": "Bunday username yoki email allaqachon mavjud!"})

    return render(request, "createAccaunt.html")


@csrf_exempt
def api_signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            surname = data.get("surname")   
            email = data.get("email")
            password = data.get("password")

            if not username or not surname or not email or not password:
                return JsonResponse({"success": False, "error": "Majburiy maydonlar to'ldirilmagan!"}, status=400)

            if User.objects.filter(username=username, surname=surname).exists():
                return JsonResponse({"success": False, "error": "Bu username + surname kombinatsiyasi allaqachon mavjud!"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "error": "Bu email allaqachon mavjud!"}, status=400)

            account = User.objects.create(
                username=username,
                surname=surname,
                email=email,
                password=make_password(password)
            )

            return JsonResponse({"success": True, "username": account.username})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON format xato!"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Faqat POST method ruxsat etilgan"}, status=405)



