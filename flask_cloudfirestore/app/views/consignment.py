from google.cloud.firestore_v1.base_query import FieldFilter
from flask.views import MethodView
import json
from flask import jsonify,request
from google.cloud import firestore

db = firestore.Client(project="mlconsole-poc") 
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
            client_doc = db.collection("jai_dev_collection").document(data.get('client_id')).get()
            user_doc = db.collection("jai_dev_collection").document(data.get('created_by')).get()

            if not client_doc.exists:
                return jsonify({'error': 'Client not found'}), 404

            if not user_doc.exists:
                return jsonify({'error': 'User not found'}), 404

            duplicate_consignments = db.collection("jai_dev_collection") \
                .where(filter=(FieldFilter("doc_type", "==", "consignment"))) \
                .where(filter=(FieldFilter("created_by", "==", data.get('created_by')))) \
                .where(filter=(FieldFilter("name", "==", data.get('name')))).get()
            
            if any(consignment.exists for consignment in duplicate_consignments):
                created_consignemnt = db.collection("jai_dev_collection").add({
                    "doc_type": "consignment",
                    "name": data.get('name'),
                    "con_type": data.get('type'),
                    "client_id": data.get('client_id'),
                    "created_by": data.get('created_by'),
                    "updated_by": data.get('created_by')
                })
                return jsonify({'Success': "Consignment created successfully",'document_id': created_consignemnt[1].id}),200
                
            else:
                return jsonify({'error': 'Consignment already exists'}), 404

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
                cons_id = data.get('con_id')

                consignment_doc = db.collection("jai_dev_collection").document(cons_id).get()
                if consignment_doc.exists:
                    data_size_bytes = len(json.dumps(consignment_doc.to_dict()).encode('utf-8'))
                    cons_info = consignment_doc.to_dict()
                    return jsonify(cons_info),200
                else:
                    return jsonify({'error': 'Consignment with this ID not found'}),404

        except Exception as e:
            return jsonify({'error': str(e)}),500



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
            data = request.get_json()
            client_id = data.get('client_id')
            cons_query=db.collection('jai_dev_collection').where(filter=FieldFilter("doc_type","==","consignment")).where(filter=FieldFilter("client_id","==",client_id))
            cons = cons_query.stream()
            
            cons_data = []
            for con in cons:
                con_data = con.to_dict()
                cons_data.append(con_data)

            if cons_data:
                serialized_data = json.dumps(cons_data)
                return jsonify(cons_data),200
            else:
                return jsonify({"error": "There are no consignment associated with the client_id"}),400

        except Exception as e:
            return jsonify({'error': str(e)}),500