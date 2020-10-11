"""
目前進度：
1. 修改 tkinter介面
2. 考慮 普通文章的單字轉入單字資料庫的功能
3. 改寫 將資料庫從Excel轉為sqlite
"""


import requests
import bs4
import tkinter as tk
import re
import pandas as pd

# 提取單字資料庫的單字串列
vpath = '/Users/justin/Desktop/Python/Python training/Project/Anki/EnglishLearner/Vacabulary/Vacabulary.xlsx'
vdf = pd.read_excel(vpath,header=None)
vdf = vdf.iloc[:,0]
vdf = vdf.values
vdf = list(vdf)

def compare_voictube_v_to_database():
    # 提取單字資料庫的單字串列
    vpath = '/Users/justin/Desktop/Python/Python training/Project/Anki/EnglishLearner/Vacabulary/Vacabulary.xlsx'
    vdf = pd.read_excel(vpath, header=None)
    vdf = vdf.iloc[:, 0]
    vdf = vdf.values
    vdf = list(vdf)

    # 輸入Voicetube網址，抓取文章
    url = voicetubeUrl.get()
    html = requests.get(url)
    sp = bs4.BeautifulSoup(html.text, 'lxml')

    datas = sp.find_all('div', class_='caption-middle')

    # 將文章變為一個一個的單字
    lst = []
    for data in datas:
        lst.append(data.text.split('\n')[0])
    pattern = r'[a-zA-z]+'

    sen_lst = [re.findall(pattern, x.strip().lower()) for x in lst]
    word_lst = ','.join([','.join(sen) for sen in sen_lst]).split(',')

    word_lst = list(set(word_lst)) # 處理Voicetube文章重複單字

    len_of_word_lst = len(word_lst) # 計算Voicetube文章數量
    # 顯示已學會的單字佔比數
    if word_lst != ['']:
        n = 0
        for v in vdf:
            if v in word_lst:
                n += 1
        already_learned = n / len_of_word_lst
        already_learned = round(already_learned * 100, 2)
        already_learned = '{}%'.format(already_learned)
        text = '熟悉的單字有: {}'.format(already_learned)

        label.config(text=text)
    else:
        return label.config(text='沒有搜尋結果')

def add_voicetube_v_to_database():
    # 提取單字資料庫的單字串列
    vpath = '/Users/justin/Desktop/Python/Python training/Project/Anki/EnglishLearner/Vacabulary/Vacabulary.xlsx'
    vdf = pd.read_excel(vpath, header=None)
    vdf = vdf.iloc[:, 0]
    vdf = vdf.values
    vdf = list(vdf)

    # 輸入Voicetube網址，抓取文章
    url = voicetubeUrl.get()
    html = requests.get(url)
    sp = bs4.BeautifulSoup(html.text, 'lxml')

    datas = sp.find_all('div', class_='caption-middle')

    # 將文章變為一個一個的單字
    lst = []
    for data in datas:
        lst.append(data.text.split('\n')[0])
    pattern = r'[a-zA-z]+'

    sen_lst = [re.findall(pattern, x.strip().lower()) for x in lst]
    word_lst = [','.join(sen) for sen in sen_lst]
    word_lst = ','.join(word_lst)
    word_lst = word_lst.replace('[','').replace(']','')
    word_lst = word_lst.split(',')
    print(word_lst)

    word_lst = list(set(word_lst)) # 處理Voicetube文章重複單字

    # 提取原資料庫的單字串列，合併（聯集）Voicetube文章單字串列，建立新單字串列
    if word_lst != [''] or []:

        new_df = list(sorted(set(word_lst + vdf)))
        new_df = pd.DataFrame(new_df)
        new_df.to_excel(vpath,header=0,index=0)
        label.config(text='單字新增成功!')

    else:
        label.config(text='沒有搜尋結果')

root=tk.Tk()
root.geometry("850x350")  #設定主視窗解析度
root.title("VacabularyKing")

btn_get_vac_from_voicetube = tk.Button(root,text='比較文章',command=compare_voictube_v_to_database)
btn_get_vac_from_voicetube.place(x=250,y=200)

btn_get_vac_from_paragraph = tk.Button(root,text='新增文章至資料庫',command=add_voicetube_v_to_database)
btn_get_vac_from_paragraph.place(x=400,y=200)

label1 = tk.Label(root,text="請輸入Voicetube網址：")
label1.place(x=40,y=100)

label =tk.Label(root,text="")
label.place(x=300,y=150)

voicetube = tk.StringVar()
paragraph = tk.StringVar()
vac = tk.StringVar()

voicetubeUrl = tk.Entry(root, textvariable=voicetube)
voicetubeUrl.config(width=40)
voicetubeUrl.place(x=200, y=100)

root.mainloop()