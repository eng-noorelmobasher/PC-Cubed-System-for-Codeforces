from PLibs import *

def showConfirm(submission,problem,verd):
    def on_close():
        top1.grab_release()
        top1.destroy()

    top1 = Toplevel()
    top1.title("Judge")
    top1.grab_set()
    top1.protocol('WM_DELETE_WINDOW', on_close)
    top1.resizable(False,False)
    top1.geometry('300x300+200+200')
    top1.configure(background="#1b1b1c")
    style = ttk.Style()
    style.configure('TFrame',background="#1b1b1c")

    frameProp = ttk.Frame(top1,padding=(0,20,0,0))
    frameProp.pack(fill=X)
    propName = Label(frameProp, text=f"Problem: {problem}",bg="#1b1b1c", fg="#dfdfe6",padx=20,font=("Arial",10,"bold"))
    propName.pack(anchor=NW)

    subID= Label(frameProp, text=f"Submission ID: {submission}",bg="#1b1b1c", fg="#dfdfe6",padx=20,font=("Arial",10,"bold"))
    subID.pack(anchor=NW,pady=30)

    if(verd == "Accepted"): verd = "Yes"
    else:
        if "Wrong" in verd:verd = "No - Wrong Answer"
        elif "Runtime" in verd: verd = "No - Runtime error"
        elif "Time limit" in verd:verd = "No - Time limit"
        elif "Memory" in verd: verd = "No - Memory limit"
        elif "Idle" in value: value = "No - Idleness limit"
    Verdict= Label(frameProp, text=verd,bg="#1b1b1c", fg=("#1cfc03" if verd=="Yes" else "red"),padx=20,font=("Arial",10,"bold"))

    Verdicttxt= Label(frameProp, text=f"Verdict: ",bg="#1b1b1c", fg="#dfdfe6",padx=20,font=("Arial",10,"bold"))
    Verdicttxt.pack(side=LEFT,anchor=NW,pady=30)
    Verdict.pack(side=LEFT,anchor=NW,pady=30)

    btn = Button(top1,text="OK",width=10,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",command=on_close)
    btn.pack(pady=20)

    top1.lift()
    top1.attributes('-topmost',True)
    top1.after_idle(top1.attributes,'-topmost',False)


def popClar(problem, question, answer):

    def on_close():
        top2.grab_release()
        top2.destroy()

    question1 = ""
    answer1 = ""
    cnt = 0
    for i in question:
        question1 += i
        cnt += 1
        if cnt > 65 and i == ' ':
            question1 += '\n'
            cnt = 0
    cnt = 0
    for i in answer:
        answer1 += i
        cnt += 1
        if cnt > 65 and i == ' ':
            answer1 += '\n'
            cnt = 0
    top2 = tk.Toplevel()
    top2.title("Judge")

    top2.protocol('WM_DELETE_WINDOW', on_close)
    top2.resizable(False, False)
    top2.geometry('800x320+200+200')
    top2.configure(background="#1b1b1c")
    style = ttk.Style()
    style.configure('TFrame', background="#1b1b1c")

    # Create a Canvas widget with scrollbars
    canvas = tk.Canvas(top2, bg="#1b1b1c", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky=tk.NSEW)

    frameProp = ttk.Frame(canvas, padding=(20, 20, 20, 0))
    frameProp.grid(row=0, column=0, sticky=tk.NSEW, pady=20)

    propName = tk.Label(frameProp, text=f"Problem: ", bg="#1b1b1c", fg="#dfdfe6", padx=20, font=("Arial", 11, "bold"))
    propName.grid(row=0, column=0, sticky=tk.NW, pady=10)
    propName = tk.Label(frameProp, text=problem, bg="#1b1b1c", fg="#dfdfe6",  font=("Arial", 11, "bold"))
    propName.grid(row=0, column=1, sticky=tk.NW, pady=10)

    subID = tk.Label(frameProp, text=f"Question: ", bg="#1b1b1c", fg="#dfdfe6", padx=20, font=("Arial", 11, "bold"))
    subID.grid(row=1, column=0, sticky=tk.NW, pady=5)
    subIDq = ttk.Label(frameProp, text=question1, background="#1b1b1c", foreground="#dfdfe6", font=("Arial", 11, "bold"),padding=(0,0,1000,0))
    subIDq.grid(row=1, column=1, sticky=tk.NW, pady=5)

    Verdicttxt = tk.Label(frameProp, text=f"Answer: ", bg="#1b1b1c", fg="#dfdfe6", padx=20, font=("Arial", 11, "bold"))
    Verdicttxt.grid(row=2, column=0, sticky=tk.NW, pady=20)
    Verdicttxtq = ttk.Label(frameProp, text=answer1, background="#1b1b1c", foreground="#dfdfe6", font=("Arial", 11, "bold"),padding=(0,0,0,0))
    Verdicttxtq.grid(row=2, column=1, sticky=tk.NW, pady=20)


    # Create a vertical scrollbar and associate it with the Canvas
    vertical_scrollbar = tk.Scrollbar(top2, command=canvas.yview)
    vertical_scrollbar.grid(row=0, column=2, sticky=tk.NS)

    # Create a horizontal scrollbar and associate it with the Canvas
    horizontal_scrollbar = tk.Scrollbar(top2, command=canvas.xview, orient=tk.HORIZONTAL)


    # Configure the Canvas to use the scrollbars
    canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    canvas.create_window(0, 0, anchor='nw', window=frameProp)

    # Update the scrollable region of the Canvas
    frameProp.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    btn = tk.Button(top2, text="OK", width=10, padx=15, background="red", fg="#dfdfe6", relief="flat", activebackground="#a10e15",
                    activeforeground="#dfdfe6", overrelief="groove", command=on_close)
    btn.grid(row=3, column=0, pady=20)
    horizontal_scrollbar.grid(row=4, column=0, sticky=tk.EW)

    top2.grid_rowconfigure(0, weight=1)
    top2.grid_columnconfigure(0, weight=1)

    top2.lift()
    top2.attributes('-topmost', True)
    top2.after_idle(top2.attributes, '-topmost', False)
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    