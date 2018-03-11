#coding=utf-8
import numpy as np
import xlrd
import xlwt
from xlutils.copy import copy
#N = 8           #八个网页
d = 0.85        #阻尼因子为0.85
delt = 0.00001  #迭代控制变量
#两个矩阵相乘
def matrix_multi(A,B):
    result = [[0]*len(B[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k]*B[k][j]
    return result

#矩阵A的每个元素都乘以n
def matrix_multiN(n,A):
    result = [[1]*len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = n*A[i][j]
    return result

#两个矩阵相加
def matrix_add(A,B):
    if len(A[0])!=len(B[0]) and len(A)!=len(B):
        return
    result = [[0]*len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j]+B[i][j]
    return result
#[[0.02506921913334438], [0.025852945421114243], [0.05621803709637763], [0.40681069669651926], [0.029737501803973554], [0.3955400481560065], [0.03572363726501575], [0.02506921913334438]]
def pageRank(A,N):
    e = []
    for i in range(N):
        e.append(1)
    norm = 100
    New_P = []
    grade=[]
    for i in range(N):
        New_P.append([1])
    print New_P
    r = [ [(1-d)*i*1/N] for i in e]
    while norm > delt:
        P = New_P
        New_P = matrix_add(r,matrix_multiN(d,matrix_multi(A,P))) #P=(1-d)*e/n+d*M'P PageRank算法的核心
        norm = 0
        #求解矩阵一阶范数
        for i in range(N):
            norm += abs(New_P[i][0]-P[i][0])
    print New_P
    for pr in New_P:
        grade.append(pr[0])
    return grade


#根据邻接矩阵求转移概率矩阵并转向
def tran_and_convert(A):
    print sum(A[0])
    result = [[0]*len(A[0]) for i in range(len(A))]
    result_convert = [[0]*len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j]*1.0/sum(A[i])
    for i in range(len(result)):
        for j in range(len(result[0])):
            result_convert[i][j]=result[j][i]
    return result_convert



def main():
    # A = [[0,1,1,0,0,1,0,0],\
    # [0,0,0,1,1,0,0,0],\
    # [0,0,0,1,0,1,0,0],\
    # [0,0,0,0,0,1,0,0],\
    # [1,0,0,1,0,0,1,1],\
    # [0,0,0,1,0,0,0,0],\
    # [0,0,1,0,0,0,0,0],\
    # [0,0,0,1,0,0,1,0]]
    data = xlrd.open_workbook('data.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    N=nrows-1
    A = [[0]*(ncols-1) for i in range(nrows-1)]
    p=1
    while p<nrows:
        q=1
        while q<ncols:
            A[p-1][q-1]=float(table.cell(p,q).value)
            q=q+1
        p=p+1
    #print M
    M = tran_and_convert(A)
    PR=pageRank(M,N)
    wb=copy(data)
    ws = wb.get_sheet(0)
    i=1
    while i<=N:
        ws.write(i,ncols,PR[i-1])
        i=i+1
    wb.save('data1.xls')
if __name__ == '__main__':
    main()

# from xlrd import open_workbook
# from xlutils.copy import copy
#
# rb = open_workbook('m:\\1.xls')
#
# #通过sheet_by_index()获取的sheet没有write()方法
# rs = rb.sheet_by_index(0)
#
# wb = copy(rb)
#
# #通过get_sheet()获取的sheet有write()方法
# ws = wb.get_sheet(0)
# ws.write(0, 0, 'changed!')
#
# wb.save('m:\\1.xls')