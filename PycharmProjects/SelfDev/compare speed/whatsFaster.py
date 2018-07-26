import timeit


if __name__ == "__main__":
    with open("1.py", 'r') as f:
        code1 = ''.join(f.readlines())
        f.close()
    with open("2.py", 'r') as f:
        code2 = ''.join(f.readlines())
        f.close()

    codes = {0: code1,
             1: code2}

    for code in codes:
        print(timeit.timeit(setup=codes[code], number=10000000))
