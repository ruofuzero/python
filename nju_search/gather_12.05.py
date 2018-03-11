#coding=utf-8
import re
import urllib2
import httplib
import socket
import MySQLdb
import time
from collections import deque,OrderedDict

global s
s=set()
error_url=[]
class table(object):      #一个table就是一个对象
    def __init__(self,name):
        self.name=name
    def select_duan(self,cur):      #获取url_duan中的url
        cur.execute('select * from duan')
        duan=cur.fetchall()
        return duan
    def select_gather(self,cur):   #获取Url_gather中的url
        cur.execute('select * from gather')
        gather=cur.fetchall()
        return gather
    def update(self,cur,conn,url,duandian):  #更新表
        cur.execute('select * from duan')
        cur.execute('UPDATE duan SET new_url = %d WHERE new_url = %d',(url,duandian))
        conn.commit()
    def insert(self,cur,conn):   #插入单个数据

        cur.execute('insert into gather value(%s)',[url])
        conn.commit()
    def insertmany(self,cur,conn,url):  #插入多个数据

        cur.executemany('insert into gather values(%s)',url)
        conn.commit()
    def insertmany_two(self,cur,conn,url): #插入多字段的数据（tuple）

        cur.executemany('insert into gather values(%s,%s)',url)
        conn.commit()

#http://xiaobao.nju.edu.cn/showarticle.php?articleid=6974

class url(object): #一个url链接也是一个数据
    def __init__(self,content):
        self.content=content
    def http_label(self):  #匹配http
        httpmatch=re.compile('http')
        http_result=httpmatch.match(self.content)
        return http_result
    def open_url(self,cur,conn,error_url):   #打开url页面
        req=urllib2.Request(self.content,headers={'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'})
        try:
            response=urllib2.urlopen(req)
            mypage=response.read()
            # response.close()
            # del req
        except socket.error,e:
            mypage=[]
            error_url.append(self.content)
        except httplib.BadStatusLine,e:
            mypage=[]
            error_url.append(self.content)
        except urllib2.URLError,e:
            mypage=[]
            error_url.append(self.content)
        except httplib.error,e:
            mypage=[]
            error_url.append(self.content)
        except urllib2.HTTPError,e:
            mypage=[]
            error_url.append(self.content)
        return mypage
    def shangji_label(self,new_url):   #匹配上级页面标签
        shangjimatch=re.compile(new_url)
        shangji_result=shangjimatch.search(self.content)
        return shangji_result
    def nju_label(self):   #匹配域名关键词 如：www, jw, nic等
        njumatch=re.compile('http://(.*?).nju.edu')
        nju_result=njumatch.search(self.content)
        return nju_result
    def js_rex(self):  #匹配js标志
        jssearch=re.compile('vascript:void')
        js_result=jssearch.search(self.content)
        return js_result
    def houzhui_label(self,suffix):  #匹配后缀用于删除 如：.css,.iso等
        houzhui=re.compile(suffix)
        houzhui_result=houzhui.search(self.content,re.S)
        return houzhui_result
    def gang_label(self):    #匹配斜杠
        gangmatch=re.compile('/')
        gang_result=gangmatch.match(self.content)
        return gang_result
    def sharpe_rex(self):   #匹配“#”
        sharpe_search=re.compile(r'#(\w+)|#|/#(\w+)|/#')
        result=sharpe_search.sub('',self.content)
        return result
    def sharpe_search(self):
        pattern=re.compile(r'#')
        result=pattern.search(self.content)
        return result

def mysql_conn(database):  #数据库连接
    conn=MySQLdb.connect(host='localhost',user='root',passwd='love539392',port=3306)
    cur=conn.cursor()
    conn.select_db(database)
    return cur,conn

def file_read(filename):  #读取txt文档
    f=open(filename,'r')
    result=f.read()
    f.close()
    return result

def file_readlines(filename): #逐行读取txt文档
    f=open(filename,'r')
    result=f.readlines()
    f.close()
    return result

def file_write(filename,putin): #写入txt文档
    f=open(filename,'w')
    f.write(putin)
    f.close

def eli_enter(huanhang): #去除txt文档中的换行符
    enterRex=re.compile('\n')
    huanhang=enterRex.sub('',huanhang)
    return huanhang

