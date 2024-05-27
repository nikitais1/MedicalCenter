from django import template

register = template.Library()


@register.filter()
def category_image(val):
    if val:
        return f'/media/{val}'

    return '#'
