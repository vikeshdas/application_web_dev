from timbba.models import Consignment,Item
from django.views import View 
import json
from django.http import JsonResponse
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
db = firestore.Client(project="mlconsole-poc")
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Log(View):
    """
        Handling log related operations like inserting log information(create log),fetch information of a log.
    """
    def put(self, request):
        """
            Insert information of a new log in database.

            Args:
                request(HttpRequest): object of HttpRequst contains information of a log.
            
            Returns:
                JsonResponse:Return message either successfully saved or error(fail) in JSON format.
        """
        try:
            data = json.loads(request.body)
            data_size_bytes = len(json.dumps(data).encode('utf-8'))
            logger.info("DATA SIZE: %s", data_size_bytes)
            con_id=data.get('con_id')
            barcode=data.get('barcode')
            length=data.get('length')
            volume=data.get('volume')

            cons_exist=db.collection("jai_dev_collection").document(con_id).get()
            if not cons_exist:
                return  JsonResponse({'error': 'consignment does not  exist'}, status=500, safe=False)
            
            duplicate_log = db.collection("jai_dev_collection").where("doc_type", "==", "log").where("barcode", "==", barcode).get()
            # if duplicate_log:
            #     return JsonResponse({'error': 'log allready exist'}, status=201, safe=False)
            
            db.collection("jai_dev_collection").add({"con_id": con_id,"barcode":barcode, "length": length, "volume": volume,"doc_type":"log"})
            return JsonResponse({'message': 'log created successfully'}, status=200, safe=False)

        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get(self, request):
        """
            Fetch information of a log from database using log id.

            Args:
                request(HttpRequest): HttpRequest object contains log id.

            Response(HttpResponse):Return information of a log in the JSON format or error.
        """
        data = json.loads(request.body)
        log_id = data.get('id')
        try:
            log_ref = db.collection("jai_dev_collection").document(log_id)
            log_doc = log_ref.get()
            if log_doc.exists:
                data_size_bytes = len(json.dumps(log_doc.to_dict()).encode('utf-8'))
                logger.info("DATA SIZE: %s", data_size_bytes)
                log_info = log_doc.to_dict()  
                return JsonResponse(log_info, status=200)
            else:
                return JsonResponse({'error': 'Log not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class Logs(View):
    """
        View class to Handle operations related to more than one log for example
        get all logs of a consignment.

    """
    def get(self, request):
        """
            Get information of all logs related to a consignment.

            Args:
                request(HttpRequest):object of HttpRequest contains consignment_id.
            
            Response:
                JsonResponse: return information of all logs related to a consignment in JSON format.
        """
        try:
            data = json.loads(request.body)
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
                    logger.info("DATA SIZE in Get: %s", data_size_bytes)
                    return JsonResponse(logs_data, status=200, safe=False)
            else:
                return JsonResponse({"error": "There are no logs associated with the consignment"}, status=404)
            
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
