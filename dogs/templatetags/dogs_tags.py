from django import template

register = template.Library()


@register.filter
def get_years_string(age):
    """Возвращает правильную форму слова 'год' в зависимости от возраста."""
    if age is None or age < 0:
        return "лет"

    age = int(age)
    remainder = age % 10
    remainder_100 = age % 100

    if remainder == 1 and remainder_100 != 11:
        return "год"
    elif remainder in (2, 3, 4) and remainder_100 not in (12, 13, 14):
        return "года"
    else:
        return "лет"
