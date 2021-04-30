from django import template

register = template.Library()


@register.filter
def non_breaking_hyphen(value):
    return value.replace("-", u"\u2011")
