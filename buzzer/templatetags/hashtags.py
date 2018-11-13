from django import template
register = template.Library()

@register.filter
def lista_hash(value):
    value = str(value)
    dict_text = value.split()
    #print(dict_text)
    return dict_text