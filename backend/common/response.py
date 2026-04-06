from rest_framework import status
from rest_framework.response import Response


def api_response(*, success=True, message='Request successful.', data=None, errors=None, http_status=status.HTTP_200_OK):
    return Response(
        {
            'success': success,
            'message': message,
            'data': data,
            'errors': errors,
        },
        status=http_status,
    )
