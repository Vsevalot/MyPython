def factorial(x):
    if x == 0 or x == 1:
        return 1
    return x * factorial(x-1)


if __name__ == "__main__":
    print("Hello, this script calculates the value of e.")
    n = input("How much digits after comma do you want?\nNumber of digits: ")
    digits = [str(i) for i in range(10)]
    for char in n:
        if char not in digits:
            print("Wrong input, you should use only digits!")
            exit(1)
    n = int(n)

    limit = 1000
    i = 1
    current_e = 1.
    previous_e = .0
    while i < limit:
        previous_e = current_e
        current_e += 1/factorial(i)
        if format(current_e, ".%df" % n) == format(previous_e, ".%df" % n):
            print("The value of the e to the {} digit is {}".format(n, format(current_e, '.{}f'.format(n))))
            exit(0)
        i += 1
    print("Can't calculate value of the e to the {} digit because of the limit of the script. "
          "The most accurate result is {}".format(n, format(current_e, '.{}f'.format(n))))
