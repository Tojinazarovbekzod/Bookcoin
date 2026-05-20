from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.db.models import Count
from functools import wraps
from .models import User, Book, Notification, PurchaseHistory, Comment
import json


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('blog:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _get_session_user(request):
    user_id = request.session.get('user_id')
    return User.objects.filter(id=user_id).first() if user_id else None


def _common_ctx(request):
    user = _get_session_user(request)
    notifications = list(Notification.objects.filter(is_active=True))
    history = list(PurchaseHistory.objects.filter(user=user).order_by('-purchased_at')[:10]) if user else []
    return {"user": user, "notifications": notifications, "history": history}


def _books_for_template(qs):
    return [
        {
            'id': b.id,
            'title': b.title,
            'author': b.author,
            'genre': b.genre,
            'price': b.price,
            'isbn': '',
            'image': b.cover_image,
        }
        for b in qs
    ]


def home_page(request):
    ctx = _common_ctx(request)
    ctx['db_books'] = _books_for_template(
        Book.objects.filter(published=True).order_by('-on_top', '-publish_date')
    )
    return render(request, "main.html", ctx)

def catalog(request):
    ctx = _common_ctx(request)
    ctx['db_books'] = _books_for_template(
        Book.objects.filter(published=True).order_by('-on_top', '-publish_date')
    )
    return render(request, "Catalog.html", ctx)

@login_required
def bookDetail(request):
    return render(request, "bookDetail.html", _common_ctx(request))

@login_required
def studentDashboard(request):
    ctx = _common_ctx(request)
    leaderboard = (
        PurchaseHistory.objects
        .values('user__id', 'user__username', 'user__surname')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )
    ctx['leaderboard'] = list(leaderboard)
    ctx['current_user_id'] = request.session.get('user_id')
    return render(request, "studentDashboard.html", ctx)

@login_required
def settings_page(request):
    user = _get_session_user(request)
    return render(request, "settings.html", {"user": user})

@login_required
def notifications_page(request):
    return render(request, "notifications.html", _common_ctx(request))

@login_required
def history_page(request):
    return render(request, "history.html", _common_ctx(request))

@login_required
def marketPlace(request):
    user = _get_session_user(request)
    db_books = Book.objects.filter(published=True).order_by('-on_top', '-publish_date')
    return render(request, "marketPlace.html", {"user": user, "db_books": db_books})

@login_required
def myBook(request):
    user = _get_session_user(request)
    return render(request, "myBook.html", {"user": user})

@login_required
def store(request):
    user = _get_session_user(request)
    return render(request, "store.html", {"user": user})

def support(request):
    return render(request, "support.html")

def credits(request):
    return render(request, "credits.html")


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            subject=f"New message from {name}",
            message=f"From: {email}\n\nMessage:\n{message}",
            from_email=email,
            recipient_list=['bekzodtojinazar@gmail.com'],
            fail_silently=False,
        )

        return redirect('blog:studentDashboard')

    return render(request, "main.html")


def login(request):
    if request.session.get('user_id'):
        return redirect('blog:studentDashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        account = User.objects.filter(username=username).first()

        if account and check_password(password, account.password):
            request.session['user_id'] = account.id
            return redirect('blog:studentDashboard')
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
                request.session['user_id'] = account.id
                if data.get("remember"):
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(0)  # expires when browser closes
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


@csrf_exempt
@login_required
def api_buy(request):
    if request.method == "POST":
        user = _get_session_user(request)
        try:
            data = json.loads(request.body)
            PurchaseHistory.objects.create(
                user=user,
                book_title=data.get("title", ""),
                book_author=data.get("author", ""),
                book_genre=data.get("genre", ""),
                price=int(data.get("price", 0)),
                book_img=data.get("img", ""),
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"error": "POST only"}, status=405)


@csrf_exempt
@login_required
def api_comments(request):
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        if not book_id:
            return JsonResponse({'error': 'book_id kerak'}, status=400)
        comments = list(Comment.objects.filter(post_id=book_id).values('id', 'author', 'text'))
        return JsonResponse({'comments': comments})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Noto\'g\'ri JSON'}, status=400)

        book_id = data.get('book_id')
        text = data.get('text', '').strip()
        if not text:
            return JsonResponse({'success': False, 'error': 'Matn bo\'sh bo\'lmasin'}, status=400)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Kitob topilmadi'}, status=404)

        user = _get_session_user(request)
        comment = Comment.objects.create(author=user.username, text=text, post=book)
        return JsonResponse({'success': True, 'comment': {'id': comment.id, 'author': comment.author, 'text': comment.text}})

    return JsonResponse({'error': 'POST yoki GET ruxsat etilgan'}, status=405)


def logout(request):
    request.session.flush()
    return redirect('blog:login')


@login_required
def update_profile(request):
    if request.method == "POST":
        user = _get_session_user(request)
        username = request.POST.get("username", "").strip()
        surname = request.POST.get("surname", "").strip()
        email = request.POST.get("email", "").strip()

        if username:
            user.username = username
        if surname:
            user.surname = surname
        if email:
            user.email = email
        user.save()

    return redirect('blog:settings_page')


@login_required
def change_password(request):
    if request.method == "POST":
        user = _get_session_user(request)
        old_password = request.POST.get("old_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not check_password(old_password, user.password):
            return render(request, "settings.html", {"user": user, "password_error": "Current password is incorrect."})

        if new_password != confirm_password:
            return render(request, "settings.html", {"user": user, "password_error": "New passwords do not match."})

        if len(new_password) < 6:
            return render(request, "settings.html", {"user": user, "password_error": "Password must be at least 6 characters."})

        user.password = make_password(new_password)
        user.save()
        return render(request, "settings.html", {"user": user, "password_success": "Password changed successfully."})

    return redirect('blog:settings_page')


@login_required
def delete_account(request):
    if request.method == "POST":
        user = _get_session_user(request)
        user.delete()
        request.session.flush()
        return redirect('blog:login')
    return redirect('blog:settings_page')


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

            remember = data.get("remember", False)

            account = User.objects.create(
                username=username,
                surname=surname,
                email=email,
                password=make_password(password)
            )

            if remember:
                request.session['user_id'] = account.id
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days

            return JsonResponse({"success": True, "username": account.username})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON format xato!"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Faqat POST method ruxsat etilgan"}, status=405)


def main(request):
    ctx = _common_ctx(request)
    ctx['db_books'] = _books_for_template(
        Book.objects.filter(published=True).order_by('-on_top', '-publish_date')
    )
    return render(request, "main.html", ctx)
