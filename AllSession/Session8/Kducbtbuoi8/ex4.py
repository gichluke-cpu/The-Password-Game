print('Chương trình tính tuổi')
import datetime
while True:
    age = int(input('nhập tuổi: '))
    time = datetime.date.today().year
    birthyear = time - age
    if age <= 0 or age >= 200:
        raise ValueError('Tuổi không hợp lệ')
    else:
        print('tuổi bạn là: ', age, 'Bạn sinh năm: ', birthyear)