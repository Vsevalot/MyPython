def next_bigger(number):
    import itertools
    i_n=[x for x in list(str(number))]
    if len(i_n)==1:
        return -1
    for i in range(len(i_n)-2,-1,-1):
        first = ''.join([v for v in i_n[:i]])
        seconds = sorted([int(''.join([str(n) for n in v ])) for v in itertools.permutations(i_n[i:],len(i_n[i:]))])
        seconds.reverse()
        second = 0
        if int(''.join(i_n[i:]))<seconds[0]:
            for k in range(len(seconds)):
                if seconds[k]==int(''.join(i_n[i:])):
                    second = seconds[k-1]
                    break
        if second:
            return int(first + str(second))
    return -1



print(next_bigger(144))
