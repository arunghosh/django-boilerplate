from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


def handle_object_not_exist(vfunc):
    def _inner(request, *args, **kwargs):
        try:
            result = vfunc(request, *args, **kwargs)
            return result
        except ObjectDoesNotExist:
            raise Http404
    return _inner
