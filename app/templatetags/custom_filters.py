from django import template

register = template.Library()

@register.filter
def initials(username):
    if len(username) > 1:
        return f"{username[0]}****{username[-1]}"
    return username

@register.filter
def modulo(value, arg):
    return value % arg