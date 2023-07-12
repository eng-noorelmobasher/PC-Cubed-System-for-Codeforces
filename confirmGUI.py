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
    top1.configure(background="#12062e")
    style = ttk.Style()
    style.configure('TFrame',background="#12062e")

    frameProp = ttk.Frame(top1,padding=(0,20,0,0))
    frameProp.pack(fill=X)
    propName = Label(frameProp, text=f"Problem: {problem}",bg="#12062e", fg="white",padx=20,font=("Arial",10,"bold"))
    propName.pack(anchor=NW)

    subID= Label(frameProp, text=f"Submission ID: {submission}",bg="#12062e", fg="white",padx=20,font=("Arial",10,"bold"))
    subID.pack(anchor=NW,pady=30)

    Verdict= Label(frameProp, text=verd,bg="#12062e", fg=("#1cfc03" if verd=="Accepted" else "red"),padx=20,font=("Arial",10,"bold"))

    Verdicttxt= Label(frameProp, text=f"Verdict: ",bg="#12062e", fg="white",padx=20,font=("Arial",10,"bold"))
    Verdicttxt.pack(side=LEFT,anchor=NW,pady=30)
    Verdict.pack(side=LEFT,anchor=NW,pady=30)

    btn = Button(top1,text="OK",width=10,padx=15, background="red",fg="white",relief="flat",activebackground="#a10e15",activeforeground="white",overrelief="groove",command=on_close)
    btn.pack(pady=20)

