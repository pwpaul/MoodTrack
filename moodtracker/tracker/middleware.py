class HTMXMiddleware:
    """
    Middleware to add an `htmx` attribute to the request object.
    This checks if the request is an HTMX request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is an HTMX request based on headers
        request.htmx = request.headers.get("HX-Request") == "true"
        response = self.get_response(request)
        return response
