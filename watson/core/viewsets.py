from core import constants
from rest_framework import viewsets
from rest_framework.response import Response
from dataclasses import asdict

devices = []

for d in (asdict(d) for d in constants.device_list):
    d = d.copy()
    d['backend'] = d['backend'].value
    devices.append(d)

CONSTANTS = {
    'devices': devices,
}


class ConstantsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = ()

    def list(self, request):
        return Response(CONSTANTS)
