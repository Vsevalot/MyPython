def first_non_repeating_letter(string: str)->str:
    alphNumber=[]
    for i in range(26):
        alphNumber.append(ord('A')+i)

    case=ord('a')-ord('A')
    for letter in string:
        if (ord(letter) in alphNumber) or ((ord(letter)-case) in alphNumber):
            alphNumber.remove()
