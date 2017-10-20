class RomanNumerals():
    roman={"MDCLXVI"[i]:[1000,500,100,50,10,5,1][i] for i in range(len("MDCLXVI"))}

    def to_roman(self,arNum:int)->str:
        currentRoman={char:0 for char in "MDCLXVI"}

        while(arNum!=0):
            for i in range(len("MDCLXVI")):
                if RomanNumerals.roman["MDCLXVI"[i]]>arNum:

