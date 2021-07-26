
from rest_framework import response
from rest_framework.decorators import action
# Create your views here.


class GetChoices:
    def add_choices_annotations(self, queryset):  # pragma: no cover
        return queryset

    def get_choices_queryset(self):
        return self.filter_queryset(self.get_queryset())

    def get_choices_values(self):
        qs = self.add_choices_annotations(self.get_choices_queryset())
        return qs.values('nazwa', 'id')

    @action(methods=['get'], url_path='choices', url_name='choices', detail=False)
    def get_choices(self, request, *args, **kwargs):
        return response.Response(data=self.get_choices_values())
