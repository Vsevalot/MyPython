def toJadenCase(string):
    preparingString=string.title()
    jString=''
    k=0
    while(1):
        while(1):
            if (k >= len(string)):
                break
            if(preparingString[k]=="'"):
                break
            jString += preparingString[k]
            k+=1
        if(k>=len(string)):
            break
        jString += string[k] + string[k + 1]
        k += 2
    return jString

print("Hello world")
quote = "How can mirrors be real if our eyes aren't real"
print(toJadenCase(quote))