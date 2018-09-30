from core import constants
from rest_framework import viewsets
from rest_framework.response import Response
from dataclasses import asdict

CONSTANTS = {
    'devices': [asdict(d) for d in constants.device_list],
}


class ConstantsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = ()

    def list(self, request):
        return Response(CONSTANTS)
