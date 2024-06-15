from flask.views import MethodView
from flask import jsonify,request
import json
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.Client(project="mlconsole-poc")

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
            con_id=data.get('con_id')
            barcode=data.get('barcode')
            length=data.get('length')
            volume=data.get('volume')

            cons_exist=db.collection("jai_dev_collection").document(con_id).get()
            if not cons_exist:
                return  jsonify({'error': 'consignment does not  exist'}),500
          
            duplicate_log = db.collection("jai_dev_collection").where(filter=(FieldFilter("doc_type", "==", "log"))).where(filter=(FieldFilter("barcode", "==", barcode))).get()
            if duplicate_log:
                return jsonify({'error': 'log allready exist'}),400
            
            db.collection("jai_dev_collection").add({"con_id": con_id,"barcode":barcode, "length": length, "volume": volume,"doc_type":"log"})
            return jsonify({'message': 'log created successfully'}),200

        
        except Exception as e:
            return jsonify({'error': str(e)}),500

    def get(self):
        """
            Fetch information of a log from database using log id.

            Args:
                request(HttpRequest): HttpRequest object contains log id.

            Response(HttpResponse):Return information of a log in the JSON format or error.
        """
        try:
            data=request.get_json()
            log_id = data.get('id')
            log_ref = db.collection("jai_dev_collection").document(log_id)
            log_doc = log_ref.get()
            if log_doc.exists:
                log_info = log_doc.to_dict()  
                return jsonify(log_info),200
            else:
                return jsonify({'error': 'Log not found'}),404
        except Exception as e:
            return jsonify({'error': str(e)}),500

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
            consignment_id = data.get('con_id')
            logs_query=db.collection('jai_dev_collection').where(filter=FieldFilter("doc_type","==","log")).where(filter=FieldFilter("con_id","==",consignment_id))
            logs = logs_query.stream()
            logs_data = []
            for log in logs:
                log_data = log.to_dict()
                logs_data.append(log_data)

            if logs_data:
                    serialized_data = json.dumps(logs_data)
                    data_size_bytes = len(serialized_data.encode("utf-8"))
                    return jsonify(logs_data),200
            else:
                return jsonify({"error": "There are no logs associated with the consignment"}),404
        except Exception as e:
            return jsonify({'error': str(e)}),500
        

