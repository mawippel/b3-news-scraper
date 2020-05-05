import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

datetime_object = datetime.strptime('5 maio 2020, 14h21', '%d %B %Y, %Hh%M')
print(datetime_object)