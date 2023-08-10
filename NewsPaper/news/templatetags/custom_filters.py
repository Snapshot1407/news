from pprint import pprint

from django import template

register = template.Library()


censor_list = ["идиот","дурак", "самодур", "кракзябра"]

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter(name="censor")
def currency(value):
   s = ''
   for w in value:
      if w != " ":
         s += w
      else:
         if s.lower() in censor_list:
            s = s[0] + '*'*len(s) + " "
         else:
            s += ' '

   return f'{s}'