from timbba.models import Roles
from django.views import View 
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError
 


class RoleView(View):
    """
        View class to handle Role related operations like creating role. Role can be like mobile,web .mobile means user can 
        access information using only mobile,or web or both.

    """
    def put(self, request):
        """
            Create new role.

            Args:
                request (HttpRequest): object of HttpRequest contains information of a role to save in database.

            Return:
                 Response(JsonResponse):return Jsonresponse either role created successfully or error.
        """
        data = json.loads(request.body)

        try:
            duplicate_role = Roles.objects.filter(name=data.get('name'))
            if duplicate_role:
                return JsonResponse({'error': "Role already exists"}, status=400)
            
            role = Roles(name=data.get('name'))
            role.save()
            serialized_data = role.role_serializer()
            return JsonResponse({'message': 'Role created successfully', 'data': serialized_data}, status=201, safe=False)

        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return JsonResponse({'error': "Role already exists"}, status=409)
            else:
                return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)