import re,httplib2,datetime,sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode 
class Spider():
    def __init__(self):
        self.header={"User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER",'cache-control':'no-cache'}
        self.h=httplib2.Http()
        self.url='http://www.landchina.com/default.aspx?tabid=263'
        #这是用post要提交的数据
        self.postData={  'TAB_QueryConditionItem':'9f2c3acd-0256-4da2-a659-6949c4671a2a',
                         'TAB_QuerySortItemList':'282:False',
                         #日期
                         'TAB_QuerySubmitConditionData':'9f2c3acd-0256-4da2-a659-6949c4671a2a:',  
                         'TAB_QuerySubmitOrderData':'282:False',
                          #第几页
                         'TAB_QuerySubmitPagerData':''} 
        self.info=[   
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl',#0
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl',#1
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl',#2
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl',#3
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl',#4
                #这条信息是土地来源，抓取下来的是数字，它要经过换算得到土地来源，不重要，我就没弄了
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl',#6  
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl',#7
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl', #8              
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl',#9
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl',#10
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl',#11
##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c1_0_ctrl',
##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c2_0_ctrl',
##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c3_0_ctrl',
##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c4_0_ctrl',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl',#12
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c2_ctrl',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c4_ctrl',                
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2_ctrl',
                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl']
    def handleDate(self,year,month,day):
        #返回日期数据
        'return date format %Y-%m-%d'
        date=datetime.date(year,month,day)
#        print date.datetime.datetime.strftime('%Y-%m-%d')
        return date  #日期对象
    def timeDelta(self,year,month):
        #计算一个月有多少天
        date=datetime.date(year,month,1)
        try:    
            date2=datetime.date(date.year,date.month+1,date.day)
        except:
            date2=datetime.date(date.year+1,1,date.day)  
        dateDelta=(date2-date).days
        return dateDelta
        
    def getPageContent(self,pageNum,date):
        
        #指定日期和页数，打开对应网页，获取内容
        postData=self.postData.copy()
        #设置搜索日期
        queryDate=date.strftime('%Y-%m-%d')+'~'+date.strftime('%Y-%m-%d')
        postData['TAB_QuerySubmitConditionData']+=queryDate
        #设置页数
        postData['TAB_QuerySubmitPagerData']=str(pageNum)
        #请求网页
        r=requests.post(self.url,data=postData,timeout=30)
        pageContent=r.text
        return pageContent
#第二步
    def getAllNum(self,date): 
        firstContent=self.getPageContent(1,date)
        if u'没有检索到相关数据' in firstContent:
            print (date,'have','0 page')
            return 0
        pattern=re.compile(u'<td.*?class="pager".*?>共(.*?)页.*?</td>')
        result=re.search(pattern,firstContent)
        if result==None:
            print (date,'have','1 page')
            return 1
        if int(result.group(1))<=200:
            print (date,'have',int(result.group(1)),'page')
            return int(result.group(1))
        else:
            print (date,'have','200 page')
            return 200
#第三步
    def getLinks(self,pageNum,date):
        'get all links'
        pageContent=self.getPageContent(pageNum,date)
        links=[]
        pattern=re.compile(u'<a.*?href="default.aspx.*?tabid=386(.*?)".*?>',re.S)
        results=re.findall(pattern,pageContent)
        for result in results:
            links.append('http://www.landchina.com/default.aspx?tabid=386'+result)
        return links  
    def getAllLinks(self,allNum,date):
        pageNum=1
        allLinks=[]
        while pageNum<=allNum:
            links=self.getLinks(pageNum,date)
            allLinks+=links
            print('scrapy link from page',pageNum,'/',allNum)
            pageNum+=1
        print (date,'have',len(allLinks),'link')
        return allLinks 
#第四步 
    def getLinkContent(self,link):
        'open the link to get the linkContent'
        resp,cont=self.h.request(link)
        linkContent=cont.decode('gbk')
        return linkContent
    def getInfo(self,linkContent):
        "get every item's info"
        data=[]
        soup=BeautifulSoup(linkContent,'html.parser')
        for item in self.info:
            if soup.find(id=item)==None:
                s=''
            else:
                s=soup.find(id=item).string
                if s==None:
                    s='null'             
            data.append(s)
        print(data)
        return data
    def saveInfo(self,data,tablename,cx):
        data=tuple(data)
        tablename=tablename
        cx=cx
        cx.execute('insert into %s values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'%tablename,data)
        cx.commit()
    def saveAllInfo(self,allLinks,date,tablename,cx):#存储单日数据
        for (i,link) in enumerate(allLinks):
            linkContent=data=None
            linkContent=self.getLinkContent(link)
            data=self.getInfo(linkContent)
            self.saveInfo(data,tablename,cx)
            print ('save info from link',i+1,'/',len(allLinks))
        cx.commit()