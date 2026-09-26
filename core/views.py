from django.http import JsonResponse
from django.utils import timezone


def api_status(request):
    return JsonResponse({"status": "ok", "time": timezone.now().isoformat()})
