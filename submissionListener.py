import time
from collections import deque
from bs4 import BeautifulSoup
from tkinter import messagebox
from confirmGUI import showConfirm

dates = deque()
def startListener(link,session):
        while True:
            time.sleep(1)
            if dates:
                date = dates.popleft()
                try:
                    data = session.get(f"{link}/my")
                except:
                    dates.appendleft(date)
                    continue

                soup = BeautifulSoup(data.text, 'html.parser')

                submissions = soup.find('table', {'class': 'status-frame-datatable'})

                rows = []
                for tr in submissions.find_all('tr')[1:]:
                    row = [td.text.strip() for td in tr.find_all('td')]
                    rows.append(row)
                    break

                subnum = rows[0][0]

                waitForIt(link,session,subnum)


def waitForIt(link,session,subnum):        
        while True:
            time.sleep(1)
            data = session.get(f"{link}/my")
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