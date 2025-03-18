import logging
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler that logs errors without traceback.
    """
    response = exception_handler(exc, context)

    view_name = context['view'].__class__.__name__
    view_module = context['view'].__class__.__module__

    if response is not None:
        error_details = response.data if isinstance(response.data, dict) else str(response.data)
        logger.error(f"Error in {view_module}.{view_name}: {error_details}")

    return response
