from django import template
from django.conf import settings

register = template.Library()


@register.filter
def verbose_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name.title()


@register.filter
def verbose_name_plural(obj):
    return obj.verbose_name_plural


@register.filter
def fTotal(stat, context):
    return context["fTotal_" + stat.player.get_operable_string() + "_" + str(stat.year)]


@register.filter
def get_class_name(obj):
    return obj.__class__.__name__


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.filter
def multiply(a, b):
    return a * b


@register.filter
def divide(a, b):
    return a/b


@register.filter
def get_stat(obj, value):
    return getattr(obj, value)


@register.filter
def get_fstat(obj, value):
    return getattr(obj, "f" + value)
