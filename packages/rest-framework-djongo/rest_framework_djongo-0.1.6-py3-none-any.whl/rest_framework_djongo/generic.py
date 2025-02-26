from bson import ObjectId
from rest_framework import generics as drf_generics
from rest_framework.generics import get_object_or_404


class DjongoSearchMixin:
    lookup_field = 'pk'
    lookup_field_class = ObjectId

    def get_object(self):
        ""
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        if hasattr(self,'lookup_field_class'):
            filter_kwargs[self.lookup_field] = self.lookup_field_class(filter_kwargs[self.lookup_field])
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj
