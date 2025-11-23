def calculate_average(numbers):

    assert len (numbers) > 0, "Danh sách không được để trống"

    assert all(isinstance(num, (int, float)) for num in numbers),     "Danh sách phải chửa số"

    total = sum(numbers)

    average = total / len(numbers)

    return average

def main():

    raw = input("Nhập một danh sách số, cách nhau bằng dấu phẩy: ")

    numbers = [float(x) for x in raw.split(',')] # chuyển từng phần từ thành số



    result = calculate_average(numbers)

    print("Trung bình:", result)

main()
