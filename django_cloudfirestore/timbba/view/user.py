from timbba.models import User,Client,Roles
from django.views import View 
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import logging
db = firestore.Client(project="mlconsole-poc")
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
            data_size_bytes = len(json.dumps(data).encode('utf-8'))
            logger.info("DATA SIZE: %s", data_size_bytes)
            user_id = data.get('id')

            user_ref = db.collection("jai_dev_collection").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_ref.update({
                    "name": data.get('name'),
                    "username": data.get('username'),
                    "contact": data.get('contact'),
                    "role": data.get('role')
                })

                updated_user_doc = user_ref.get().to_dict()
                return JsonResponse(updated_user_doc, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
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

        try:
            data = json.loads(request.body)
            data_size_bytes = len(json.dumps(data).encode('utf-8'))
            logger.info("DATA SIZE: %s", data_size_bytes)
            doc_type=data.get("doc_type")
            name=data.get('name')
            username=data.get('username')
            contact=data.get('contact')
            role=data.get('role')
            client=data.get('client_id')
            # duplicate_user = db.collection("jai_dev_collection").where("doc_type", "==", "user").where("username", "==", username).get()
            # if duplicate_user:
            #     return JsonResponse({'error': 'User already exist'}, status=201, safe=False)
            new_user_ref =db.collection("jai_dev_collection").add({"name": name,"username":username, "contact": contact, "role": role,"doc_type":doc_type,"client":client})
            # return JsonResponse({'message': 'User created successfully'}, status=201, safe=False)
            return JsonResponse({'message': 'User created successfully', 'document_id': new_user_ref[1].id}, status=200, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get(self, request):
        """
            Fetch information of a user from database, based on user_id.

            Args:
                request: HttpRequest's object contains id of a user.
            
            Returns: JsonResponse: returns information of a user in the JSON format.
        """
        logger.info("RICHED TILL HERE CALL MADE: %s")
        data = json.loads(request.body)
        user_id = data.get('id')
        try:
            user_ref = db.collection("jai_dev_collection").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_info = user_doc.to_dict()  
                data_size_bytes=data_size_bytes = len(json.dumps(user_info).encode('utf-8'))
                logger.info("DATA SIZE in Get: %s", data_size_bytes)
                return JsonResponse({"user":user_info}, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    

    def delete(self, request):

        """
            Delete a user from database based on user_id.

            Args:
                HttpRequest's object contains id of a user, whose information needs to delete.
            
            Returns: returns message in JSON format either user deleted successfully or error.
        """
        
        try:
            data = json.loads(request.body)
            data_size_bytes = len(json.dumps(data).encode('utf-8'))
            logger.info("DATA SIZE: %s", data_size_bytes)
            user_id = data.get('id')

            user_ref = db.collection("jai_dev_collection").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                # Delete the document
                user_ref.delete()
                return JsonResponse({'message': 'User deleted successfully'}, status=204)
            else:
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
        try:
            data = json.loads(request.body)
            client_id = data.get('client_id')
            users_query=db.collection('jai_dev_collection').where(filter=FieldFilter("doc_type","==","user")).where(filter=FieldFilter("client","==",client_id))
            users = users_query.stream()

            users_data = []
            for user in users:
                user_data = user.to_dict()
                users_data.append(user_data)

            if users_data:
                logger.info(f"number of users: {len(users_data)}")
                serialized_data = json.dumps(users_data)
                data_size_bytes = len(serialized_data.encode("utf-8"))
                logger.info("DATA SIZE in Get: %s", data_size_bytes)
                return JsonResponse(users_data, status=200, safe=False)
            else:
                return JsonResponse({"error": "There are no users associated with the client_id"}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
