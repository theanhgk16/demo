from django import template

register = template.Library()

@register.filter
def replace_comma_with_dot(value):

    # Chuyển Decimal thành chuỗi và thực hiện thay thế dấu phẩy bằng dấu chấm
    value_str = str(value)
    return value_str.replace(',', '.')
