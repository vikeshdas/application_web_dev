"""
    File contains view to handle operation  to create new client client
"""

import json
from datetime import datetime
from django.http import JsonResponse,HttpRequest
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from timbba.models import Client


class ClientView(APIView):
    """
    A view for handling client related operation like creating a new client.
    A client is a admin who buys subscription for our application or we can
    say that client is a owner of a factory who makes logs to plyboard.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request: HttpRequest) -> JsonResponse:
        """
        Create a new client.This function will be required when a client buys subscription.
        When client signup then this function will be executing.

        Args:
            HttpRequest :Contains client data in request body.

        Returns:
            JsonResponse:return JSON, that client is created successfully.
        """
        data = json.loads(request.body)

        try:
            duplicate_client = Client.objects.filter(contact=data.get("contact"))
            if duplicate_client:
                return JsonResponse({"error": "Client already exists"}, status=400)
            client = Client(
                name=data.get("name"),
                address=data.get("address"),
                contact=data.get("contact"),
                updated_at=datetime.now(),
                created_at=datetime.now(),
                email=data.get("email"),
            )
            client.save()
            serialized_data = client.client_serializer()
            return JsonResponse(
                {"message": "Client created successfully", "data": serialized_data},
                status=201,
                safe=False,
            )

        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return JsonResponse({"error": "Client already exists"}, status=409)
            return JsonResponse({"error": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
