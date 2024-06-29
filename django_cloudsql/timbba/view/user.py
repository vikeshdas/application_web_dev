from timbba.models import Client,Roles
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.core.cache import cache
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import json

User = get_user_model()

class CustomPagination(PageNumberPagination):
    """
        Custom pagination class that extends the PageNumberPagination provided by Django REST Framework.
        
        This pagination class initialize some vlues for pagination:
        - Default page size of 2.
        - Allows clients to specify the page size via the 'page_size' query parameter.
        - Restricts the maximum page size that can be requested to 100.

        Attributes:
            page_size (int): The default number of items to include in each page.
            page_size_query_param (str): The name of the query parameter that allows clients to set the page size.
            max_page_size (int): The maximum number of items allowed in each page
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserView(APIView):
    permission_classes = [AllowAny]

    """
        A View class to handle user related operations like creating a new user,fetching information of a user , 
        updating a user and delete a user.

    """
    def patch(self, request):
        """
            Update information of a user based on id of a user.

            Args:
                request:HttpRequest's object contains id of a user.
            
            Returns(JsonResponse): returns a message in Json format either successfully updated or error.
        """
        try:
            data = json.loads(request.body)
            user_id = data.get('id')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            user.name = data.get('name',user.name)
            user.username = data.get('username', user.username)
            user.role_id = data.get('role', user.role_id)
            user.contact = data.get('contact', user.contact)
            user.client_id = data.get('client_id', user.client_id)
            user.save()
            return JsonResponse({'message': 'User updated successfully'}, status=200)
        
        except IntegrityError as e:
            if "Duplicate entry" in str(e) and "for key 'client_user.username'" in str(e):
                return JsonResponse({'error': "This username already exists"}, status=409)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


   
    def put(self, request):
        """
            Creating a new user with unique username and contact number,means saving information of a user in database.

            Args:
                request:HttpRequest's object contains information of a user to save in database.
            
            Returns:
                JsonResponse : Returns message in JSON format either data saved successfully or failed.
        """
        data = json.loads(request.body)
        try:
            try:
                role = Roles.objects.get(id=data.get('role_id'))
            except Roles.DoesNotExist:
                return JsonResponse({'error': 'Role not found'}, status=404)

            try:
                client = Client.objects.get(id=data.get('client_id'))
            except Client.DoesNotExist:
                return JsonResponse({'error': 'Client not found'}, status=404)
        
            user = User.objects.create_user(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                username=data.get('username'),
                email=data.get('email'),
                role=role,
                phone=data.get('phone'),
                client=client,
                password=data.get('password')
            )
            
            serialized_data = user.user_serializer()
            return JsonResponse({'message': 'User created successfully', 'data': serialized_data}, status=201, safe=False)
        except Roles.DoesNotExist:
            return JsonResponse({'error': "Role does not exist"}, status=400)
        except Client.DoesNotExist:
            return JsonResponse({'error': "Client does not exist"}, status=400)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return JsonResponse({'error': "User already exists"}, status=409)
            else:
                return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

    def get(self, request):
        """
            Fetch information of a user from the database, based on user_id.

            Args:
                request: HttpRequest's object contains id of a user.

            Returns: JsonResponse: returns information of a user in the JSON format.
        """

        user_id = request.GET.get('id')
        cache_key = f'user_data_{user_id}'

        cached_data = cache.get(cache_key)
        if cached_data:
            response_data = cached_data
            response_data['message'] = 'Data retrieved from cache'
            return JsonResponse(response_data, status=200)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        serialized_data = user.user_serializer()
        cache.set(cache_key, serialized_data, timeout=300)
        return JsonResponse(serialized_data, status=200)
        
    def delete(self, request):
        
        """
            Delete a user from database based on user_id.

            Args:
                HttpRequest's object contains id of a user, whose information needs to delete.
            
            Returns: returns message in JSON format either user deleted successfully or error.
        """
        data = json.loads(request.body)
        user_id = data.get('id')
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'},status=204)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        
class Users(APIView):
    """
      A view class handles operations related to more than one user.like get information of all users related to a client.

      Methods:
        get(self,request): get information of all users of a client

    """

    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
            Fetch all users of a client based on client_id .if client exist in database

            Args:
                request: HttpRequest's object contains client_id whose all user need to fetch from database.
            
            Return: information of all user of a client in the JSON format or error if client is invalid.
                
        """
        data = request.GET
        client_id = data.get('client_id')

        if not Client.objects.filter(id=client_id):
            return JsonResponse({"error": "There is no such client"}, status=409, safe=False)
        try:
            users = User.objects.filter(client_id=client_id)
            paginator = CustomPagination()
            paginated_users = paginator.paginate_queryset(users, request)
            serialized_data = [user.user_serializer() for user in paginated_users]

            return paginator.get_paginated_response(serialized_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)