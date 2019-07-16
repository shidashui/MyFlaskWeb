print(__name__.split('.')[0])
print(__file__)


a = '1.2.3.4'
b = a.split('.')
c = ''
d = c.join(b)
print(d)


a = '1010'
b = '10'
d = len(b)-len(a)
a = '0'*d +a
b = '0'* -d +b
print(zip(a,b))
for i,j in zip(a,b):
    print(i)

print(a)
print(b)
print(d)