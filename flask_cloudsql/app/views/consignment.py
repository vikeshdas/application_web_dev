from app.models import db
from datetime import datetime

from flask.views import MethodView
from flask import jsonify,request

from app.models import User,Client,Consignment

class ConsignmentView(MethodView):
    """
        View for handling consignment related operations.Consignment is a excel file that 
        contains information of logs with its dimensions and vehicle number in which these 
        logs comes to factory . Same excel file will be inserted in to database. So this
        class helps to insert consignment information in the database.
    """
    def put(self):
        """
            Create a new consignment. Add information of consignment like vehicle number,consignment name,
            with client information,user information who inserts these information using my application.

            Args: 
                request:HTTP's request object contains information of a consignment
            
            Return:
                JsonResponse: success or fail in JSON form
        """
        try:
            data = request.get_json()
            user_id = data.get("created_by_id")
            client_id = data.get("client_id")
            user = User.query.filter_by(id=user_id).first()
            client = Client.query.filter_by(id=client_id).first()

            if not user:
                return jsonify({'error': 'User not found'}), 404

            if not client:
                return jsonify({'error': 'Client not found'}), 404

            # duplicate_consignment = Consignment.query.filter_by(client_id=client_id, created_by_id=user_id, name=data.get('name')).first()
            
            # if not duplicate_consignment:
            new_consignment = Consignment(
                name=data.get('name'),
                type=data.get('type'),
                client_id=client_id,
                created_by_id=user_id,
                updated_by_id=user_id,
                updated_at=datetime.now()
            )

            db.session.add(new_consignment)
            db.session.commit()

            return jsonify({'message': 'Consignment added successfully','consignment':new_consignment.con_serializer()}), 201
            
            # else:
            #     return jsonify({'error': 'Consignment already exists'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 404

    def get(self):
        """
            Fetch details of a consignment from the database by Id.

            Args: 
                request : The object of HttpRequest contains consignment Id.
            
            Returns:
                JsonResponse: Details of a consignment.if Id not found in database return a error message.
        """
        try:
            data = request.get_json()
            consignment=Consignment.query.get(data.get("con_id"))

            if not consignment:
                return jsonify({'error': 'Consignment not found'}), 404

            return jsonify({'consignment': consignment.con_serializer()}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 404


class ConsignmentsView(MethodView):
    """
        Handles operations related to more than one consignment.
        like fetching all consignments information related of a client.

        Method:
            get(self,request): Fetch all consignments of a particular client.
    """
    def get(self):
        """
            Retrieve information of all consignments of a particular client.

            Args:
               request (HttpRequest): object of HttpRequest contains client Id.

            Returns:
                JsonResponse: returns list of consignments of a particular client in JSON format. 
        """
        try:

            data=request.get_json() 
            client=Client.query.get(data.get("client_id"))
            consignments = Consignment.query.filter_by(client_id = data.get("client_id")).all()

            if not client:
                return jsonify({'error': 'Client not found'}), 404
            
            serialize_consigment=[ con.con_serializer() for con in consignments]
            return jsonify({'consignments': serialize_consigment}), 201
        except Exception as e:
            return jsonify({'error': str(e)}),404
        