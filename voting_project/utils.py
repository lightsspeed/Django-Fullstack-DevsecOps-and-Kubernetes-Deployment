import random
import string
from django.utils.text import slugify


def generate_unique_slug(model_instance, title, slug_field_name="slug"):
    slug = slugify(title)
    model_class = model_instance.__class__

    # Check if slug already exists
    extension = ""
    while True:
        potential_slug = f"{slug}{extension}"
        # Filter by slug, but exclude current instance if it has a PK (for updates)
        queryset = model_class.objects.filter(**{slug_field_name: potential_slug})
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        if not queryset.exists():
            return potential_slug

        # If exists, add/change extension
        extension = f"-{random_string(4)}"


def random_string(length=4):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
