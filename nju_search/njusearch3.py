#coding=utf-8
import re
import urllib2
import httplib
import socket
import MySQLdb
import time
from collections import deque

global s
s=set()

class table(object):
    def __init__(self,name):
        self.name=name
    def select_duan(self,cur):
        cur.execute('select * from '+self.name+'duan')
        duan=cur.fetchall()
        return duan
    def select_gather(self,cur):
        cur.execute('select * from '+self.name+'gather')
        gather=cur.fetchall()
        return gather
    def update(self,cur,conn,url,duandian):
        cur.execute('select * from '+self.name+'duan')
        cur.execute('UPDATE '+self.name+'duan SET url = %s WHERE url = %s',(url,duandian))
        conn.commit()
    def insert(self,cur,conn):

        cur.execute('insert into '+self.name+'gather value(%s)',[url])
        conn.commit()
    def insertmany(self,cur,conn,url):

        cur.executemany('insert into '+self.name+'gather values(%s)',url)
        conn.commit()


#http://xiaobao.nju.edu.cn/showarticle.php?articleid=6974

class url(object):
    def __init__(self,content):
        self.content=content
    def http_label(self):
        httpmatch=re.compile('http')
        http_result=httpmatch.match(self.content)
        return http_result
    def open_url(self):
        req=urllib2.Request(self.content,headers={'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'})
        try:
            response=urllib2.urlopen(req)
            mypage=response.read()
            # response.close()
            # del req
        except socket.error,e:
            mypage=[]
            pass
        except httplib.BadStatusLine,e:
            #print 'yes'
            mypage=[]
            pass
        except urllib2.URLError,e:
            #print 'yes'
            mypage=[]
            pass
        except httplib.error,e:
            #print 'yes'
            mypage=[]
            pass
        except urllib2.HTTPError,e:
            #print 'yes'
            mypage=[]
            pass
        return mypage
    def shangji_label(self,new_url):
        shangjimatch=re.compile(new_url)
        shangji_result=shangjimatch.search(self.content)
        return shangji_result
    def nju_label(self):
        njumatch=re.compile('http://(.*?).nju.edu')
        nju_result=njumatch.search(self.content)
        return nju_result
    def houzhui_label(self,suffix):
        houzhui=re.compile(suffix)
        houzhui_result=houzhui.search(self.content,re.S)
        return houzhui_result
    def gang_label(self):
        gangmatch=re.compile('/')
        gang_result=gangmatch.match(self.content)
        return gang_result

def mysql_conn(database):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='love539392',port=3306)
    cur=conn.cursor()
    conn.select_db(database)
    return cur,conn

def file_read(filename):
    f=open(filename,'r')
    result=f.read()
    f.close()
    return result

def file_readlines(filename):
    f=open(filename,'r')
    result=f.readlines()
    f.close()
    return result

def file_write(filename,putin):
    f=open(filename,'w')
    f.write(putin)
    f.close

def eli_enter(huanhang):
    enterRex=re.compile('\n')
    huanhang=enterRex.sub('',huanhang)
    return huanhang

def insert_function(cur,conn,url_url,new_url,ktable,url_result):
    #url_md5=hashlib.md5(new_url.content).hexdigest()
    n=0
    shangji_result=url_url.shangji_label(new_url.content)
    if shangji_result:
        pass
    else:
        #zhui=file_readlines('houzhui.txt')
        for suffix in open('houzhui.txt'):
            suffix=eli_enter(suffix)
            houzhui_result=new_url.houzhui_label(suffix)
            if houzhui_result:
                n=n+1
        if n == 0:
            http_result=new_url.http_label()
            if http_result:
                nju_result=new_url.nju_label()
                if nju_result:
                    if nju_result.group(1)==ktable.name:
                        #cur,conn=mysql_conn('python')

                        url2_result=ktable.select_gather(cur)
                        #
                        for key_url in url2_result:
                            if key_url[0]==new_url.content:
                                n=n+1
                        if n == 0:
                            #print new_url.content

                            # ktable.insert(cur,conn,new_url.content)
                            s.add((new_url.content,))
                            url_result.append(new_url.content)

                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                gang_result=new_url.gang_label()
                if gang_result:
                    new_url.content='http://'+ktable.name+'.nju.edu.cn'+new_url.content
                else:
                    new_url.content='http://'+ktable.name+'.nju.edu.cn'+'/'+new_url.content
                #cur,conn=mysql_conn('python')
                url2_result=ktable.select_gather(cur)
                # conn.commit()
                # cur.close()
                # conn.close()

                for key_url in url2_result:
                    if key_url[0] == new_url.content:
                        n=n+1

                if n==0:
                    #print new_url.content
                    # url_md5=hashlib.md5(new_url.content).hexdigest()
                    #ktable.insert(cur,conn,new_url.content)
                    s.add((new_url.content,))
                    url_result.append(new_url.content)
        else:
            pass
def multi_threading(url_result,cur,conn,url2,k,url_url,ktable,**kw):

    for p in url2:
        num=0
        new_url=url(p)
        try:
            if k in blacklist:
                for i in kw:
                    if k==i:
                        for heiyu in dict[i]:
                            if heiyu in new_url.content:
                                num=num+1
                        if num==0:
                             insert_function(cur,conn,url_url,new_url,ktable,url_result)
                        else:
                            pass
                    else:
                        pass
            else:
                insert_function(cur,conn,url_url,new_url,ktable,url_result)
        except re.error,e:
            error=[p]
            #print 'yes'
            pass
