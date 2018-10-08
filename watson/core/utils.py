from django.utils.text import slugify


def get_slug(queryset, slug, slug_attr='slug', postfix=None):
    # Add a prefix to slug to make sure uniqness.
    slug_base = slugify(slug)
    if postfix is None:
        postfix_str = ''
    else:
        postfix_str = str(postfix)
    slug_str = f'{slug_base}{postfix_str}'

    if queryset.filter(**{slug_attr: slug_str}).exists():
        if postfix is None:
            postfix = 1
        else:
            postfix = postfix + 1
        return get_slug(queryset, slug, slug_attr, postfix)
    else:
        return slug_str
