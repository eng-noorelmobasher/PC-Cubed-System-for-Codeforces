from PLibs import *
import images
import threading

global contestLink
global username
global password
global ok

def login(contestLink,username,password):
    username = userEntry.get()
    password = passEntry.get()
    contestLink = CLEntry.get()
    login_data = {
        'action': 'enter',
        'handleOrEmail': username,
        'password': password,
        'remember': 'on',
        '_tta': '135'
    }
    global session
    session = requests.Session()
    response = session.post('https://codeforces.com/enter', data=login_data).content
    


    if contestLink[-1] == '/':
        contestLink = ''.join(list(contestLink)[:-1])
    res = check_acc(contestLink, response, session)
    if not res:
        return
    
    if ok==False:
        file = open("UP.txt","w")
        file.write(f"{username},{password}")
        file.close()   

    thread = threading.Thread(target=lambda: startListener(contestLink,session))
    thread.daemon = True
    thread.start()
    
    frameCred.destroy()
    frameCredCL.destroy()
    frameCredPass.destroy()
    btn.destroy()
    community_photo.forget()

    btnCFrame = ttk.Frame(root)
    btnCFrame.pack(expand=0,anchor=NW)
    statusBtn = Button(btnCFrame,text="Show My Submissions",width=20,padx=0, background="red",fg="white",relief="flat",activebackground="#a10e15",activeforeground="white",overrelief="groove",bd=0,command=lambda: showData(contestLink,'my','status-frame-datatable',session))
    standingBtn = Button(btnCFrame,text="Show Standing",width=10,padx=15, background="red",fg="white",relief="flat",activebackground="#a10e15",activeforeground="white",overrelief="groove",bd=0,command=lambda: showData(contestLink,'standings','standings',session))
    statusBtn.pack(side=LEFT,anchor=NW)
    standingBtn.pack(side=LEFT,anchor=NW)
    global selected_option
    selected_option = StringVar()

    options = getProblemNames(contestLink,session)
    
    for i in range(len(options)//2):
        prefix = options.pop(0)
        suffix = options.pop(0)
        options.append(f"{prefix}: {suffix}")

    checkBFrame = ttk.Frame(root,padding=(30,30,0,0))
    checkBFrame.pack(anchor=NW)
    # set the initial value of the variable to the first option
    selected_option.set(options[0])
                
                
    # create the OptionMenu widget
    dropdown = ttk.Combobox(checkBFrame, values=options, textvariable=selected_option,width=40,state='readonly',height=10)
    dropdown.pack(side=LEFT,anchor=NW)
    fileLab = Label(checkBFrame, text='',bg="#12062e",fg="white",font=("Arial",10))
    def getFileSub():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[('Python Files', '*.py'), ('CPP Files', '*.cpp'), ('Java Files', '*.java')])
        finalSubBtn.configure(state="active")
        if file_path:
            fileLab.config(text=file_path[file_path.rindex('/'):])
            getFilebutton.forget()
            fileLab.pack(side=RIGHT)
            getFilebutton.pack(side=RIGHT,anchor=NE,padx=30)

    getFilebutton = Button(checkBFrame,text="Choose a File to Submit",width=15,padx=15, background="red",fg="white",relief="flat",activebackground="#a10e15",activeforeground="white",overrelief="groove",bd=0, command=getFileSub)
    getFilebutton.pack(side=RIGHT,anchor=NE,padx=30)

    framFinalSub = ttk.Frame(root,padding=(30,30,0,165))
    framFinalSub.pack(anchor=NW)

    finalSubBtn = Button(framFinalSub,text="Submit",width=10,padx=20, background="red",fg="white",relief="flat",activebackground="#a10e15",activeforeground="white",overrelief="groove",bd=0,command=lambda: submutSolution(contestLink,session,selected_option.get()[:selected_option.get().index(':')],file_path),state="disabled")
    finalSubBtn.pack(side=LEFT,anchor=NW)    

    community_photo.pack(side=RIGHT, anchor="se",padx=10,pady=0,expand=False, fill="y")
root = Tk()
root.geometry("800x430+300+300")
root.resizable(False,False)
root.title('PC^3')

root.configure(background="#12062e")

welcome = Label(root, text="Welcome to PC^3 judgement system.",fg="white",bg="#12062e")
welcome.pack(anchor=NW)

style = ttk.Style()
style.configure('TFrame',background="#12062e")
frameCred = ttk.Frame(root,padding=(0,80,0,0))
frameCred.pack()
userLab = Label(frameCred, text="Username: ",bg="#12062e", fg="white",padx=20,font=("Arial",10,"bold"))
userEntry = Entry(frameCred,width=40,font=("Arial",10), relief="flat")
userLab.pack(side=LEFT,anchor=N)
userEntry.pack(side=RIGHT,anchor=N)

frameCredPass = ttk.Frame(root,padding=(0,20,0,0))
frameCredPass.pack()
passLab = Label(frameCredPass, text="Password: ",bg="#12062e", fg="white",padx=20,font=("Arial",10,"bold"))
passEntry = Entry(frameCredPass,width=40,font=("Arial",10),show="*",relief="flat")
passLab.pack(side=LEFT,anchor=N,fill=X,padx=2)
passEntry.pack(side=RIGHT,anchor=N,fill=X)
ok = True
try:
    cred = open("UP.txt","r")
    user,passw = cred.readline().split(',')
    userEntry.insert(END, user)
    passEntry.insert(END,passw)
except:
    ok = False

frameCredCL = ttk.Frame(root,padding=(0,20,0,0))
frameCredCL.pack()
CLLab = Label(frameCredCL, text="Contest Link: ",bg="#12062e", fg="white",padx=12,font=("Arial",10,"bold"))
CLEntry = Entry(frameCredCL,width=40,font=("Arial",10),relief="flat")
CLLab.pack(side=LEFT,anchor=N,fill=X)
CLEntry.pack(side=RIGHT,anchor=N,fill=X)



btn = Button(root,text="Login",width=10,padx=15, background="red",fg="white",relief="flat",activebackground="#a10e15",activeforeground="white",overrelief="groove",command=lambda: login(CLEntry.get(),userEntry.get(),passEntry.get()))
btn.pack(pady=40,padx=100)
img = PhotoImage(data=images.image_acpc_base64)
community_photo = Label(root, image=img,background="#12062e",width=150,height=150)
community_photo.pack(side=RIGHT,anchor="se",padx=10,pady=0,expand=False,fill="y")
root.mainloop()