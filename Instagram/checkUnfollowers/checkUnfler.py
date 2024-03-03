listFler = open("flers.dat")
listFling = open("fling.dat")
fileEr = set(i for i in listFler.readlines())
fileIng = set(i for i in listFling.readlines())
er = []
ing = []

for i in fileEr:
    if i.islower(): 
        er += [i]
er.sort()
for i in fileIng:
    if i.islower(): 
        ing += [i]
ing.sort()
dem = 0
for i in er:
    if not i in ing: 
        print(i)
        dem += 1
print("Number of unfollowing-you accounts:", dem)