def insert_function(cur,conn,url_url,new_url,ktable,url_result,id,url_all,url_list):   #判断url是否重复，写入数据库
    #url_md5=hashlib.md5(new_url.content).hexdigest()
    n=0
    id_gather=[]
    id_set=set()
    shangji_result=url_url.shangji_label(new_url.content)
    if shangji_result:
        pass
    else:
        js_result=new_url.js_rex()
        if js_result:
            pass
        else:
            sharpe_result=new_url.sharpe_search()
            if sharpe_result:
                pass
            else:
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
                            if nju_result.group(1) in url_all:
                        #cur,conn=mysql_conn('python')
                                new_url.content=new_url.sharpe_rex()
                                pattern=re.compile(r'/$')
                                new_url.content=pattern.sub('',new_url.content)
                                new_url.content=new_url.content.lower()
                                cur.execute('select * from id_url')
                                id_set=set(url_list)
                                if new_url.content not in id_set:
                                    url_result[new_url.content]=id
                                    cur.execute("insert into id_url value(%s,%s)",(str(id),new_url.content))
                                    conn.commit()
                                    id=id+1
                                    url_list.append(new_url.content)

                                else:
                                    pass
                                url2_result=ktable.select_gather(cur)

                                if (str(url_result[new_url.content]),str(url_result[url_url.content])) in url2_result:
                                    pass
                                else:
                                    s.add((str(url_result[new_url.content]),str(url_result[url_url.content])))

                                # if nju_result.group(1)==ktable.name:
                                #     pass
                                # else:
                                #     url_result.pop(new_url.content)
                                #     url_list.pop()

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
                        new_url.content=new_url.sharpe_rex()
                        pattern=re.compile(r'/$|/ +$')
                        new_url.content=pattern.sub('',new_url.content)
                        new_url.content=new_url.content.lower()
                        id_set=set(url_list)
                        if new_url.content not in id_set:
                            url_result[new_url.content]=id
                            cur.execute("insert into id_url value(%s,%s)",(str(id),new_url.content))
                            conn.commit()
                            url_list.append(new_url.content)
                            id=id+1
                        else:
                            pass
                        url2_result=ktable.select_gather(cur)

                        if (str(url_result[new_url.content]),str(url_result[url_url.content])) in url2_result:
                            pass
                        else:
                            s.add((str(url_result[new_url.content]),str(url_result[url_url.content])))

                else:
                    pass
    return id
# def multi_threading(url_result,cur,conn,url2,k,url_url,ktable,**kw):
#
#     for p in url2:
#         num=0
#         new_url=url(p)
#         try:
#             if k in blacklist:
#                 for i in kw:
#                     if k==i:
#                         for heiyu in dict[i]:
#                             if heiyu in new_url.content:
#                                 num=num+1
#                         if num==0:
#                              insert_function(cur,conn,url_url,new_url,ktable,url_result)
#                         else:
#                             pass
#                     else:
#                         pass
#             else:
#                 insert_function(cur,conn,url_url,new_url,ktable,url_result)
#         except re.error,e:
#             error=[p]
#             #print 'yes'
#             pass
def url_allopen(txt):
    for i in open(txt):
        yield i
def url_fetch1(mypage):    #正则匹配
    url_pattern=re.compile('''href=(?:"(.*?)"|'(.*?)'|(.*?))''',re.I)
    return url_pattern.finditer(mypage)
