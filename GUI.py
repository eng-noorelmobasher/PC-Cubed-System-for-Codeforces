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
    global session
    session = requests.Session()
    submission_page = session.get(f"https://codeforces.com/enter").content
    soup = BeautifulSoup(submission_page, 'html.parser')
    form_data = {}
    for field in ['csrf_token' ]:
        field_value = soup.find('input', {'name': field}).get('value', '')

        form_data[field] = field_value
        
    headers = {
        'X-Csrf-Token': form_data['csrf_token']
    }
    login_data = {
        'csrf_token': form_data['csrf_token'],
        'action': 'enter',
        'handleOrEmail': username,
        'password': password,
        'remember': 'on',
        '_tta': '135'
    }


    response = session.post('https://codeforces.com/enter', data=login_data,headers=headers).content
    
    open('errr.txt','wb').write(response)

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
    print(contestLink)
    frameCred.destroy()
    frameCredPass.destroy()
    btn.destroy()
    community_photo.forget()

    btnCFrame = ttk.Frame(root)
    btnCFrame.pack(expand=0,anchor=NW)
    statusBtn = Button(btnCFrame,text="Show My Submissions",width=20,padx=0, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",bd=0,command=lambda: showData(contestLink,'my','status-frame-datatable',session))   
    standingBtn = Button(btnCFrame,text="Show Standing",width=10,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",bd=0,command=lambda: showData(contestLink,'standings','standings',session))
    reqClar = Button(btnCFrame,text="Submit a Clarification",width=20,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",bd=0, command=lambda :showClar(options, session, contestLink)) 
    shClar = Button(btnCFrame,text="Show Clarifications",width=20,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",bd=0, command=lambda :ShowAllClar(session,contestLink)) 
    downPdf = Button(btnCFrame,text="Download Statements",width=20,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",bd=0, command=getStatments)  
    statusBtn.pack(side=LEFT,anchor=NW)
    standingBtn.pack(side=LEFT,anchor=NW)
    reqClar.pack(side=LEFT, anchor=NW)
    shClar.pack(side=LEFT, anchor=NW)
    downPdf.pack(side=LEFT, anchor=NW)
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
    fileLab = Label(checkBFrame, text='',bg="#1b1b1c",fg="#dfdfe6",font=("Arial",10))
    def getFileSub():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[('Python Files', '*.py'), ('CPP Files', '*.cpp'), ('Java Files', '*.java')])
        finalSubBtn.configure(state="active")
        if file_path:
            fileLab.config(text=file_path[file_path.rindex('/'):])
            getFilebutton.forget()
            fileLab.pack(side=RIGHT)
            getFilebutton.pack(side=RIGHT,anchor=NE,padx=30)

    getFilebutton = Button(checkBFrame,text="Choose a File to Submit",width=15,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",bd=0, command=getFileSub)
    getFilebutton.pack(side=RIGHT,anchor=NE,padx=30)

    framFinalSub = ttk.Frame(root,padding=(30,30,0,165))
    framFinalSub.pack(anchor=NW)

    finalSubBtn = Button(framFinalSub,text="Submit",width=10,padx=20, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",bd=0,command=lambda: submutSolution(contestLink,session,selected_option.get()[:selected_option.get().index(':')],file_path),state="disabled")
    finalSubBtn.pack(side=LEFT,anchor=NW)    

    community_photo.pack(side=RIGHT, anchor="se",padx=10,pady=0,expand=False, fill="y")

contestLink = getContestLink()
if not contestLink:
    exit()
open('temp.txt', 'w').write("Nothing Here..")
root = Tk()
root.geometry("800x430+300+300")
root.resizable(False,False)
root.title('PC^3')

root.configure(background="#1b1b1c")

welcome = Label(root, text="Welcome to PC^3 judgement system.",fg="#dfdfe6",bg="#1b1b1c")
welcome.pack(anchor=NW)

style = ttk.Style()
style.configure('TFrame',background="#1b1b1c")
frameCred = ttk.Frame(root,padding=(0,120,0,0))
frameCred.pack()
userLab = Label(frameCred, text="Username: ",bg="#1b1b1c", fg="#dfdfe6",padx=20,font=("Arial",10,"bold"))
userEntry = Entry(frameCred,width=40,font=("Arial",10), relief="flat")
userLab.pack(side=LEFT,anchor=N)
userEntry.pack(side=RIGHT,anchor=N)

frameCredPass = ttk.Frame(root,padding=(0,20,0,0))
frameCredPass.pack()
passLab = Label(frameCredPass, text="Password: ",bg="#1b1b1c", fg="#dfdfe6",padx=20,font=("Arial",10,"bold"))
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


btn = Button(root,text="Login",width=10,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove",command=lambda: login(contestLink,userEntry.get(),passEntry.get()))
btn.pack(pady=40,padx=100)
img = PhotoImage(data=images.image_acpc_base64)
community_photo = Label(root, image=img,background="#1b1b1c",width=150,height=150)
community_photo.pack(side=RIGHT,anchor="se",padx=10,pady=0,expand=False,fill="y")
root.mainloop()