class RunMathematic:
    def plus(a,b):
        return a + b

    def kurang(a,b):
        return a - b
    
    def kali(a,b):
        return a * b

    def bagi(a,b):
        return a / b

    def luasPersegi(s):
        return s*s

res = RunMathematic.luasPersegi(9)
print(res)