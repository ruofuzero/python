#coding=utf-8
import MySQLdb
import xlwt
import xlrd
import random
import csv
line1=['a']
s=[]
lines=[]
conn=MySQLdb.connect(host='localhost',user='root',passwd='love539392',port=3306)
cur=conn.cursor()     #设置游标
conn.select_db('njusearch')        #选择数据库
cur.execute('select * from id_url')
for url in cur.fetchall():
    s.append(url[0])
    # if url[0] not in s:
    #     s.append(url[0])
    # if url[1] not in s:
    #     s.append(url[1])
#s.remove('a')
line1.extend(s)
lines.append(line1)
length=len(s)
cur.execute('select * from gather')
result=cur.fetchall()
print length
for url in s:
    print url
    line=[]
    line.append(url)
    num=0

    while num<length:
        if (s[num],url) in result:
            line.append(1)

        else:
            line.append(0)

        num=num+1
    lines.append(line)

# w=xlwt.Workbook()
# sheet=w.add_sheet("my_sheet")
# for row in range(0,10):
#     for col in range(0,10):
#         sheet.write(row,col,random.randrange(0,10))
#sheet.write(0,,'a')
writer = csv.writer(file('gather_new.csv', 'wb'))

for line in lines:
    writer.writerow(line)
# for url in s:
#     sheet.write(n,0,url)
#     sheet.write(0,n,url)
#     n+=1
#w.save("www.xls")
