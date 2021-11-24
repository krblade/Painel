from django import template
import locale

from decimal import Decimal
#########################################################
## Filtro para definir o padrão de moeda local direto no Template

register = template.Library()
@register.filter(name='currency')
def currency(value):    
        try:    
            locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')    
        except:    
            locale.setlocale(locale.LC_ALL,'')    
        value = Decimal(value)    
        loc = locale.localeconv()    
        return locale.currency(value, loc['currency_symbol'], grouping=True)


        