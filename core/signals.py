from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Library, Rack 


@receiver(post_save, sender=Library)
def create_racks(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.no_of_rack + 1):
            Rack.objects.create(library=instance, rack_number=i)