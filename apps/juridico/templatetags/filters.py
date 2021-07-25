from django import template

register = template.Library()


@register.filter()
def soma(val1, val2):
    return 'R$ ' + str(val1 * val2)
