class A:
    a = [1,2,3]
    b = [4,5,6]
    c = [7,8,9]


print(A.a)
print(A.b)
print(A.c)

for i in [A.a, A.b, A.c]:
    print(i)