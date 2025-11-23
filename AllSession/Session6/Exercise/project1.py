from datetime import datetime


time_now = datetime.now()
print(time_now)
holiday = datetime(2026, 1, 1)

remaining = holiday - time_now
print("There are", remaining.days, 'days left until tet holiday')
print("and there are", remaining.seconds//3600, 'hours left until the day ends')


