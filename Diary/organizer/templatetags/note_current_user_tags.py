from django import template
import calendar

register = template.Library()


@register.simple_tag
def define(val=None):
    return val


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
