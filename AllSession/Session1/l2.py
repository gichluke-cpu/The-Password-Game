def calculate_sum(numbers):
        #Debugging starts he

        print("Debugging: số=", numbers)

        total = 0

        for num in numbers:

            print("Debugging: Cộng", num, "vào tổng")

            total += num

            print("Debugging: Tổng cộng là =", total)

            #Debugging ends here

        return total

3

def main():
    numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(numbers)

    print("Sum:", result)

main()