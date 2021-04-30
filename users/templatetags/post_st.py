from django import template

from users.models import Fraction

register = template.Library()


@register.inclusion_tag('users/profile/groups.html')
def fractions_list():
    fractions = Fraction.objects.filter(show_in_list=True).order_by("-power")
    return {'fractions': fractions}
