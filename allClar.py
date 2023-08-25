from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup

def ShowAllClar(session,contestLink):
    def on_close():
        topClar.grab_release()
        topClar.destroy()


    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), 'units')


    

    topClar = Toplevel()
    topClar.grab_set()
    topClar.protocol('WM_DELETE_WINDOW', on_close)
    topClar.resizable(False,False)
    topClar.geometry('800x400')
    topClar.title("Info")


    canvas = Canvas(topClar, borderwidth=0, highlightthickness=0,background="#1b1b1c")
    canvas.grid(row=0, column=0, sticky='nsew')
    
    xscrollbar = Scrollbar(topClar, orient='horizontal', command=canvas.xview)
    xscrollbar.grid(row=1, column=0, sticky='ew')


    yscrollbar = Scrollbar(topClar, orient='vertical', command=canvas.yview)
    yscrollbar.grid(row=0, column=1, sticky='ns')


    table_frame = Frame(canvas)
    table_frame.grid(row=0, column=0, sticky='nsew')

    headers = [ 'Party', "problem",'Question','Answer']

    for i, header in enumerate(headers):
        label = Label(table_frame, text=header, borderwidth=1, relief='solid',highlightbackground='#dfdfe6',background="#1b1b1c",foreground="#dfdfe6",highlightcolor="#dfdfe6",highlightthickness=1,font=("Arial",10,"bold"))
        label.grid(row=0, column=i, sticky='nsew')
        table_frame.grid_columnconfigure(i, weight=1)

    cont = session.get(contestLink).text

    soup = BeautifulSoup(cont,'html.parser')

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
    
    for i, row in enumerate(rows):
        m = 0
        for j, value in enumerate(row):
            if j == 4 or j == 5:
                res = ""
                cnt = 0
                for o in value:
                    res += o
                    cnt += 1
                    if cnt > 25 and o == " ":
                        cnt = 0
                        res += '\n'
                value = res if res else "Waiting for Judge Answer..."

            if j == 0 or j == 2:m += 1; continue
            if j == 1 and value == "": value = "Judge"

            value = '\n' + value + '\n'
            label = Label(table_frame, text=value, borderwidth=1, relief='solid', highlightbackground='#dfdfe6',background="#1b1b1c",foreground="#dfdfe6",highlightcolor="#dfdfe6",highlightthickness=1,font=("Arial",10,"bold"))
            label.grid(row=i+1, column=j - m, sticky='nsew')
            table_frame.grid_rowconfigure(i+1, weight=1)

    canvas.create_window((0, 0), window=table_frame, anchor='nw')

    table_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'), xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)

    topClar.grid_columnconfigure(0, weight=1)
    topClar.grid_rowconfigure(0, weight=1)
    topClar.geometry("{}x{}".format(table_frame.winfo_width()+15, "400"))
    
    canvas.bind_all('<MouseWheel>', on_mousewheel)    


    topClar.mainloop()

