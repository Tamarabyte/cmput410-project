from django.http import HttpResponse

def home(request):
    """ Handles the home URL """
    html = "<html><body>Server is Working! - Hindlebook!</body></html>"

    # Should use render() with a template in the future
    return HttpResponse(html)