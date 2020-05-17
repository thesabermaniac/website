from django import template
register = template.Library()


@register.filter
def verbose_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name.title()


@register.filter
def verbose_name_plural(obj):
    return obj.verbose_name_plural
