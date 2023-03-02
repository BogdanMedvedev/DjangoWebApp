a = [1,2,3,4,5,6,7,8]

for i in a:
    isinstance(i, int)
    if a.index(i)//2==1:
        print (f'{i} Привет')