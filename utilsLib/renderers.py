from rest_framework.renderers import JSONRenderer
from rest_framework.status import is_success, is_client_error, is_server_error
from rest_framework.response import Response

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response", None)

        status_code = response.status_code if response else 200

        # Determine status message
        if is_success(status_code):
            status_text = "success"
        elif is_client_error(status_code):
            status_text = "error"
        elif is_server_error(status_code):
            status_text = "fail"
        else:
            status_text = "unknown"

        # Extract message
        message = None
        if isinstance(data, dict) and "message" in data:
            message = data.pop("message")

        custom_response = {
            "status_code": status_code,
            "status": status_text,
            "message": message or response.status_text,
            "data": data if data else None,
        }

        return super().render(custom_response, accepted_media_type, renderer_context)
