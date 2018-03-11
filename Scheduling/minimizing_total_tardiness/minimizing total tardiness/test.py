# i=1

# locals()['a'+str(i)] = []
# locals()['a'+str(i)].append('a')
# print ( locals()['a'+str(i)])
# a=['a','b']
# c = 'c'
# b=['d','e']
# d= []
# d.append(a+list(c)+b)
# print (d)
d = [[]]
print (d)
if d[0] == []:
	print ('yes')

a = [1,2,3,4]
# s = a.pop(a.index(min(a)))
# print(s)
while a:
	
	b=a.pop(0)
	print (b)
		
print (a)