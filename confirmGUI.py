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