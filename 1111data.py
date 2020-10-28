import requests
from bs4 import BeautifulSoup
import pandas as pd

df = []
baseurl = 'https://www.1111.com.tw/job-bank/job-index.asp?si=1&ks=電腦&ss=s&ps=100&page='  #電腦

#取得總頁數
html = requests.get(baseurl + '1')
soup = BeautifulSoup(html.text, 'lxml')
tem = soup.find('option',value='1').text
page = int(tem.replace('1 / ', ''))

if page > 15:  #最多取15頁資料
    page = 1
#逐頁讀取資料
for i in range(page):
    url = baseurl + str(i+1)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    # job = soup.find_all()
    job = soup.select(".it-md")  #取class=jbInfoin內容
    for j in range(len(job)):
        work = job[j].find('a',class_='text-truncate position0Link mobileItemClick').get('title')  #職務名稱
        work = work.replace('【誠徵】', '').replace('【急徵】', '').replace('誠徵', '')
        site = 'https://www.1111.com.tw/' + job[j].find('a',class_='text-truncate position0Link mobileItemClick').get('href')  #工作網址
        company = job[j].find('div',class_='d-block d-md-none text-truncate jb-organ-m').text  #公司名稱
        companysort = job[j].find('span', class_='d-none d-md-block').text  #公司類別
        companysort = companysort.replace('｜','')
        area = job[j].find('span', class_='d-inline d-lg-none').text  #工作地點
        salary = job[j].find('span', style='color:#dd7926;').text
        experiment = job[j].find('span','d-none d-md-inline').text  #工作經驗
        school = job[j].find('span','d-none d-md-inline').text  #學歷
        content = job[j].find('div', class_='col-12 jbInfoTxt UnExtension').text

        dfmono = pd.DataFrame([{'職務名稱':work,
                             '工作網址': site,
                             '公司名稱': company,
                             '公司類別': companysort,
                             '工作地點':area,
                             '薪資':salary,
                             '工作經驗':experiment,
                             '學歷':school,
                             '工作內容':content }],
                             )
        df.append(dfmono)
    print('處理第 ' + str(i+1) + ' 頁完畢！')

df = pd.concat(df, ignore_index=True)

df.to_excel('1111data.xlsx', index=0)  #存為excel檔

