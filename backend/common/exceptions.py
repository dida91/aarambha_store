from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from common.response import build_envelope


def enveloped_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return Response(
            build_envelope(
                success=False,
                message="Internal server error",
                data=None,
                errors={"detail": ["An unexpected error occurred."]},
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        build_envelope(
            success=False,
            message="Request failed",
            data=None,
            errors=response.data,
        ),
        status=response.status_code,
    )
