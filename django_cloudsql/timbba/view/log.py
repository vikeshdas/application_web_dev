"""
    View to handle log releted operation like create log,
    get information of a log and list logs of a consignment.
"""

import json
from timbba.models import Consignment, Item
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpRequest
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.views import APIView


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class that extends the PageNumberPagination provided by Django REST Framework.

    This pagination class initialize some vlues for pagination:
    - Default page size of 2.
    - Allows clients to specify the page size via the 'page_size' query parameter.
    - Restricts the maximum page size that can be requested to 100.

    Attributes:
    page_size (int): The default number of items to include in each page.
    page_size_query_param (str): The name of the query parameter that
    allows clients to set the page size.max_page_size (int):
    The maximum number of items allowed in each page
    """

    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100


class Log(APIView):
    """
    Handling log related operations like inserting log
    information(create log),fetch information of a log.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request: HttpRequest) -> JsonResponse:
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
            return JsonResponse({"error": str(e)}, status=404)

        duplicate_log = Item.objects.filter(barcode=data.get("barcode"))
        if duplicate_log.exists():
            return JsonResponse(
                {"error": "Log with this barcode allredy exist"}, status=404
            )

        try:
            consignment_obj = Consignment.objects.get(id=data.get("con_id"))
            log = Item(
                consignment=consignment_obj,
                barcode=data.get("barcode"),
                length=data.get("length"),
                volume=data.get("volume"),
            )
            log.save()
            serialized_data = log.log_serializer()
            return JsonResponse(
                {"message": "log inserted successfully", "data": serialized_data},
                status=201,
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Fetch information of a log from database using log id.

        Args:
            request(HttpRequest): HttpRequest object contains log id.

        Response(HttpResponse):Return information of a log in the JSON format or error.
        """
        log_id = request.GET.get("id")
        cache_key = f"log_data_{log_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            response_data = cached_data
            response_data["message"] = "Data retrieved from cache"
            return JsonResponse(response_data, status=200)

        try:
            log = Item.objects.get(id=log_id)
            serializer_data = log.log_serializer()
            cache.set(cache_key, serializer_data, timeout=300)
            return JsonResponse(serializer_data, status=201)
        except Item.DoesNotExist:
            return JsonResponse({"error": "log with this id not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class Logs(APIView):
    """
    View class to Handle operations related to more than one log for example
    get all logs of a consignment.

    """

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Get information of all logs related to a consignment.

        Args:
            request(HttpRequest):object of HttpRequest contains consignment_id.

        Response:
            JsonResponse: return information of all logs related to a consignment in JSON format.
        """
        consignment_id = request.GET.get("con_id")
        cache_key = f"logs_data_{consignment_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            response_data = cached_data
            response_data["message"] = "Data retrieved from cache"
            return JsonResponse(response_data, status=200)

        consignment_exist = Consignment.objects.filter(id=consignment_id)
        if not consignment_exist:
            return JsonResponse(
                {"error": "Consignment with this id does not exist"}, status=404
            )
        try:
            logs = Item.objects.filter(consignment=consignment_id)
            paginator = CustomPagination()
            paginated_logs = paginator.paginate_queryset(logs, request)

            serialized_data = [log.log_serializer() for log in paginated_logs]
            cache.set(cache_key, serialized_data, timeout=300)
            return paginator.get_paginated_response(serialized_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