def url_allopen(txt):
    for i in open(txt):
        yield i
def url_fetch1(mypage):
    url_pattern=re.compile('''href=(?:"(.*?)"|'(.*?)'|(.*?))''',re.I)
    return url_pattern.finditer(mypage)
# def url_fetch2(mypage):
#     url2_pattern=re.compile("href='(.*?)'",re.I)
#     return url2_pattern.finditer(mypage)
if __name__ == '__main__':
    dict={'cosec':'title','scw973':'itemstr','moon':'calendar','seg':'publication','innovation':'comment','horizon':'session','dafls':'categories','tuanwei':{'article?catid','format=opensearch'},'eol':{'claroline','rest_route','redirect','feed=rss'}}
    cur,conn=mysql_conn('njusearch')
    blacklist=[]

    heimingdan=file_readlines('heimingdan.txt')
    for i in heimingdan:
        i=eli_enter(i)
        blacklist.append(i)

    #url_all=file_readlines('url_all.txt')
    for key in url_allopen('url_test.txt'):

        #time_duan=float(time_duan)
        start_time=time.time()
        print key
        k=eli_enter(key)
        ktable=table(k)

        duan=ktable.select_duan(cur)
        url_result=deque()
        url_result.append('http://'+k+'.nju.edu.cn')
        #print url_result[0]
        i=0
        length=len(url_result)
        while url_result[i]!=duan[0][0]:
            i=i+1
        while i<length:
            url2=deque()
            url3=deque()
            url_url=url(url_result[i])
            print url_url.content
            duandian=ktable.select_duan(cur)
            ktable.update(cur,conn,url_url.content,duandian[0][0])

            func1_start=time.time()
            mypage=url_url.open_url()
            func1_end=time.time()
            print "func1 time =",func1_end-func1_start
            if mypage:
                func2_start=time.time()
                for ia in url_fetch1(mypage):
                    if ia.group(1):
                        num1=0
                        new_url=url(ia.group(1))
                        try:
                            if k in blacklist:
                                for iw in dict:
                                    if k==iw:
                                        for heiyu in dict[iw]:
                                            if heiyu in new_url.content:
                                                num1=num1+1
                                        if num1==0:
                                            insert_function(cur,conn,url_url,new_url,ktable,url_result)
                                        else:
                                            pass
                                    else:
                                        pass
                            else:
                                insert_function(cur,conn,url_url,new_url,ktable,url_result)
                        except re.error,e:
                    #error=[p]
            #print 'yes'
                            pass
                # for ii in url_fetch1(mypage):
                #     num2=0
                #     new_url=url(ii.group(1))
                #     try:
                #         if k in blacklist:
                #             for i in kw:
                #                 if k==i:
                #                     for heiyu in dict[i]:
                #                         if heiyu in new_url.content:
                #                             num2=num2+1
                #                     if num2==0:
                #                         insert_function(cur,conn,url_url,new_url,ktable,url_result)
                #                     else:
                #                         pass
                #                 else:
                #                     pass
                #         else:
                #             insert_function(cur,conn,url_url,new_url,ktable,url_result)
                #     except re.error,e:
                    #error=[p]
            #print 'yes'
                        # pass
            func2_end=time.time()
            print "func2 time =",func2_end-func2_start

            #del url2 ,url3
            # t1=threading.Thread(target=multi_threading(cur,conn,u1,k,url_url,ktable,**dict))
            # #threads.append(t1)
            # t2=threading.Thread(target=multi_threading(cur,conn,u2,k,url_url,ktable,**dict))
            # threads.append(t2)
            # t3=threading.Thread(target=multi_threading(cur,conn,u3,k,url_url,ktable,**dict))
            # threads.append(t3)
            # t4=threading.Thread(target=multi_threading(cur,conn,u4,k,url_url,ktable,**dict))
            # threads.append(t4)
            # for t in threads:
            #     t.setDaemon(True)
            #     t.start()
            # for t in threads:
            #     t.join()
            #     p = Pool()
            #     for url5 in u_sum:
            #         p.apply_async(multi_threading(cur,conn,url5,k,url_url,ktable,**dict))
            # p.apply_async(multi_threading(cur,conn,u2,k,url_url,ktable,**dict))

            # t3.start()
            # t4.start()
            #     p.close()
            #     p.join()
            # t3.join()
            # t4.join()
            # print s
            func3_start=time.time()
            ktable.insertmany(cur,conn,s)
            func3_end=time.time()
            print "func3 time =",func3_end-func3_start
            #conn.commit()

            s.clear()


            i=i+1

            length=len(url_result)
            end_time=time.time()
            if (end_time-start_time)>86400:
                break
        if (end_time-start_time)>86400:
            pass
        else:
            time_duan=float(file_read('time.txt'))
            time_sum=time_duan+end_time-start_time
            s_time=str(time_sum)
            file_write('time.txt',s_time)

    conn.commit()
    cur.close()
    conn.close()

