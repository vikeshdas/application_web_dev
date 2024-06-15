from timbba.models import Client
from django.views import View 
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError
from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
db = firestore.Client(project="mlconsole-poc")  

class ClientView(View):
    
    """
        A view for handling client related operation like creating a new client.
        A client is a admin who buys subscription for our application or we can 
        say that client is a owner of a factory who makes logs to plyboard.
    """
    def put(self, request):
        """
            Create a new client.This function will be required when a client buys subscription.
            When client signup then this function will be executing.

            Args:
                HttpRequest :Contains client data in request body.

            Returns:
                JsonResponse:return JSON, that client is created successfully. 
        """
        data = json.loads(request.body)
        data_size_bytes = len(json.dumps(data).encode('utf-8'))
        logger.info("DATA SIZE: %s", data_size_bytes)

        try:
            contact=data.get('contact')
            duplicate_client = db.collection("jai_dev_collection").where("doc_type", "==", "client").where("contact", "==", contact).get()
            # if duplicate_client:
            #     return JsonResponse({'error': "Client already exists"}, status=400)
            new_user_ref=db.collection("jai_dev_collection").add({"doc_type":data.get('doc_type'),"name":data.get('name'),"address":data.get('address'),"contact":data.get('contact'),"updated_at":datetime.now(),"created_at":datetime.now(),"email":data.get('email')})
            return JsonResponse({'message': 'Client created successfully','document_id': new_user_ref[1].id}, status=200, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
