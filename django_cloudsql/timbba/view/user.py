from timbba.models import User,Client,Roles
from django.views import View 
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError

 

class UserView(View):
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
            duplicate_username = User.objects.filter(username=data.get('username'))
            contact_duplicate= User.objects.filter(contact=data.get('contact'))
            exist_role=Roles.objects.filter(id=data.get('role_id'))
            exist_client=Client.objects.filter(id=data.get('client_id'))

            if not exist_client:
                return JsonResponse({"error": "Client with this id not exists"}, status=409, safe=False)
        
            if not exist_role:
                return JsonResponse({"error": "Role with this id not exists"}, status=409, safe=False)
            
            # if duplicate_username.exists():
            #     return JsonResponse({"error": "User with this username already exists"}, status=409, safe=False)
            
            # if contact_duplicate:
            #     return JsonResponse({"error": "User with this contact number already exists"}, status=409, safe=False)

            user = User(name=data.get('name'),username=data.get('username'),role_id=data.get('role_id'),contact=data.get('contact'),client_id=data.get('client_id'))
            user.save()
            serialized_data = user.user_serializer()
            return JsonResponse({'message': 'User created successfully', 'data': serialized_data}, status=201, safe=False)

        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return JsonResponse({'error': "User already exists"}, status=409)
            else:
                return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get(self, request):
        """
            Fetch information of a user from database, based on user_id.

            Args:
                request: HttpRequest's object contains id of a user.
            
            Returns: JsonResponse: returns information of a user in the JSON format.
        """
        data = json.loads(request.body)
        user_id = data.get('id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        serialized_data = user.user_serializer() 
        return JsonResponse(serialized_data,status=200)
    

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


class Users(View):
    """
      A view class handles operations related to more than one user.like get information of all users related to a client.

      Methods:
        get(self,request): get information of all users of a client

    """
    def get(self, request):
        """
            Fetch all users of a client based on client_id .if client exist in database

            Args:
                request: HttpRequest's object contains client_id whose all user need to fetch from database.
            
            Return: information of all user of a client in the JSON format or error if client is invalid.
                
        """
        print("inside function",request.body)
        data = json.loads(request.body)
        client_id = data.get('client_id')
        if not Client.objects.filter(id=client_id):
            return JsonResponse({"error": "There is no such client"}, status=409, safe=False)
        try:
            users = User.objects.filter(client_id=client_id)
            serialized_data = [user.user_serializer() for user in users]
            return JsonResponse(serialized_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        