from django.http import Http404, JsonResponse

from .models import Enrollment


def summary(request, ref):
    try:
        obj = Enrollment.objects.get(ref=ref)
    except Enrollment.DoesNotExist:
        raise Http404
    return JsonResponse({"ref": obj.ref, "amount_cents": obj.amount_cents, "status": obj.status})
