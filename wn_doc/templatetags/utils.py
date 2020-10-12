from django import template
import datetime


register = template.Library()


@register.filter(name='lookup')
def lookup(value, arg, default=''):
    if arg in value:
        return value[arg]
    else:
        return default


@register.filter(name="calc_age")
def calc_age(value, default=''):
    today = datetime.date.today()
    birthday = datetime.datetime.strptime(value, '%Y-%m-%d').date()
    age = today.year - birthday.year
    # 誕生日を迎えていなかったら-1歳する
    if (today.month - birthday.month <= 0) and (today.day - birthday.day < 0):
        age -= 1

    return {'age': age, 'birthday': birthday}
