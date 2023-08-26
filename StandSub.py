import tkinter as tk
from bs4 import BeautifulSoup

def showData(link,mode,className,session):
    def on_close():
        top2.grab_release()
        top2.destroy()


    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), 'units')

    data = session.get(f"{link}/{mode}")

    soup = BeautifulSoup(data.text, 'html.parser')

    standings_table = soup.find('table', {'class': className})


    headers = [th.text.strip() for th in standings_table.find_all('th')]


    rows = []
    for tr in standings_table.find_all('tr')[1:]:
        row = [td.text.strip() for td in tr.find_all('td')]
        rows.append(row)

    top2 = tk.Toplevel()
    top2.grab_set()
    top2.protocol('WM_DELETE_WINDOW', on_close)
    #top2.resizable(False,False)
    top2.geometry('800x400')
    top2.title("Info")
    
    if mode == "my":
        top2.geometry('500x400')
    else:
        top2.geometry('800x400')  
        top2.state('zoomed')  
    top2.configure(background="#1b1b1c")

    canvas = tk.Canvas(top2, borderwidth=0, highlightthickness=0,background="#1b1b1c")
    canvas.grid(row=0, column=0, sticky='nsew')
    
    xscrollbar = tk.Scrollbar(top2, orient='horizontal', command=canvas.xview)
    xscrollbar.grid(row=1, column=0, sticky='ew')


    yscrollbar = tk.Scrollbar(top2, orient='vertical', command=canvas.yview)
    yscrollbar.grid(row=0, column=1, sticky='ns')


    table_frame = tk.Frame(canvas)
    table_frame.grid(row=0, column=0, sticky='nsew')
    if mode == "standings":
        rows.pop()

    for i, header in enumerate(headers):
        if i < 3 and mode == "my":continue
        label = tk.Label(table_frame, text=header, borderwidth=1, relief='solid',highlightbackground='#dfdfe6',background="#1b1b1c",foreground="#dfdfe6",highlightcolor="#dfdfe6",highlightthickness=1,font=("Arial",10,"bold"))
        label.grid(row=0, column=i - (3 if mode == "my" else 0), sticky='nsew')
        table_frame.grid_columnconfigure(i - (3 if mode == "my"else 0), weight=1)



    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            if j < 3 and mode == "my":continue
            if mode == "my" and j==5:
                if(rows[i][j] == "Accepted"): value = "Yes"
                elif "Running" in value or "queue" in value: value = "NEW"
                else:
                    if "Wrong" in value:value = "No - Wrong Answer"
                    elif "Runtime" in value: value = "No - Runtime error"
                    elif "Time limit" in value:value = "No - Time limit"
                    elif "Memory" in value: value = "No - Memory limit"
                    elif "Idle" in value: value = "No - Idleness limit"
            
            if ':' in value and j > 3 and mode != "my":
                tmp = value[value.index('+') + 1:value.index('\n')]
                ans = value.index(':')
                num = str(int(str(value[ans-2] + value[ans-1])) * 60 + int(str(value[ans + 1] + value[ans + 2])))
                value = '\n' + (str(int(tmp)+1) + ' / ' + num if tmp else "1 / " + num) + '\n'

            else:
                value = '\n' + value + '\n'
            label = tk.Label(table_frame, text=value, borderwidth=1, relief='solid', highlightbackground='#dfdfe6',background="#1b1b1c",foreground="#dfdfe6",highlightcolor="#dfdfe6",highlightthickness=1,font=("Arial",10,"bold"),width = 10 if j > 3 and mode != "my" else None)
            if value != '\n\n' and ('/' in value or '+' in value) and j > 3 and mode != "my":
                if '/' in value:
                    ans = value.index('/') + 1
                    num = int(value[ans:])

                    ok = False
                    for o in range(len(rows)):
                        if ':' not in rows[o][j]:continue
                        tmp = rows[o][j]
                        ans2 = tmp.index(':')
                        num2 = int(str(tmp[ans2-2] + tmp[ans2-1])) * 60 + int(str(tmp[ans2 + 1] + tmp[ans2 + 2]))

                        if num > num2: break
                    else: ok = True
                    if not ok:
                        label.configure(background='#1cfc03',fg="black")
                    else:
                        label.configure(background='green')
                else:
                    label.configure(background='#1cfc03')
            if mode == "my" and j==5:
                if value == "\nYes\n":
                    label.configure(foreground=("#1cfc03"))
                elif "No" in value or "error" in value:
                    label.configure(foreground=("red"))
                else:
                    label.configure(foreground=("#dfdfe6"))
            if '-' in value and j > 3 and mode != "my":
                label.configure(bg="red")
            label.grid(row=i+1, column=j - (3 if mode == "my" else 0), sticky='nsew')
            table_frame.grid_rowconfigure(i+1, weight=1)



    canvas.create_window((0, 0), window=table_frame, anchor='nw')

    table_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'), xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)

    top2.grid_columnconfigure(0, weight=1)
    top2.grid_rowconfigure(0, weight=1)
    top2.geometry("{}x{}".format(table_frame.winfo_width()+15, "400"))
    
    canvas.bind_all('<MouseWheel>', on_mousewheel)

    top2.mainloop()