# def url_fetch2(mypage):
#     url2_pattern=re.compile("href='(.*?)'",re.I)
#     return url2_pattern.finditer(mypage)
if __name__ == '__main__':


    dict={'cosec':'title','scw973':'itemstr','moon':'calendar','seg':'publication','innovation':'comment','horizon':'session','dafls':'categories','tuanwei':{'article?catid','format=opensearch'},'eol':{'claroline','rest_route','redirect','feed=rss'}}#控制一些有问题的网站的域名
    cur,conn=mysql_conn('njusearch') #链接数据库
    cur.execute("select * from id_url")  #id的设置
    id_url=cur.fetchall()
    id_length=len(id_url)
    if id_url:
        id=int(id_url[id_length-1][0])+1
    else:
        id=1
    blacklist=[]
    url_all=['stuex','www','xgc','xiaoban']
    heimingdan=file_readlines('heimingdan.txt')
    for i in heimingdan:
        i=eli_enter(i)
        blacklist.append(i)
    url_result=OrderedDict()
    url_list=deque()
    i=0
    #url_all=file_readlines('url_all.txt')
    for key in url_allopen('url_test.txt'):

        #time_duan=float(time_duan)
        start_time=time.time()
        print key
        k=eli_enter(key)
        ktable=table(k)

        #duan=ktable.select_duan(cur)
        url_list.append('http://'+k+'.nju.edu.cn')
        if 'http://'+k+'.nju.edu.cn' not in url_result.keys():
            url_result['http://'+k+'.nju.edu.cn']=id

        cur.execute('select * from id_url')
        id_url_reuslt=cur.fetchall()
        id_s=[]
        if id_url_reuslt:
            for id_count in id_url_reuslt:
                id_s.append(id_count[1])
            if 'http://'+k+'.nju.edu.cn' not in id_s:
                cur.execute("insert into id_url value(%s,%s)",(str(id),'http://'+k+'.nju.edu.cn'))
                conn.commit()
                id=id+1
        else:
            cur.execute("insert into id_url value(%s,%s)",(str(id),'http://'+k+'.nju.edu.cn'))
            conn.commit()
            id=id+1
        #print url_result[0]

        length=len(url_list)
        # while url_result[i]!=duan[0][0]:
        #     i=i+1
        while i<length:
            url_url=url(url_list[i])  #url_url为一个url对象
            print url_url.content
            #duandian=ktable.select_duan(cur)
            #ktable.update(cur,conn,url_url.content,duandian[0][0])

            func1_start=time.time()
            mypage=url_url.open_url(cur,conn,error_url)
            func1_end=time.time()
            print "func1 time =",func1_end-func1_start
            if mypage:
                func2_start=time.time()
                if url_fetch1(mypage):
                    for ia in url_fetch1(mypage):
                        if ia.group(1):
                            num1=0
                            new_url=url(ia.group(1))
                        #url_result[new_url.content]=id
                        #id=id+1
                            try:
                                if k in blacklist:
                                    for iw in dict:
                                        if k==iw:
                                            for heiyu in dict[iw]:
                                                if heiyu in new_url.content:
                                                    num1=num1+1
                                            if num1==0:
                                                id=insert_function(cur,conn,url_url,new_url,ktable,url_result,id,url_all,url_list)
                                            else:
                                                pass
                                        else:
                                            pass
                                else:
                                    id=insert_function(cur,conn,url_url,new_url,ktable,url_result,id,url_all,url_list)
                            except re.error,e:
                                pass
                        if ia.group(2):
                            num1=0
                            new_url=url(ia.group(2))
                        #url_result[new_url.content]=id
                        #id=id+1
                            try:
                                if k in blacklist:
                                    for iw in dict:
                                        if k==iw:
                                            for heiyu in dict[iw]:
                                                if heiyu in new_url.content:
                                                    num1=num1+1
                                            if num1==0:
                                                id=insert_function(cur,conn,url_url,new_url,ktable,url_result,id,url_all,url_list)
                                            else:
                                                pass
                                        else:
                                            pass
                                else:
                                    id=insert_function(cur,conn,url_url,new_url,ktable,url_result,id,url_all,url_list)
                            except re.error,e:
                                pass
                        if ia.group(3):
                            num1=0
                            new_url=url(ia.group(3))
                        #url_result[new_url.content]=id
                        #id=id+1
                            try:
                                if k in blacklist:
                                    for iw in dict:
                                        if k==iw:
                                            for heiyu in dict[iw]:
                                                if heiyu in new_url.content:
                                                    num1=num1+1
                                            if num1==0:
                                                id=insert_function(cur,conn,url_url,new_url,ktable,url_result,id,url_all,url_list)
                                            else:
                                                pass
                                        else:
                                            pass
                                else:
                                    id=insert_function(cur,conn,url_url,new_url,ktable,url_result,id,url_all,url_list)
                            except re.error,e:
                                pass
                        if (ia.group(1)==None) & (ia.group(2)==None) & (ia.group(3)==None):
                            redict_pattern=re.compile('http-equiv="refresh"')
                            redict_result=redict_pattern.search(mypage)
                            if redict_result:
                                quotation=re.compile('&quot;')
                                mypage=quotation.sub('',mypage)
                                newurl_pattern=re.compile('URL=(.*?)"')
                                newurl_result=newurl_pattern.search(mypage)
                                if newurl_result:
                                    http_pattern=re.compile('http')
                                    http_result=http_pattern.search(newurl_result.group(1))
                                    if http_result:
                                        nju_pattern=re.compile('http://(.*?).nju.edu.cn')
                                        nju_result=nju_pattern.search(newurl_result.group(1))
                                        if nju_result:
                                            if nju_result in url_all:
                                                end_pattern=re.compile(r'/$')
                                                newurl=end_pattern.sub('',newurl_result.group(1))
                                                newurl=newurl.lower()
                                                if newurl not in url_list:
                                                    url_list.append(newurl)
                                                    url_result[newurl]=url_result[url_url.content]
                                                    cur.execute('select * from id_url')
                                                    cur.execute('UPDATE id_url SET url = %s WHERE id = %s',(newurl,str(url_result[url_url.content])))
                                                    conn.commit()
                                    else:
                                        gangmatch=re.compile('/')
                                        gang_result=gangmatch.match(newurl_result.group(1))
                                        if gang_result:
                                            newurl='http://'+ktable.name+'.nju.edu.cn'+newurl_result.group(1)
                                        else:
                                            newurl='http://'+ktable.name+'.nju.edu.cn/'+newurl_result.group(1)
                                        end_pattern=re.compile(r'/$')
                                        newurl=end_pattern.sub('',newurl)
                                        newurl=newurl.lower()
                                        if newurl not in url_list:
                                            url_list.append(newurl)
                                            url_result[newurl]=url_result[url_url.content]
                                            cur.execute('select * from id_url')
                                            cur.execute('UPDATE id_url SET url = %s WHERE id = %s',(newurl,str(url_result[url_url.content])))
                                            conn.commit()
                func2_end=time.time()
                print "func2 time =",func2_end-func2_start

                func3_start=time.time()
                ktable.insertmany_two(cur,conn,s)
                func3_end=time.time()
                print "func3 time =",func3_end-func3_start
            #conn.commit()
            else:
                pass

            s.clear()
            i=i+1
            length=len(url_list)
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
    for er_url in error_url:
        cur.execute("delete from gather where new_url= %s" ,(str(url_result[er_url])))
        conn.commit()
        cur.execute("delete from id_url where id=%s",(str(url_result[er_url])))
        conn.commit()

    conn.commit()
    cur.close()
    conn.close()







