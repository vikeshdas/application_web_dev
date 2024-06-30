"""
    File contains view to handle operation releted to consignments
    like insert new consignment,get information of consignment and 
    get all logs of a consignment.
"""

import json
from timbba.models import User, Client, Consignment
from django.http import JsonResponse,HttpRequest
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class that extends the PageNumberPagination
    provided by Django REST Framework.

    This pagination class initialize some vlues for pagination:
    - Default page size of 2.
    - Allows clients to specify the page size via the 'page_size' query parameter.
    - Restricts the maximum page size that can be requested to 100.

    Attributes:
        page_size (int): The default number of items to include
        in each page. page_size_query_param (str): The name of
        the query parameter that allows clients to set the page
        size.max_page_size (int): The maximum number of items
        allowed in each page
    """

    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100


class ConsignmentView(APIView):
    """
    View for handling consignment related operations.Consignment is a excel file that
    contains information of logs with its dimensions and vehicle number in which these
    logs comes to factory . Same excel file will be inserted in to database. So this
    class helps to insert consignment information in the database.

    """

    permission_classes = [IsAuthenticated]

    def put(self, request: HttpRequest) -> JsonResponse:
        """
        Create a new consignment. Add information of consignment
        like vehicle number,consignment name,
        with client information,user in information who inserts
        these information using my application.

        Args:
            request:HTTP's request object contains information of a consignment

        Return:
            JsonResponse: success or fail in JSON form
        """
        data = json.loads(request.body)

        try:
            try:
                client = Client.objects.get(id=data.get("client_id"))
            except Client.DoesNotExist:
                return JsonResponse({"error": "client_id does not exist"}, status=404)
            try:
                user = User.objects.get(id=data.get("user_id"))
            except User.DoesNotExist:
                return JsonResponse({"error": "user_id does not exist"}, status=404)
            duplicate_consignment = (
                Consignment.objects.filter(client_id=client)
                .filter(created_by=user)
                .filter(name=data.get("name"))
            )
            if not duplicate_consignment.exists():
                consignment = Consignment(
                    name=data.get("name"),
                    type=data.get("type"),
                    client_id=client,
                    created_by=user,
                    updated_by=user,
                )
                consignment.save()
                serialize_data = consignment.con_serializer()
                return JsonResponse(
                    {
                        "message": "Consignment created successfully",
                        "data": serialize_data,
                    },
                    status=201,
                )
            return JsonResponse(
                    {"message": "Consignment allredy exist"}, status=409
                )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Fetch details of a consignment from the database by Id.

        Args:
            request : The object of HttpRequest contains consignment Id.

        Returns:
            JsonResponse: Details of a consignment.if Id not found in
            database return a error message.
        """
        cons_id = request.GET.get("con_id")
        cache_key = f"consignment_data_{cons_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            response_data = cached_data
            response_data["message"] = "Data retrieved from cache"
            return JsonResponse(response_data, status=200)

        try:
            consignment = Consignment.objects.get(id=cons_id)
        except Consignment.DoesNotExist:
            return JsonResponse(
                {"error": "Consignment with this id not found"}, status=404
            )

        serialized_data = consignment.con_serializer()
        cache.set(cache_key, serialized_data, timeout=300)
        return JsonResponse(serialized_data, status=201)


class Consignments(APIView):
    """
    Handles operations related to more than one consignment.
    like fetching all consignments information related of a client.

    Method:
        get(self,request): Fetch all consignments of a particular client.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Retrieve information of all consignments of a particular client.

        Args:
           request (HttpRequest): object of HttpRequest contains client Id.

        Returns:
            JsonResponse: returns list of consignments of a particular client in JSON format.
        """
        client_id = request.GET.get("client_id")
        cache_key = f"consignments_data_{client_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            response_data = cached_data
            response_data["message"] = "Data retrieved from cache"
            return JsonResponse(response_data, status=200)

        try:
            Client.objects.get(id=client_id)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)

        try:
            consignments = Consignment.objects.filter(client_id=client_id)
            paginator = CustomPagination()
            paginated_consignment = paginator.paginate_queryset(consignments, request)

            serialized_data = [cons.con_serializer() for cons in paginated_consignment]
            return paginator.get_paginated_response(serialized_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
