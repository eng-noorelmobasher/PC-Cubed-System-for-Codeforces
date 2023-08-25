from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def submitClar(session,question,contest_link,problem,on_close):

    if len(question) == 0:
        messagebox.showerror(title="Error", message="You can't submit an empty question.")
        return

    if len(question) > 1000:
        messagebox.showerror(title="Error", message=f"At most 1000 character are allowed, you wrote {len(question)} character")
        return
           
    form_data = {}

    form_data["question"] = question
    form_data["submittedProblemIndex"] = problem
    form_data["contestId"] = contest_link[contest_link.rindex('/') + 1:]
    
    respone = session.post(f'{contest_link[:contest_link.index("/contest/")]}/data/newProblemQuestion', data=form_data)

    if(respone.status_code == 200):        
        messagebox.showinfo(title="Success!", message="Submited Successfuly")
        on_close()
        return
    else:
        messagebox.showerror(title="Failure!",message="something went wrong, try again.")

def showClar(options, session, contest_link):
    
    def on_close():
        clarWindow.grab_release()
        clarWindow.destroy()

    def insert_line_break(event):
        text = event.widget
        _, col = map(int, text.index(INSERT).split('.'))
        if col >= text['width']:
            text.insert(INSERT, '\n')

    clarWindow = Toplevel()
    clarWindow.geometry("800x430+300+300")
    clarWindow.resizable(False,False)
    clarWindow.title('PC^3')

    clarWindow.grab_set()
    clarWindow.protocol('WM_DELETE_WINDOW', on_close)

    clarWindow.configure(background="#1b1b1c")

    style2 = ttk.Style()
    style2.configure('TFrame',background="#1b1b1c")

    textFrame = ttk.Frame(clarWindow,padding=(27,30,0,0))
    textFrame.pack(anchor=NW)

    firstxt = Label(textFrame, text="Choose a problem", background="#1b1b1c", foreground="#dfdfe6", font=("Arial",10,"bold"))
    firstxt.pack(anchor=NW, side=LEFT)

    selected_option2 = StringVar()
    checkBFrame2 = ttk.Frame(clarWindow,padding=(30,10,0,0))
    checkBFrame2.pack(anchor=NW)
    # set the initial value of the variable to the first option
    selected_option2.set(options[0])
                
        
    # create the OptionMenu widget
    dropdown = ttk.Combobox(checkBFrame2, values=options, textvariable=selected_option2,width=40,state='readonly',height=10)
    dropdown.pack(side=LEFT,anchor=NW)

    frameProb = ttk.Frame(clarWindow,padding=(10,40,0,0))
    frameProb.pack(anchor=NW)
    userLab = Label(frameProb, text="Write your question here",bg="#1b1b1c", fg="#dfdfe6",padx=20,font=("Arial",10,"bold"))
    userLab.pack(side=LEFT,anchor=NW)

    frameEnt = ttk.Frame(clarWindow,padding=(30,10,0,0))
    frameEnt.pack(anchor=NW)
    # Create a Text widget

    text = Text(frameEnt, width=80, height=10, font=("Arial",11))
    text.pack(side=LEFT, anchor=NW)

    problem = selected_option2.get()[:selected_option2.get().index(':')]

    # Bind the function to the KeyPress event of the Text widget
    text.bind('<KeyPress>', insert_line_break)

    framebtn = ttk.Frame(clarWindow, padding=(0,40,0,0))
    btn = Button(framebtn,text="Submit",width=10,padx=15, background="red",fg="#dfdfe6",relief="flat",activebackground="#a10e15",activeforeground="#dfdfe6",overrelief="groove", command= lambda: submitClar(session, text.get("1.0", END).strip(), contest_link, problem, on_close))

    framebtn.pack()
    btn.pack()

    clarWindow.mainloop()
