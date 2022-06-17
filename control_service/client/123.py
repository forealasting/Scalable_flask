r = 10


x = []
d = 1/r
count = 0
j = 300*r
for i in range(j):
    x.append(count)
    count += d
print(x)