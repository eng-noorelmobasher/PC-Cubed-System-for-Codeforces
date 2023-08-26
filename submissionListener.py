import time
from collections import deque
from bs4 import BeautifulSoup
from tkinter import messagebox
from confirmGUI import showConfirm,popClar



def startListener(link,session):
    open('confirmed.txt','a')
    confirmed = set(i[:-1] for i in open('confirmed.txt','r').readlines())

    while True:
        time.sleep(30)
        try:
            data = session.get(f"{link}").text
        except:
            continue

        soup = BeautifulSoup(data,'html.parser')

        table = soup.find("table" , {'class':"problem-questions-table"})

        rows1 = table.find_all("td")
        res = []
        for i in rows1:
            res.append(i.text.strip())

        rows = []

        for i in range(0,len(res),5):
            tmp = []
            for j in range(5):
                st = res[i+j].split('*****')
                for c in range(len(st)):
                    st[c] = ' '.join(st[c].split('\xa0'))
                    tmp.append(st[c])
            rows.append(tmp)        
            
        for row in rows:
            if (row[2] not in confirmed) and row[-1]:
                confirmed.add(row[2])
                open('confirmed.txt','a').write(row[2]+'\n')
                if row[0]:
                    popClar(row[3],row[4],row[5])
                else:
                    popClar(row[4],row[3],row[5])

def waitForIt(link,session,subnum):        
        while True:
            time.sleep(1)
            try:
                data = session.get(f"{link}/my")
            except:
                continue

            soup = BeautifulSoup(data.text, 'html.parser')

            submissions = soup.find('table', {'class': 'status-frame-datatable'})

            rows = []
            for tr in submissions.find_all('tr')[1:]:
                row = [td.text.strip() for td in tr.find_all('td')]
                rows.append(row)
            ok = True
            for i in rows:
                if i[0] == subnum:
                    if "In queue" not in i[5] and "Running" not in i[5]:
                        ok = False
                        showConfirm(i[0],i[3],i[5])
                        break
            if ok == False:break   