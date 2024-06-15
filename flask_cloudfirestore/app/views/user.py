
from flask import logging
from flask.views import MethodView
from flask import jsonify,request
import logging
import json
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
db = firestore.Client(project="mlconsole-poc")


class UsersView(MethodView):
    """
      A view class handles operations related to more than one user.like get information of all users related to a client.

      Methods:
        get(self,request): get information of all users of a client

    """
    def get(self):
        """
        Fetch all users of a client based on client_id if the client exists in the database.

        Args:
            request: HttpRequest's object contains client_id whose all users need to fetch from the database.
        
        Return: information of all users of a client in JSON format or an error if the client is invalid.
        """
        try:
            data = request.get_json()
            client_id = data.get('client_id')
            users_query=db.collection('jai_dev_collection').where(filter=FieldFilter("doc_type","==","user")).where(filter=FieldFilter("client","==",client_id))
            users = users_query.stream()

            users_data = []
            for user in users:
                user_data = user.to_dict()
                users_data.append(user_data)

            if users_data:
                serialized_data = json.dumps(users_data)
                data_size_bytes = len(serialized_data.encode("utf-8"))
                return jsonify(users_data),200
            else:
                return jsonify({"error": "There are no users associated with the client_id"}),400

        except Exception as e:
            return jsonify({'error': str(e)}),500


class UserView(MethodView):
    """
        A View class to handle user related operations like creating a new user,fetching information of a user , 
        updating a user and delete a user.

    """
    def get(self):

        """
            Fetch information of a user from database, based on user_id.

            Args:
                request: HttpRequest's object contains id of a user.
            
            Returns: JsonResponse: returns information of a user in the JSON format.
        """
        try:
            data = request.get_json()
            data_size_bytes = len(json.dumps(data).encode('utf-8'))
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

                user_doc = user_ref.get().to_dict()
                return jsonify(user_doc),200
            else:
                return jsonify({'error': 'User not found'}),404
        except Exception as e:
            return jsonify({'error': str(e)}),500

    
    
    def put(self):
        """
            Creating a new user with unique username and contact number,means saving information of a user in database.

            Args:
                request:HttpRequest's object contains information of a user to save in database.
            
            Returns:
                JsonResponse : Returns message in JSON format either data saved successfully or failed.
        """
        logger = logging.getLogger(__name__)
        try:
            data = request.get_json()
            doc_type=data.get("doc_type")
            name=data.get('name')
            username=data.get('username')
            contact=data.get('contact')
            role=data.get('role')
            client=data.get('client_id')
            # duplicate_user = db.collection("jai_dev_collection").where(filter=(FieldFilter("doc_type", "==", "user"))).where(filter=(FieldFilter("username", "==", username))).limit(1)
            # logger.info("duplicate_user: %s",duplicate_user)
            # if len(duplicate_user)>0:
            #     return jsonify({'error': 'User already exist'}),400
            new_user_ref =db.collection("jai_dev_collection").add({"name": name,"username":username, "contact": contact, "role": role,"doc_type":doc_type,"client":client})
            return jsonify({'message': 'User created successfully', 'document_id': new_user_ref[1].id}),200

        except Exception as e:
            return jsonify({'error': str(e)}, status=500)

    def patch(self):
        """
            Update information of a user based on id of a user.

            Args:
                request:HttpRequest's object contains id of a user.
            
            Returns(JsonResponse): returns a message in JSON format either successfully updated or error.
        """
        try:
            data = request.get_json()
            data_size_bytes = len(json.dumps(data).encode('utf-8'))
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
                return jsonify(updated_user_doc),200
            else:
                return jsonify({'error': 'User not found'}),404
        except Exception as e:
            return jsonify({'error': str(e)}),500
    
    def delete(self):
        """
            Delete a user from database based on user_id.

            Args:
                HttpRequest's object contains id of a user, whose information needs to delete.
            
            Returns: returns message in JSON format either user deleted successfully or error.
        """
        try:
            data = request.get_json()
            user_id = data.get('id')

            user_ref = db.collection("jai_dev_collection").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_ref.delete()
                return jsonify({'message': 'User deleted successfully'}),204
            else:
                return jsonify({'error': 'User not found'}),404

        except Exception as e:
            return jsonify({'error': str(e)}, status=500)