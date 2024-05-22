# myproject/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

class ApiRoot(APIView):
    """
    API root view.
    """

    def get(self, request, format=None):

        return Response({
        'obtain token': reverse('token_obtain_pair', request=request, format=format),
        'refresh token': reverse('token_refresh', request=request, format=format),
        # Add more endpoints here
        })




