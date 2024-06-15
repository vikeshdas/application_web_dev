from app.models import db


from flask.views import MethodView
from flask import jsonify,request
from app.models import Logs ,Consignment


class LogView(MethodView):
    """
        Handling log related operations like inserting log information(create log),fetch information of a log.
    """
    def put(self):
        """
            Insert information of a new log in database.

            Args:
                request(HttpRequest): object of HttpRequst contains information of a log.
            
            Returns:
                JsonResponse:Return message either successfully saved or error(fail) in JSON format.
        """
        data = request.get_json()

        try:
            consignment = Consignment.query.get(data.get("con_id"))
            if not consignment:
                return jsonify({'error': 'Consignment with this id does not exist'}),404

            duplicate_log = Logs.query.filter_by(barcode=data.get('barcode')).first()

            # if duplicate_log is not None:
            #     return jsonify({'error': 'Log with this barcode already exists'}),404

            log = Logs(consignment_id=data.get("con_id"), barcode=data.get('barcode'), length=data.get('length'), volume=data.get('volume'))
            db.session.add(log)
            db.session.commit()

            serialized_data = log.log_serializer()
            return jsonify({'message': 'Log inserted successfully', 'data': serialized_data}), 201

        except Exception as e:
            return jsonify({'error': str(e)}),400

    def get(self):
        """
            Fetch information of a log from database using log id.

            Args:
                request(HttpRequest): HttpRequest object contains log id.

            Response(HttpResponse):Return information of a log in the JSON format or error.
        """
        try:
            data=request.get_json()
            log_id=data.get("id")
            log=Logs.query.filter_by(id=log_id).first()
            if not log:
                return jsonify({'error': 'Log not found'}),404
            serialized_data=log.log_serializer() 
            return jsonify({'message': 'Log inserted successfully', 'data': serialized_data}), 201
        except Exception as e:
            return jsonify({'error': str(e)}),400

class LogsView(MethodView):
    """
        View class to Handle operations related to more than one log for example
        get all logs of a consignment.

    """
    def get(self):
        """
            Get information of all logs related to a consignment.

            Args:
                request(HttpRequest):object of HttpRequest contains consignment's id.
            
            Response:
                JsonResponse: return information of all logs related to a consignment in JSON format.
        """
        try:
            data=request.get_json()
            con_id = data.get('con_id')
            consignment_exist=Consignment.query.filter_by(id=con_id).first()
            if not consignment_exist:
                return jsonify({'error': 'consignment with this id  not found'}),404
            
            logs = Logs.query.filter_by(consignment_id=con_id).all()
            serialized_data = [log.log_serializer() for log in logs]
            return jsonify({'data': serialized_data}), 201
        
        except Exception as e:
            return jsonify({'error': str(e)}),400

        

