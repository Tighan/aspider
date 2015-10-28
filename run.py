
import spider,sqlite3,time,random
s=spider.Spider()
#日期
cx=sqlite3.connect('spider.db')
cx.execute('create table nowat (id,month,year)')
cx.execute('insert into nowat values(0,0,0)')
cu=cx.cursor()
dictyear={1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九",0:"零"}
dictmonth={1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九",10:"十",11:"十一",12:"十二"}
def returnyear(year):
    year=str(year)
    t=''
    for k in year:
        t=t+dictyear[int(k)]
    t=t+"年"
    return t
def returnmonth(month):
    return dictmonth[month]+"月"
def getData(year1,month1,year2,month2):
    for year in range(int(year1),int(year2)+1):
        for month in range(int(month1),int(month2)+1):
            day=1
            tablename=returnyear(year)+returnmonth(month)
            cx.execute("create table %s ('行政区','电子监管号','项目名称','项目位置','面积(公顷)','土地用途','供地方式','土地使用年限','行业分类','土地级别','成交价格(万元)','土地使用权人','约定容积率下限','约定容积率上限','约定交地时间','约定开工时间','约定竣工时间','实际开工时间','实际竣工时间','批准单位','合同签订日期')"%tablename)
            cu.execute("update nowat set year='%s' where id = 0"%year)
            cu.execute("update nowat set month='%s' where id = 0"%month)
            delta=s.timeDelta(int(year),int(month))
            while day<=delta:
        #日期
                date=s.handleDate(year,month,day)
        #页数
                allNum=s.getAllNum(date)
        #链接
                allLinks=s.getAllLinks(allNum,date)
        #信息
                s.saveAllInfo(allLinks,date,tablename,cx)
                day+=1
             #   print(date,'KO!')
            #print (date.strftime('%Y-%m'),'KO!')
            print ("now at",year,month)
            time.sleep(random.random() * 3)
def restart():
    order=False
    cu.execute("select * from nowat")
    yam=cu.fetchall()[0]
    year=int(yam[1])
    month=int(yam[2])+1
    if month>12:
        year=year+1
        month=1
    if year!=2015 and month!=10:
        getData(year,month,2015,9)
    else:
        order=True
    return order
while True:
    try:
        getData(1996,1,2015,1)
    except:
        o=restart()
        if o ==True:
            break