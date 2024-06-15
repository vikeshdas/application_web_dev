from timbba.models import User,Client,Consignment
from django.views import View 
import json
from django.http import JsonResponse


class ConsignmentView(View):
    """
        View for handling consignment related operations.Consignment is a excel file that 
        contains information of logs with its dimensions and vehicle number in which these 
        logs comes to factory . Same excel file will be inserted in to database. So this
        class helps to insert consignment information in the database.

    """
    def put(self, request):
        """
            Create a new consignment. Add information of consignment like vehicle number,consignment name,
            with client information,user in information who inserts these information using my application.

            Args: 
                request:HTTP's request object contains information of a consignment
            
            Return:
                JsonResponse: success or fail in JSON form
        """
        data = json.loads(request.body)

        try:
            try:
                client = Client.objects.get(id=data.get('client_id'))
            except Client.DoesNotExist:
                return JsonResponse({"error": "client_id does not exist"}, status=404)
            try:
                user = User.objects.get(id=data.get('user_id'))
            except User.DoesNotExist:
                return JsonResponse({"error": "user_id does not exist"}, status=404)
            duplicate_consignment=Consignment.objects.filter(client_id=client).filter(created_by=user).filter(name=data.get('name'))
            if not duplicate_consignment.exists():
                consignment = Consignment(name=data.get('name'),type=data.get('type'),client_id=client,created_by=user,updated_by=user)
                consignment.save()
                serialize_data=consignment.con_serializer()
                return JsonResponse({'message': 'Consignment created successfully', 'data': serialize_data}, status=201)
            else:
                return JsonResponse({'message': 'Consignment allredy exist'}, status=409)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        """
            Fetch details of a consignment from the database by Id.

            Args: 
                request : The object of HttpRequest contains consignment Id.
            
            Returns:
                JsonResponse: Details of a consignment.if Id not found in database return a error message.
        """
        data = json.loads(request.body)
        cons_id = data.get('con_id')
        try:
            consignment = Consignment.objects.get(id=cons_id)
        except Consignment.DoesNotExist:
            return JsonResponse({'error': 'Consignment with this id not found'}, status=404)
        
        serialized_data = consignment.con_serializer() 
        return JsonResponse(serialized_data,status=201)
    
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
        data = json.loads(request.body)
        client_id = data.get('client_id')
        try:
            client_exist=Client.objects.get(id=client_id)
        except Exception as e:
            return JsonResponse({'error': 'Client not found with this id'}, status=404)
    
        consignments = Consignment.objects.filter(client_id=client_id)
        serialized_data = [cons.con_serializer() for cons in consignments]
        return JsonResponse({"consignments":serialized_data}, status=200)