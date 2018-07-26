if __name__ == "__main__":
    print("Hello, this script calculates the value of pi.")
    n = input("How much digits after comma do you want?\nNumber of digits: ")
    digits = [str(i) for i in range(10)]
    for char in n:
        if char not in digits:
            print("Wrong input, you should use only digits!")
            exit(1)
    n = int(n)

    limit = 10000000
    i = 0
    current_pi = 0
    previous_pi = 0
    while i < limit:
        previous_pi = current_pi
        if i % 2 == 0:
            current_pi += 4 / (2 * i + 1)
        else:
            current_pi -= 4 / (2 * i + 1)
        if format(current_pi, ".%df" % n) == format(previous_pi, ".%df" % n):
            print("The value of the pi to the {} digit is {}".format(n, format(current_pi, '.{}f'.format(n))))
            exit(0)
        i += 1
    print("Can't calculate value of the pi to the {} digit because of the limit of the script. "
          "The most accurate result is {}".format(n, format(current_pi, '.{}f'.format(n))))
