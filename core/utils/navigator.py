from django.http import JsonResponse
from django.apps import apps

def navigate_record(request):
    direction = request.POST.get('direction')
    model_name = request.POST.get('model_name')
    current_record_id = request.POST.get('current_record_id')

    # Get the model class dynamically based on the provided model name
    Model = apps.get_model(app_label='your_app_label', model_name=model_name)

    # Retrieve the next or previous record based on the provided information
    if direction == 'next':
        next_record = Model.objects.filter(id__gt=current_record_id).order_by('id').first()
        if next_record:
            data = {
                'title': next_record.title,
                'description': next_record.description,
            }
        else:
            data = None
    elif direction == 'previous':
        previous_record = Model.objects.filter(id__lt=current_record_id).order_by('-id').first()
        if previous_record:
            data = {
                'title': previous_record.title,
                'description': previous_record.description,
            }
        else:
            data = None

    return JsonResponse(data)
