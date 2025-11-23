while True:
    age = int(input('Please type in your age: '))
    if age <= 0 or age >= 200:
        raise ValueError('Tuổi không hợp lệ')
    else:
        print('tuổi bạn là: ', age)
    