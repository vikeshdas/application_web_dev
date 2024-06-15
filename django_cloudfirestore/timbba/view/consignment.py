from timbba.models import User,Client,Consignment
from django.views import View 
import json
from django.http import JsonResponse
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = firestore.Client(project="mlconsole-poc")  
class ConsignmentView(View):
    """
        View for handling consignment related operations.Consignment is a excel file that 
        contains information of logs with its dimensions and vehicle number in which these 
        logs comes to factory . Same excel file will be inserted in to database. So this
        class helps to insert consignment information in the database.

    """
    def put(self, request):
        """
        Creates a new consignment.

        Args:
            request: HTTP's request object containing consignment information.

        Returns:
            JsonResponse: Success or failure message in JSON format.
        """

        data = json.loads(request.body)
        data_size_bytes = len(json.dumps(data).encode('utf-8'))
        logger.info("DATA SIZE: %s", data_size_bytes)

        try:
           
            client_doc = db.collection("jai_dev_collection").document(data.get('client_id')).get()
            user_doc = db.collection("jai_dev_collection").document(data.get('created_by')).get()

            if not client_doc.exists:
                return JsonResponse({"error": "client_id does not exist"}, status=404)
            if not user_doc.exists:
                return JsonResponse({"error": "user_id does not exist"}, status=404)

      
            duplicate_consignments = db.collection("jai_dev_collection") \
                .where(filter=(FieldFilter("doc_type", "==", "consignment"))) \
                .where(filter=(FieldFilter("created_by", "==", data.get('created_by')))) \
                .where(filter=(FieldFilter("name", "==", data.get('name')))).get()

            # created_consignemnt=""
            if any(consignment.exists for consignment in duplicate_consignments):
                created_consignemnt = db.collection("jai_dev_collection").add({
                    "doc_type": "consignment",
                    "name": data.get('name'),
                    "con_type": data.get('type'),
                    "client_id": data.get('client_id'),
                    "created_by": data.get('created_by'),
                    "updated_by": data.get('created_by')
                })
                # consignment = consignment.get().to_dict()
                return JsonResponse({'Success': "Consignment created successfully",'document_id': created_consignemnt[1].id},status=200)
                # return JsonResponse({'message': 'Consignment already exists'}, status=409)
            
            else:
                created_consignemnt = db.collection("jai_dev_collection").add({
                    "doc_type": "consignment",
                    "name": data.get('name'),
                    "con_type": data.get('type'),
                    "client_id": data.get('client_id'),
                    "created_by": data.get('created_by'),
                    "updated_by": data.get('created_by')
                })
                # consignment = consignment.get().to_dict()
                return JsonResponse({'Success': "Consignment created successfully",'document_id': created_consignemnt[1].id},status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        """
        Fetches details of a consignment from the database by ID.

        Args:
            request: The HttpRequest object containing consignment ID.

        Returns:
            JsonResponse: Details of the consignment. If ID not found, returns an error message.
        """

        try:
            data = json.loads(request.body)
            cons_id = data.get('con_id')

            consignment_doc = db.collection("jai_dev_collection").document(cons_id).get()
            if consignment_doc.exists:
                data_size_bytes = len(json.dumps(consignment_doc.to_dict()).encode('utf-8'))
                logger.info("DATA SIZE in Get: %s", data_size_bytes)
                cons_info = consignment_doc.to_dict()
                return JsonResponse(cons_info, status=200)
            else:
                return JsonResponse({'error': 'Consignment with this ID not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    
class Consignments(View):
    """
        Handles operations related to more than one consignment.
        like fetching all consignments information related of a client.

        Method:
            get(self,request): Fetch all consignments of a particular client.
    """
    def get(self, request):
        """
            Retrieve information of all consignments of a particular client.

            Args:
               request (HttpRequest): object of HttpRequest contains client Id.

            Returns:
                JsonResponse: returns list of consignments of a particular client in JSON format. 
        """
        try:    
            data = json.loads(request.body)
            client_id = data.get('client_id')
            cons_query=db.collection('jai_dev_collection').where(filter=FieldFilter("doc_type","==","consignment")).where(filter=FieldFilter("client_id","==",client_id))
            cons = cons_query.stream()
            
            cons_data = []
            for con in cons:
                con_data = con.to_dict()
                cons_data.append(con_data)

            if cons_data:
                serialized_data = json.dumps(cons_data)
                data_size_bytes = len(serialized_data.encode("utf-8"))
                logger.info("DATA SIZE in Get: %s", data_size_bytes)
                return JsonResponse(cons_data, status=200, safe=False)
            else:
                return JsonResponse({"error": "There are no consignment associated with the client_id"}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Client not found with this id'}, status=404)
