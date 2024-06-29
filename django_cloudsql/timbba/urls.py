
from django.urls import path
from django.contrib import admin
from timbba.view import consignment, log,user,client,role,login
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', user.UserView.as_view()),
    path('users/', user.Users.as_view()),
    path('consignment/', consignment.ConsignmentView.as_view()),
    path('consignments/', consignment.Consignments.as_view()),
    path('log/', log.Log.as_view()),
    path('logs/', log.Logs.as_view()),
    path('client/', client.ClientView.as_view()),
    path('role/', role.RoleView.as_view()),
    path('login/', login.LoginView.as_view()),
]