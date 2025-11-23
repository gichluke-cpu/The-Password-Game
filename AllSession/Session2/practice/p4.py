import re

pattern = r'^(0[1-9]|[12][0-9]|3[01])/' \
              r'(0[1-9]|1[0-2])/' \
              r'(19[0-9]{2}|20[0-9]{2})$'

date_list = ['28/09/2025', '31/04/2025', '99/99/9999']


valid_dates = [d for d in date_list if re.fullmatch(pattern, d)]


valid_dates.sort()

print('All the valid dates are: ', valid_dates)