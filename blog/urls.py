from django.urls import path
from .views import login, logout, signup, main, api_login, api_signup, home_page, catalog, contact_view, bookDetail, studentDashboard, settings_page, marketPlace, myBook, store, support, update_profile, change_password, delete_account, api_buy, notifications_page, history_page, api_comments

app_name = "blog"

urlpatterns = [
    path("", home_page, name="home"),
    path("main/", main, name="main"),
    path("catalog/", catalog, name="catalog"),
    path("bookDetail/", bookDetail, name="bookDetail"),
    path("studentDashboard/", studentDashboard, name="studentDashboard"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("api/login/", api_login, name="api_login"),
    path("signup/", signup, name="signup"),
    path("api/signup/", api_signup, name="api_signup"),
    path("settings/", settings_page, name="settings_page"),
    path("marketPlace/", marketPlace, name="marketPlace"),
    path('contact/', contact_view, name='contact_view'),
    path("myBook/", myBook, name="myBook"),
    path("store/", store, name="store"),
    path("support/", support, name="support"),
    path("settings/update-profile/", update_profile, name="update_profile"),
    path("settings/change-password/", change_password, name="change_password"),
    path("settings/delete-account/", delete_account, name="delete_account"),
    path("api/buy/", api_buy, name="api_buy"),
    path("api/comments/", api_comments, name="api_comments"),
    path("notifications/", notifications_page, name="notifications"),
    path("history/", history_page, name="history"),
]


