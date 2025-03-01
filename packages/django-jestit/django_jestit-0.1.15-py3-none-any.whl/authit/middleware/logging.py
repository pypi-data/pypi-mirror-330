from jestit.models import JestitLog


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Only log if the endpoint starts with '/api'
        if request.path.startswith('/api'):
            # Log Request and Response details with data
            JestitLog.logit(request, request.body, "api_request")
            JestitLog.logit(request, response.content, "api_response")
        return response
