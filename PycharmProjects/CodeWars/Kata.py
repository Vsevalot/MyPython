def permutations(string:str)->list:
    if len(string) == 1:
        return [string]
    if len(string)==2:
        return list({string,string[1]+string[0]})
    return list(set(sum([[ string[i] + combination for combination in permutations(string[:i]+string[i+1:])] for i in range(len(string))],[])))


a="11"

print(permutations(a))