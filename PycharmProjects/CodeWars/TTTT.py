roman={"MDCLXVI"[i]:[1000,500,100,50,10,5,1][i] for i in range(len("MDCLXVI"))}
x=roman.copy()
x["M"]=1
print(roman)