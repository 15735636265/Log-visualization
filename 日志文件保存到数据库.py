#/usr/bin/env python
#-*-coding:UTF-8 -*-
from  datetime  import  datetime
import requests
import pymysql
#print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) #2018-05-25 22:23:44
#print(datetime.now().strftime("%d/%b-%Y %H:%M:%S")) #25/May-2018 22:23:44格式
#print(datetime.strptime('17/Jun/2017:12:11:16',"%d/%b/%Y:%H:%M:%S")) #格式转换


def 数据库(log):
   with open('./rizhi/'+log,"r",encoding='utf-8')  as  ngfile:
      for line in ngfile:
         try:
            _nodes = line.split()
            IP= _nodes[0]
            Time= _nodes[3][1:-1].replace(":"," ",1) #将时间转换为17/Jun/2017 12:43:4格式
            Time = datetime.strptime(Time,"%d/%b/%Y %H:%M:%S")#将时间格式化为2017-06-17 12:43:04
            Methods = _nodes[5][1:]
            Source = _nodes[6]
            Protocol = _nodes[7][:-1]
            Status = _nodes[8]
         except IndexError:
            print("没有此索引")
         except BaseException:
            print("连接失败")
         # Status=[]
         r = requests.get('http://ip-api.com/json/%s?lang=zh-CN' % IP)
         # if r.json()['status']=='success':
         if r.content:
            i = r.json()
            cou = i['country']
            reg = i['regionName']
            cit = i['city']
            map_city=[]
            map_city.append(u'%s%s%s'% (cou,reg,cit))
            country=[]
            country.append(u'%s' %cou)
            region=[]
            region.append(u'%s' %reg)
            city = []
            city.append(u'%s' % cit)
         else:
            print("error! ip: %s" % IP)
         print(IP,Time,Methods,Source,Protocol,Status,map_city,country,region,city)

         connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='rizhi',
            charset="utf8"
         )
         cur = connect.cursor()
         sql = "insert into nginxlog(ip,time,methods,source,protocol,status,map_city,country,region,city) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
         cur.execute(sql,(IP,Time,Methods,Source,Protocol,Status,map_city,country,region,city))
         connect.commit()

      connect.close()
logs=['access_log','love.gkx.cool-access_log','test.gkx.cool-access_log','www.gkx.cool-access_log']
for log in logs:
   数据库(log)