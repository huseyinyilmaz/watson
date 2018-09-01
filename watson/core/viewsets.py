from core import constants
from rest_framework import viewsets
from rest_framework.response import Response
from dataclasses import asdict

CONSTANTS = {
    'dimensions': [asdict(d) for d in constants.dimensions_list],
    'browsers': [{'name': b.name, 'value': b.value} for b in constants.Browser]
}


class ConstantsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        return Response(CONSTANTS)
