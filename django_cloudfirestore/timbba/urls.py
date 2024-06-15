
from django.urls import path

from timbba.view import consignment, log,user,client,role
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('user/',csrf_exempt(user.UserView.as_view())),
    path('users/',csrf_exempt(user.Users.as_view())),
    path('consignment/',csrf_exempt(consignment.ConsignmentView.as_view())),
    path('consignments/',csrf_exempt(consignment.Consignments.as_view())),
    path('log/',csrf_exempt(log.Log.as_view())),
    path('logs/',csrf_exempt(log.Logs.as_view())),
    path('client/',csrf_exempt(client.ClientView.as_view())),
    path('role/',csrf_exempt(role.RoleView.as_view()))
]
