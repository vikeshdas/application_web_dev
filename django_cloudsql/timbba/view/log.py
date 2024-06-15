from timbba.models import Consignment,Item
from django.views import View 
import json
from django.http import JsonResponse



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
        data = json.loads(request.body)

        try:
            Consignment.objects.get(id=data.get("con_id"))
        except Exception as e:
            return JsonResponse({'error':'Consignment with this id does not exist'}, status=404)
        
        duplicate_log=Item.objects.filter(barcode=data.get('barcode'))
        print("duplicate_log",duplicate_log)
        # if duplicate_log.exists():
        #     return JsonResponse({'error':'Log with this barcode allredy exist'}, status=404)

        try:
            consignmentObj=Consignment.objects.get(id=data.get("con_id"))
            log = Item(consignment=consignmentObj,barcode=data.get('barcode'),length=data.get('length'),volume=data.get('volume'))
            log.save()
            serialized_data = log.log_serializer()
            return JsonResponse({'message': 'log inserted successfully', 'data': serialized_data}, status=201)
        
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
            log = Item.objects.get(id=log_id)
            serializer_data = log.log_serializer()
            return JsonResponse(serializer_data,status=201)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'log with this id not found'}, status=404)
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
        data = json.loads(request.body)
        consignment_id = data.get('con_id')
        consignment_exist=Consignment.objects.filter(id=consignment_id)
        if not consignment_exist:
            return JsonResponse({'error':'Consignment with this id does not exist'}, status=404)
        try:
            logs = Item.objects.filter(consignment=consignment_id)
            serialized_data = [log.log_serializer() for log in logs]
            return JsonResponse(serialized_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        