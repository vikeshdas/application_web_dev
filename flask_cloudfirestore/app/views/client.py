
from flask.views import MethodView
from flask import request, jsonify
from datetime import datetime
from google.cloud import firestore


db = firestore.Client(project="mlconsole-poc")


class ClientView(MethodView):
    """
        A view for handling client related operation like creating a new client.
        A client is a admin who buys subscription for our application or we can 
        say that client is a owner of a factory who makes logs to plyboard.
    """
    def put(self):
        """
            Create a new client.This function will be required when a client buys subscription.
            When client signup then this function will be executing.

            Args:
                HttpRequest :Contains client data in request body.

            Returns:
                JsonResponse:return JSON, that client is created successfully. 
        """
        try:
            data = request.get_json()
            contact=data.get('contact')
            duplicate_client = db.collection("jai_dev_collection").where("doc_type", "==", "client").where("contact", "==", contact).get()
            # if len(duplicate_client):
            #     return jsonify({'error': "Client already exists"}),400
            new_user_ref=db.collection("jai_dev_collection").add({"doc_type":data.get('doc_type'),"name":data.get('name'),"address":data.get('address'),"contact":data.get('contact'),"updated_at":datetime.now(),"created_at":datetime.now(),"email":data.get('email')})
            return jsonify({'message': 'Client created successfully','document_id': new_user_ref[1].id}),200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

