from django import template

register = template.Library()


@register.filter
def my_thousand_separator(value):
    after_point = str(round(value % 1, 2))
    value = str(int(value))
    result = []
    while len(value) >= 4:
        result.append(str(value[-1:-4:-1])[::-1])
        value = str(int(value)//1000)
    result.append(value)
    res = f"{' '.join(result[::-1])} руб. {after_point[2:]} коп."
    return res

