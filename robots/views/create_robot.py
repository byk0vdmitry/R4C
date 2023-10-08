import json
from django.forms import ValidationError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot


@csrf_exempt
def create_robot(request):
    """
    Create a robot based on the provided data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: The JSON response indicating the success or error message.
    """
    if request.method == 'POST':
        data_list = ['model', 'version', 'created']
        data = json.loads(request.body)
        if data_list == list(data.keys()):
            try:
                # Create a new Robot object with the provided data
                Robot.objects.create(
                    serial=f"{data['model']}-{data['version']}",
                    model=data['model'],
                    version=data['version'],
                    created=data['created']
                )
                return JsonResponse({'success': 'Robot created'})
            except ValidationError as error:
                # Return an error response if there is a validation error
                return JsonResponse({'error': f"Validation error: {error}"}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request data'}, status=400)
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'})
