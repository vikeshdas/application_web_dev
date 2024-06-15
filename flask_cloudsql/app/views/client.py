
from flask.views import MethodView
from flask import request, jsonify
from app.models import db
from datetime import datetime
from app.models import Client


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
            print("puting client")
            data = request.get_json()
            duplicate_client=Client.query.filter_by(contact=data.get('contact')).first()
            if duplicate_client:
                return jsonify({'error': 'Duplicate client'}), 404
            new_client = Client(
                name=data['name'],
                address=data['address'],
                contact=data['contact'],
                email=data['email'],
                updated_at=datetime.now()
            )

            db.session.add(new_client)
 
            db.session.commit()
            created_client = Client.query.filter_by(id=new_client.id).first()

        # Construct the response JSON
            response_data = {
                'message': 'Client created successfully',
                'client': {
                    'id': created_client.id,
                    'name': created_client.name,
                    'address': created_client.address,
                    'contact': created_client.contact,
                    'email': created_client.email,
                    'updated_at': created_client.updated_at
                }
            }

            return jsonify(response_data), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

