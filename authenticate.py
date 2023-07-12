from tkinter import messagebox
from bs4 import BeautifulSoup

def check_acc(link,response,session):
    
    soup = BeautifulSoup(response, 'html.parser')
    if soup.find('div', {'class':'enterPage'}):
        messagebox.showerror(title="Error",message="Invalid username or password")
        return
    
    try:
        CLresponse = session.post(link).text
    except:
        messagebox.showerror(title="Error",message="Invalid Contest Link")
        return

    if "No such contest" in CLresponse or "Illegal contest ID" in CLresponse or "codeforces.com" not in link:
        messagebox.showerror(title="Error",message="Invalid Contest Link")
        return

    return True


