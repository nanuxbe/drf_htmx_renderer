from rest_framework.response import Response
from htmx_renderer.views import ModelViewSet


class DebugViewSet(ModelViewSet):
    def update(self, request, *args, **kwargs):
       partial = kwargs.pop('partial', False)
       instance = self.get_object()
       serializer = self.get_serializer(instance, data=request.data, partial=partial)
       serializer.is_valid(raise_exception=True)
       print(serializer.validated_data)
       self.perform_update(serializer)

       if getattr(instance, '_prefetched_objects_cache', None):
           # If 'prefetch_related' has been applied to a queryset, we need to
           # forcibly invalidate the prefetch cache on the instance.
           instance._prefetched_objects_cache = {}

       return Response(serializer.data)
