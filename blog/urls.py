from django.urls import path
from .views import login, signup, main, api_login, api_signup, home_page, catalog, contact_view, bookDetail, studentDashboard, settings_page, marketPlace, myBook, store, support

app_name = "blog"

urlpatterns = [
    path("", home_page, name="home"),
    path("main/", main, name="main"),
    path("catalog/", catalog, name="catalog"),
    path("bookDetail/", bookDetail, name="bookDetail"),
    path("studentDashboard/", studentDashboard, name="studentDashboard"),
    path("login/", login, name="login"),  
    path("api/login/", api_login, name="api_login"), 
    path("signup/", signup, name="signup"),
    path("api/signup/", api_signup, name="api_signup"),
    path("settings/", settings_page, name="settings_page"),
    path("marketPlace/", marketPlace, name="marketPlace"),
    path('contact/', contact_view, name='contact_view'),
    path("myBook/", myBook, name="myBook"),
    path("store/", store, name="store"),
    path("support/", support, name="support"),
]


