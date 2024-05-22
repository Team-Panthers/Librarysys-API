from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class IncrementingField(models.PositiveIntegerField):

    def __init__(self, by_fields=None, *args, **kwargs):
        self.by_fields = by_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.by_fields:
                    query = {field: getattr(model_instance, field) for field in self.by_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                value = 1
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
