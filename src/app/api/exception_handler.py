from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """Custom DRF exception handler that returns a consistent JSON structure.

    Returns:
        Response: JSON with keys `status`, `message` and optional `details`.
    """
    # First, let DRF handle the exception to get the standard error response
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Build a normalized response
        data = {
            "status": "error",
            "message": None,
        }
        # Use DRF's response data to fill message/details
        if isinstance(response.data, dict):
            # Try to extract a readable message
            message = response.data.get('detail') or response.data
            data["message"] = message
            # include full details for validation errors
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                data["details"] = response.data
        else:
            data["message"] = response.data

        return Response(data, status=response.status_code)

    # Non-DRF exceptions — return generic 500 JSON
    return Response({"status": "error", "message": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
