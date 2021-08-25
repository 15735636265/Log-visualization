import pymysql #导包
from collections import Counter;
import json
import flask
from flask import render_template

app =flask.Flask(__name__)
@app.route('/')
def index():
    # 连接数据库
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='rizhi')
    # 定义游标
    cursor = db.cursor()
    # sql语句
    sql = 'select IP,Time,methods,region,country,city from nginxlog;'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    ip_list = []
    time_list = []
    methods_list=[]
    region_list=[]
    country_list=[]
    city_list = []
    for row in results:
        ip = row[0]
        time = row[1]
        methods=row[2]
        region=row[3]
        country=row[4]
        city = row[5]
        ip_list.append(ip)
        time_list.append(time.strftime("%m")+'月')   #将时间转化成月份"%m"(年月日时分秒：%Y%M%D%H%D%S)
        methods_list.append(methods)
        region_list.append(region)
        country_list.append(country)
        city_list.append(city)
    #字典输出ip访问次数
    ip_number=dict(Counter(ip_list))
    print(ip_number)
    #字典输出每个月访问次数
    time_number = dict(Counter(time_list))
    print(time_number)
    #字典输出HTTP方法访问次数
    methods_number=dict(Counter(methods_list))
    print(methods_number)
    #字典输出省份访问次数
    region_number=dict(Counter(region_list))
    print(region_number)
    #字典输出国家访问次数
    country_number=dict(Counter(country_list))
    print(country_number)
    #字典输出各个城市访问次数
    city_number = dict(Counter(city_list))
    print(city_number)
    #获取一共多少访问量
    sql = 'select count(*) from nginxlog;'
    cursor.execute(sql)
    results = cursor.fetchall()
    count=results[0][0]
    #获取404的访问量
    sql='select count(*) from nginxlog where status=404;'
    cursor.execute(sql)
    results = cursor.fetchall()
    status_count = results[0][0]
    # 关闭游标
    cursor.close()
    # 数据回滚
    db.rollback()
    # 关闭数据库
    db.close()
    #IP,Time,methods,region,country,city
    ip_values = list(ip_number.values())
    ip_keys = json.dumps(list(ip_number.keys()))
    print(ip_keys)
    ips=[]
    top_ip = sorted(set(ip_number.values()), reverse=True)[:5]
    filtered = sorted([[e, ip_number[e]] for e in ip_number if ip_number[e] in top_ip],key=lambda k: k[1], reverse=True)
    for name, value in filtered:
        ip={"name":name,"value":value}
        ips.append(ip)
    print(ips)
    time_values = list(time_number.values())
    time_keys = json.dumps(list(time_number.keys()))
    print(time_keys)
    methods_values = list(methods_number.values())
    methods_keys = list(methods_number.keys())
    print(methods_values)
    print(methods_keys)
    #输出https方法最多的前三个
    method = []
    top_method=sorted(set(methods_number.values()),reverse=True)[:3]
    filtered=sorted([[e,methods_number[e]] for e in methods_number if methods_number[e] in top_method],key=lambda k:k[1],reverse=True)
    for name,value in filtered:
        methods={"name":name,"value":value}
        method.append(methods)
    print(method)
    region_values = list(region_number.values())
    region_keys = json.dumps(list(region_number.keys()))
    print(region_keys)
    regions=[]
    region_keys=[]
    region_values=[]
    top_region = sorted(set(region_number.values()), reverse=True)[:10]
    filtered = sorted([[e, region_number[e]] for e in region_number if region_number[e] in top_region],
                      key=lambda k: k[1], reverse=True)
    for name, value in filtered:
        region= {"name": name, "value": value}
        regions.append(region)
        region_keys.append(name)
        region_values.append(value)
    print(regions)
    country_values = list(country_number.values())
    country_keys = json.dumps(list(country_number.keys()))
    print(country_keys)
    country_keys = []
    country_values = []
    countrys = []
    top_country = sorted(set(country_number.values()), reverse=True)
    filtered = sorted([[e, country_number[e]] for e in country_number if country_number[e] in top_country],
                      key=lambda k: k[1], reverse=True)
    for name, value in filtered:
        country = {"name": name, "value": value}
        countrys.append(country)
        country_keys.append(name)
        country_values.append(value)
    print(countrys)
    city_values= list(city_number.values())
    city_keys= json.dumps(list(city_number.keys()))
    print(city_keys)
    city_keys=[]
    city_values=[]
    citys=[]
    top_city = sorted(set(city_number.values()), reverse=True)[:10]
    filtered = sorted([[e, city_number[e]] for e in city_number if city_number[e] in top_city],
                      key=lambda k: k[1], reverse=True)
    for name, value in filtered:
        city = {"name": name, "value": value}
        citys.append(city)
        city_keys.append(name)
        city_values.append(value)
    print(citys)
    return render_template('index.html',status_count=status_count,count=count,ips=ips,ip_v=ip_values,ip_k=ip_keys,ti_v=time_values,ti_k=time_keys,method=method,me_v=methods_values,me_k=methods_keys,res=regions,re_v=region_values,re_k=region_keys,cos=countrys,co_v=country_values,co_k=country_keys,cis=citys,ci_v=city_values,ci_k=city_keys)
if __name__=="__main__":
     app.run()

