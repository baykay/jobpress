from django.utils.text import slugify


def slug_generator(model_instance, title, slug):
    slug = slugify(title)
    model_class = model_instance.__class__
    while model_class._default_manager.filter(slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        new_object_pk = object_pk.pk + 1
        slug = f'{slug}-{new_object_pk}'
    return slug
