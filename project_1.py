from tkinter import Tk,Label,Frame,Entry,Button,messagebox,simpledialog,StringVar,Radiobutton,Toplevel
from tkcalendar import Calendar
from tkinter.ttk import Combobox
from datetime import datetime   
import time
import tables
import generator_capture
tables.create_tables()
from PIL import Image,ImageTk


import sqlite3
import mail

# #welcome Page degined
# wel=Tk()
# wel.state('zoomed')
# wel.configure(bg='powder blue')
# wel.title("Banking system")

# fst_lable=Label(wel,text="Welcome to My first page",font=("Arial",35,'italic'),bg='powder blue')
# fst_lable.pack(expand=True)

# emozie=''
# def animation():
#     global emozie
#     emozie+='👉'
#     if len(emozie) >5:
#         emozie=""
#     fst_lable.config(text="Welcome to My first page" + emozie)
#     fst_lable.after(1000,animation)

# animation()
# wel.after(4000,wel.destroy)
# wel.mainloop()




root=Tk()
root.state("zoomed")
root.title("Banking System")
root.configure(bg="powder blue")


#create a function for update time every 1000 milisecond(1 sec) using time module .strftime
def update_time():
    currentTime=time.strftime("%d-%m-%Y %r")
    date_labl.configure(text=currentTime)
    root.after(1000,update_time)

#create a hading for this project    
head_lbl=Label(root,text="Banking simulator" ,font=('arial',50,'underline','bold'),background='powder blue')
head_lbl.pack()

#create a udated time and date every second for this project    
currentTime=time.strftime("%d-%m-%Y %r")
date_labl=Label(root,text=currentTime,font=('arial',20,'underline','bold'),background='powder blue')
date_labl.pack()

#show image in topLevel before date and title
imag=Image.open("bg.jpg").resize((200,180))# load the image from local file 
imageTk=ImageTk.PhotoImage(imag,master=root) #find where are show the image when are excute when from root windwo
imageLable=Label(root,image=imageTk) #create a lable for showing image
imageLable.place(relx=.0,rely=.0)


#create a fotter lable text for this project
fotter_labl=Label(root,text="ARBAJ ALI \n MOB:-7541063076",font=("Arial",15,'bold'),bg='powder blue')
fotter_labl.pack(side='bottom',pady=10)

#create a function for forget sreen when user click on forgot button then open this screen
def forgot_screen():
    
    #create a function for destroy this frame and call main screen like back button 
    def Back():
        frm.destroy()
        main_screen()
    
    def show_otp_forgot():
        account=AcnEntry.get()
        email=EmailEntry.get()
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select name,email,pass from accounts where acn=? and email=?",(account,email))
        tup=curobj.fetchone()
        conobj.close()
        
        if tup!=None:
            otp=generator_capture.forgot_otp()
            text=f"hello {tup[0]} \n please send otp for forgot = {otp}"
            mail.frogot_otp_mail(tup[1],text)
            messagebox.showinfo("forgot","shoe the forgot password")
            n=3
            for i in range(n+1):
                user_otp=simpledialog.askinteger("forgot","forgot otp")
                if otp==user_otp:
                    messagebox.showinfo("password",tup[2])
                    break
                else:
                    messagebox.showerror("error",f'Invalid otp! try again {n-1} left')
        else:
            messagebox.showerror("forgot","Invalid deatails")
   
    
    #fram for forgot Screen  
    frm=Frame(root,background='pink',highlightbackground='black',highlightthickness=2)
    frm.place(relx=0,rely=.17,relheight=.75,relwidth=1)
    
    back_btn=Button(frm,text='Back',font=("Arial",15,'bold'),bd=2,bg="powder blue",command=Back)
    back_btn.place(relx=0,rely=0)
    
    title_fram=Label(frm,text='forgot password',font=("Arial",25),bg='pink',fg='green')
    title_fram.pack(pady=25)
    
    Acnlbl=Label(frm,text="Account", font=("Arial",15,'bold'),bg="pink")
    Acnlbl.place(relx=.35,rely=.2)
    
    AcnEntry=Entry(frm,font=("Arial",15,'bold'))
    AcnEntry.place(relx=.45,rely=.2,relwidth=.20,height=30)
    AcnEntry.focus()
    
    Emaillbl=Label(frm,text="Email Id", font=("Arial",15,'bold'),bg="pink")
    Emaillbl.place(relx=.35,rely=.3)
    
    EmailEntry=Entry(frm,font=("Arial",15,'bold'))
    EmailEntry.place(relx=.45,rely=.3,relwidth=.20,height=30)
    
    submit_btn=Button(frm,text='Send OTP',font=("Arial",15,'bold'),bd=2,bg="powder blue",command=show_otp_forgot)
    submit_btn.place(relx=.57,rely=.4)   
    
    







#######################################################main screen #######################################################
def main_screen():
    
    #create a function for refres capture
    def refres():
        global capture
        capture=generator_capture.random_capture()
        capllbl.configure(text=capture)
    
    #create a function for forgot screen open    
    def frogot():
        frm.destroy()
        forgot_screen()
        
    # create a function for login button with given a message box if we dont't select any option
    def login_button():
        if user_combobox.get() == '--select--':
            messagebox.showerror("Error", "Please select user type")
            return
        elif AcnEntry.get() == 0:
            messagebox.showerror("Warning", "Please fill account number")
            return
        elif not AcnEntry.get().isdigit():
            messagebox.showerror("Warning", "Account number must be numeric")
            return
        elif passEntry.get() == "":
            messagebox.showerror("Warning","please fill password")
            return
        elif cap_entry.get() == "":
            messagebox.showerror("Warning","please fill Capture")
            return
        else:
            print("All Done welcome in Bank Simulation 👉")
        
        
        ucn=AcnEntry.get()
        upass=passEntry.get()
        
        global capture
        ucap=cap_entry.get()
        capture=capture.replace(" ","")
        if ucap!=capture:
            messagebox.showerror("Login",'Invalid capture')
            return
        
        if user_combobox.get()  == "Admin":
            if ucn=="0" and upass=="arbaj":
                frm.destroy()
                Admin_screen()
            else:
                messagebox.showinfo("login","invalid credantials")
        elif user_combobox.get() == 'User':
            cononj=sqlite3.connect(database='bank.sqlite')
            curobj=cononj.cursor()
            query="select * from accounts where acn=? and pass==?"
            curobj.execute(query,(ucn,upass))
            tup=curobj.fetchone()
            cononj.close()
            if tup!=None:
                frm.destroy()
                User_screen(ucn)
            else:
                messagebox.showinfo("login","invalid credantials")    
                
                         
    def reset():
        user_combobox.delete(0)
        AcnEntry.delete(0,'end')
        passEntry.delete(0,'end')
        cap_entry.delete(0,'end')
        
    # create a frame for main screen       
    frm=Frame(root,background="pink",bd=2,highlightbackground='black',highlightthickness=1)
    frm.place(relx=0,rely=.17,relheight=0.75,relwidth=1)

    #for title 
    frm_title_lable=Label(frm, text="login Area", font=("Arial", 25), bg="pink",fg='green')
    frm_title_lable.pack(pady=25)
    
    userlbl=Label(frm,text="USER TYPE", font=("Arial",15,'bold'),bg="pink")
    userlbl.place(relx=.35,rely=.2)
    
    user_combobox=Combobox(frm,values=['--select--','Admin','User'],font=('Arial',20,'bold'),state='readonly')
    user_combobox.place(relx=.45,rely=.2,relwidth=.20)
    user_combobox.current(0)
    
    Acnlbl=Label(frm,text="Account", font=("Arial",15,'bold'),bg="pink")
    Acnlbl.place(relx=.35,rely=.3)
    
    AcnEntry=Entry(frm,font=("Arial",15,'bold'))
    AcnEntry.place(relx=.45,rely=.3,relwidth=.20,height=30)
    AcnEntry.focus()
    
    passllbl=Label(frm,text="PASSWORD", font=("Arial",15,'bold'),bg="pink")
    passllbl.place(relx=.35,rely=.4)
    
    passEntry=Entry(frm,font=("Arial",15,'bold'),show="*")
    passEntry.place(relx=.45,rely=.4,relwidth=.20,height=30)

    global capture
    capture=generator_capture.random_capture()
    capllbl=Label(frm,text=capture, font=("Segoe UI",15,'italic'),bg="gray",highlightbackground='black',highlightthickness=1)
    capllbl.place(relx=.51,rely=.5,relwidth=.10)
    
    ref_btn=Button(frm,text="🔄",font=("Arial",15,'bold'),bd=2,command=refres)
    ref_btn.place(relx=.62,rely=.5,relheight=.06)
    
    cap_type_lable=Label(frm,text='Type Capture',font=("Arial",13,'italic'))
    cap_type_lable.place(relx=.47,rely=.6)
    
    cap_entry=Entry(frm,font=("Arial",15,'italic'),bd=2,background='gray')
    cap_entry.place(relx=.55,rely=.6,relwidth=.1)

    login_btn=Button(frm,text='Login',font=("Arial",15,'bold'),bd=2,bg="powder blue",command=login_button)
    login_btn.place(relx=.46,rely=.68,relwidth=.08,)   
    
    reset_btn=Button(frm,text='Reset',font=("Arial",15,'bold'),bd=2,bg="powder blue",command=reset)
    reset_btn.place(relx=.56,rely=.68,relwidth=.08)   
    
    forgot_btn=Button(frm,text='Forgot password',font=("Arial",15,'bold'),bd=2,bg="powder blue",command=frogot)
    forgot_btn.place(relx=.45,rely=.77,relwidth=.2) 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    
   ####################################################Admin screen ######################################################################
#create a function for admin screen and create a frame inside the frame for  new acc and view and close account
def Admin_screen():
    def logout():
        frm.destroy()
        main_screen()
        
    frm=Frame(root,background="pink",bd=2,highlightbackground='black',highlightthickness=1)
    frm.place(relx=0,rely=.17,relheight=0.75,relwidth=1)
    
    Admin_welcome_lable=Label(frm,text=f"Welcome ?",font=("Arial",15,'italic'))
    Admin_welcome_lable.place(relx=.01,rely=.02)
    
    logout_btn=Button(frm,text='Logout',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=logout)
    logout_btn.place(relx=.9,rely=0)
    
    def New():
        def reset():
            name_Entry.delete(0,'end')
            email_Entry.delete(0,'end')
            Adhar_Entry.delete(0,'end')
            mob_Entry.delete(0,'end')
            dob_Entry.delete(0,'end')
            Adress_entry.delete(0,'end')    
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.03,rely=.23,relheight=.7,relwidth=.94)
        
        def open_acn():
            name=name_Entry.get()
            email=email_Entry.get()
            dob= dob_Entry.get()
            mob=mob_Entry.get()
            adhar=Adhar_Entry.get()
            adress=Adress_entry.get()
            bal=0
            opendate=time.strftime("%d-%b-%Y %r")
            pwd=generator_capture.random_password()
            gender=gender_string.get()
            # print(gender)
            
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(name,pwd,email,bal,mob,adhar,opendate,adress,dob,gender))
            conobj.commit()
            conobj.close()
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select max(acn) from accounts"
            curobj.execute(query)
            acn=curobj.fetchone()[0]
            conobj.close()
             
            text=f"""
            welcome {name},
            we have successfully opend your account in pnb bank
            this is your credendials
            acn={acn}
            pass={pwd}
            """
            mail.openanc_mail(email,text)
            messagebox.showinfo("Account open","we have open account")
            
        new_title_lable=Label(ifrm, text="fill the form for open new account", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)
    
        name_lbl=Label(ifrm,text='Full name', font=("Arial",15,'bold'),bg="white")
        name_lbl.place(relx=.1,rely=.1)
        
        name_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        name_Entry.place(relx=.1,rely=.18,relwidth=.20,height=40)
        name_Entry.focus()
                
        email_lbl=Label(ifrm,text="email id", font=("Arial",15,'bold'),bg="white")
        email_lbl.place(relx=.4,rely=.1)
        
        email_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        email_Entry.place(relx=.4,rely=.18,relwidth=.20,height=40)
        
        mob_lbl=Label(ifrm,text="Mobile Number", font=("Arial",15,'bold'),bg="white")
        mob_lbl.place(relx=.7,rely=.1)
        
        mob_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        mob_Entry.place(relx=.7,rely=.18,relwidth=.20,height=40)
        
        Adhar_lbl=Label(ifrm,text="Adhar Number", font=("Arial",15,'bold'),bg="white")
        Adhar_lbl.place(relx=.1,rely=.29)
        
        Adhar_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        Adhar_Entry.place(relx=.1,rely=.37,relwidth=.20,height=40)
 
        dob_lbl=Label(ifrm,text="DOB", font=("Arial",15,'bold'),bg="white")
        dob_lbl.place(relx=.4,rely=.29)
        
        dob_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        dob_Entry.place(relx=.4,rely=.37,relwidth=.20,height=40)
        
        gender_lbl=Label(ifrm,text="Gender", font=("Arial",15,'bold'),bg="white")
        gender_lbl.place(relx=.7,rely=.29)
        
        gender_string=StringVar()
        gender_string.set('male')
        Radiobutton(ifrm,text='Male',font=("Arial",15),bg='white',value='male',variable=gender_string).place(relx=.7,rely=.37)
        Radiobutton(ifrm,text='Female',font=("Arial",15),bg='white',value='female',variable=gender_string).place(relx=.8,rely=.37)
        Radiobutton(ifrm,text='Other',font=("Arial",15),bg='white',value='other',variable=gender_string).place(relx=.9,rely=.37)
        
        Adress_lbl=Label(ifrm,text="Adress", font=("Arial",15,'bold'),bg="white")
        Adress_lbl.place(relx=.1,rely=.47)
        
        Adress_entry=Entry(ifrm,font=("Arial",20,'bold'),bd=3,highlightcolor='gray',highlightthickness=3)
        Adress_entry.place(relx=.1,rely=.53,relheight=.3,relwidth=.8)  
        
        open_btn=Button(ifrm,text='open Account',font=("Arial",15,'bold'),bd=2,bg="white",command=open_acn)
        open_btn.place(relx=.35,rely=.87,relwidth=.2) 
        
        reset_btn=Button(ifrm,text='reset',font=("Arial",15,'bold'),bd=2,bg="white",command=reset)
        reset_btn.place(relx=.6,rely=.87,relwidth=.2)

    def view():
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.03,rely=.23,relheight=.7,relwidth=.94)

        new_title_lable=Label(ifrm, text="view your personal account", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)
        
        user_acc_number=simpledialog.askinteger("view your account",'please enter your currect account number')
          
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(user_acc_number,))
        tup=curobj.fetchone()
        conobj.close()
        if tup!=None:
            messagebox.showinfo("dtails",tup)
        else:
            messagebox.showerror("Details",'Acount does not exists')
            
            

    def close():
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.03,rely=.23,relheight=.7,relwidth=.94)

        new_title_lable=Label(ifrm, text="close your available account", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)
        
        user_acc_number=simpledialog.askinteger("close account",'please enter your currect account number')
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query="select name,email from accounts where acn=?"
        curobj.execute(query,(user_acc_number,))
        tup=curobj.fetchone()
        print(tup[1])
        conobj.close()
        if tup!=None:
            otp=generator_capture.close_otp()
            text=f"hello {tup[0]} \n OTP to close your account: {otp}"
            mail.close_otp_mail(tup[1],text)
            messagebox.showinfo("close","we have to send otp for close account")
            uotp=simpledialog.askinteger("close otp",'otp')
            if otp==uotp:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query="delete from accounts where acn=?"
                curobj.execute(query,(user_acc_number,))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("close","Account close")
            else:
                messagebox.showinfo("show error","invalid otp")
        else:
            messagebox.showerror("close","Account does not exist")
        
    new_btn=Button(frm,text='New Account',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=New)
    new_btn.place(relx=.08,rely=.1,relwidth=.2) 

    view_btn=Button(frm,text='View Account',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=view)
    view_btn.place(relx=.41,rely=.1,relwidth=.2) 
    
    close_btn=Button(frm,text='Close Account',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=close)
    close_btn.place(relx=.78,rely=.1,relwidth=.2) 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    

# ****************************************user screen****************************************************
def User_screen(ucn):
    def logout():
        frm.destroy()
        main_screen()
        
    frm=Frame(root,background="pink",bd=2,highlightbackground='black',highlightthickness=1)
    frm.place(relx=0,rely=.17,relheight=0.72,relwidth=1)

    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("select name from accounts where acn=?",(ucn,))
    name=curobj.fetchone()[0]
    
    user_welcome_lable=Label(frm,text=f"Welcome {name}",font=("Arial",15,'italic'),bg='pink')
    user_welcome_lable.place(relx=.0,rely=.0)
    
    logout_btn=Button(frm,text='Logout',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=logout)
    logout_btn.place(relx=.9,rely=0) 
    
    def show():
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.25,rely=.1,relheight=.75,relwidth=.6)

        new_title_lable=Label(ifrm, text="your pesonal details", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from accounts where acn=?",(ucn,))
        tup=curobj.fetchone()
        conobj.close()
        
        text=f"""
Acount number ={tup[0]}

Holder name={tup[1]}

Acount Gmail ={tup[3]}

Acount balance ={tup[4]}

Acount mobile ={tup[5]}

Acount adhar ={tup[6]}
"""
        infolable=Label(ifrm,text=text,font=("Arial",15,'bold'),bg='white').place(relx=.2,rely=.1)
        
    def Edit():
        
        def reset():
            name_Entry.delete(0,'end')
            email_Entry.delete(0,'end')
            mob_Entry.delete(0,'end')
            pass_Entry.delete(0,'end')
                
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.25,rely=.1,relheight=.75,relwidth=.6)
        
        new_title_lable=Label(ifrm, text="Update your pesonal details", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)
    
    
    
        def update():
            name=name_Entry.get()
            email=email_Entry.get()
            mob=mob_Entry.get()
            pwd=pass_Entry.get()
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("update accounts set name=?,email=?,mob=?,pass=? where acn=?",(name,email,mob,pwd,ucn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("update","your infrormation is update successfully")
            
            
        name_lbl=Label(ifrm,text='Full name', font=("Arial",15,'bold'),bg="white")
        name_lbl.place(relx=.15,rely=.13)
        
        name_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        name_Entry.place(relx=.15,rely=.22,relwidth=.25,height=40)
        name_Entry.focus()

        email_lbl=Label(ifrm,text="email id", font=("Arial",15,'bold'),bg="white")
        email_lbl.place(relx=.44,rely=.13)
        
        email_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        email_Entry.place(relx=.44,rely=.22,relwidth=.25,height=40)
        
        mob_lbl=Label(ifrm,text="Mobile Number", font=("Arial",15,'bold'),bg="white")
        mob_lbl.place(relx=.15,rely=.45)
        
        mob_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        mob_Entry.place(relx=.15,rely=.54,relwidth=.25,height=40)
        
        pass_lbl=Label(ifrm,text="password", font=("Arial",15,'bold'),bg="white")
        pass_lbl.place(relx=.44,rely=.45)
        
        pass_Entry=Entry(ifrm,font=("Arial",13,'bold'),bd=2,highlightcolor='gray')
        pass_Entry.place(relx=.44,rely=.54,relwidth=.25,height=40)
            
        open_btn=Button(ifrm,text='update & save',font=("Arial",15,'bold'),bd=2,bg="white",command=update)
        open_btn.place(relx=.35,rely=.87,relwidth=.2) 
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        curobj.execute("select name,email,mob,pass from accounts where acn=?",(ucn,))
        tup=curobj.fetchone()
        curobj.close()
        name_Entry.insert(0,tup[0])
        email_Entry.insert(0,tup[1])
        mob_Entry.insert(0,tup[2])
        pass_Entry.insert(0,tup[3])
        
        reset_btn=Button(ifrm,text='reset',font=("Arial",15,'bold'),bd=2,bg="white",command=reset)
        reset_btn.place(relx=.6,rely=.87,relwidth=.2)

    def deposite():
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.25,rely=.1,relheight=.75,relwidth=.6)

        new_title_lable=Label(ifrm, text="add ammount", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)
        
        user_ammount=simpledialog.askinteger("Enter your amount",'Deposite amount')
        if user_ammount==None:
            return
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("update accounts set bal=bal+? where acn=?",(user_ammount,ucn))
        conobj.commit()
        conobj.close()
        
        
        #INSERT TRANSACTION RECORD
        date = time.strftime("%Y-%m-%d")
        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute(
            "INSERT INTO transactions VALUES(null,?,?,?,?,null)",
            (ucn, "DEPOSIT", user_ammount, date)
        )
        conobj.commit()
        conobj.close()
        messagebox.showinfo("deposite",f"deposite succefully {user_ammount}")
        
        

    def withdraw():
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.25,rely=.1,relheight=.75,relwidth=.6)

        new_title_lable=Label(ifrm, text="withdraw ammount on your account", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)

        user_withdraw_amt=simpledialog.askinteger("Enter your amount","withdraw ammount")
        if user_withdraw_amt==None:
            return
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select bal from accounts where acn=?",(ucn,))
        tup=curobj.fetchone()[0]
        conobj.close()
        
        if tup>=user_withdraw_amt:
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("update accounts set bal=bal-? where acn=?",(user_withdraw_amt,ucn))
            conobj.commit()
            conobj.close()
            
                        # ---- SAVE TRANSACTION ----
            date = time.strftime("%Y-%m-%d")
            conobj = sqlite3.connect("bank.sqlite")
            curobj = conobj.cursor()
            curobj.execute(
                "INSERT INTO transactions VALUES(null,?,?,?,?,null)",
                (ucn, "WITHDRAW", user_withdraw_amt, date)
            )
            conobj.commit()
            conobj.close()
            messagebox.showinfo("withdarw",f"deposite succefully {user_withdraw_amt}")
        else:
            messagebox.showinfo("widraw",f"insufficient balance")
            
    
    def transfer():
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.25,rely=.1,relheight=.75,relwidth=.6)

        new_title_lable=Label(ifrm, text="transfer ammount", font=("Arial", 25), bg="white",fg='gray')
        new_title_lable.pack(pady=5)
        
        to_account_number=simpledialog.askinteger("To acn","to account number")
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from accounts where acn=?",(to_account_number,))
        tup=curobj.fetchone()
        conobj.close()
        if tup != None:
            user_amt=simpledialog.askinteger("ammount","transfer ammount")
            if user_amt==None:
                return
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("select bal from accounts where acn=?",(ucn,))
            bal=curobj.fetchone()[0]
            conobj.close()
            if bal>=user_amt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute("update accounts set bal=bal-? where acn=?",(user_amt,ucn))
                curobj.execute("update accounts set bal=bal+? where acn=?",(user_amt,to_account_number))
                conobj.commit()
                conobj.close()
                
                date = time.strftime("%Y-%m-%d")
                conobj = sqlite3.connect("bank.sqlite")
                curobj = conobj.cursor()
                # sender
                curobj.execute(
                    "INSERT INTO transactions VALUES(null,?,?,?,?,null)",
                    (ucn, "TRANSFER-OUT", user_amt, date)
                )
                # receiver
                curobj.execute(
                    "INSERT INTO transactions VALUES(null,?,?,?,?,null)",
                    (to_account_number, "TRANSFER-IN", user_amt, date)
                )
                conobj.commit()
                conobj.close()

                messagebox.showinfo("withdarw",f"transfer succefully {user_amt} to {to_account_number}")
            else:
        
                messagebox.showinfo("widraw",f"insufficient balance")
        else:
            messagebox.showerror("acount","account does not exist")    

    def ministatment():

        def reset():
            from_entry.delete(0,'end')
            to_entry.delete(0,'end')

        def open_cal(ifrm, ent):
            t = Toplevel(ifrm)
            cal = Calendar(t)
            cal.pack()

            Button(
                t,
                text="OK",
                command=lambda: (
                    ent.delete(0,'end'),
                    ent.insert(0, cal.get_date()),
                    t.destroy()
                )
            ).pack()

        def show_statement():
            f = from_entry.get()
            t = to_entry.get()
            con = sqlite3.connect("bank.sqlite")
            cur = con.cursor()
            query = """
            SELECT type, amount, date 
            FROM transactions
            WHERE acn=?
            ORDER BY tid DESC
            """
            cur.execute(query, (ucn,))
            rows = cur.fetchall()
            con.close()
            if not rows:
                messagebox.showinfo("Statement", "No transactions found")
                return
            text = ""
            for r in rows:
                text += f"{r[2]:<15} | {r[0]:<15} | ₹{r[1]}\n"
            result_lbl.config(text=text)

        # ---------- UI ----------
        ifrm=Frame(frm,background="white",bd=2,highlightbackground='black',highlightthickness=1)
        ifrm.place(relx=.25,rely=.1,relheight=.75,relwidth=.6)

        Label(ifrm, text="Mini Statement", font=("Arial",25), bg="white", fg="gray").pack(pady=5)

        Label(ifrm,text='From Date',font=("Arial",15,'bold'),bg='white').place(relx=.15,rely=.25)
        from_entry=Entry(ifrm)
        from_entry.place(relx=.15,rely=.34,relwidth=.25,height=25)

        Button(ifrm, text="📅", command=lambda:open_cal(ifrm,from_entry)).place(relx=.42,rely=.34,height=25)

        Label(ifrm,text='To Date',font=("Arial",15,'bold'),bg='white').place(relx=.48,rely=.25)
        to_entry=Entry(ifrm)
        to_entry.place(relx=.48,rely=.34,relwidth=.25,height=25)

        Button(ifrm, text="📅", command=lambda:open_cal(ifrm,to_entry)).place(relx=.76,rely=.34,height=25)

        open_btn=Button(ifrm,text='Show Statement',font=("Arial",15,'bold'),command=show_statement)
        open_btn.place(relx=.3,rely=.78,relwidth=.25)

        reset_btn=Button(ifrm,text='Reset',font=("Arial",15,'bold'),command=reset)
        reset_btn.place(relx=.6,rely=.78,relwidth=.2)

        result_lbl = Label(ifrm,text="",justify="left",bg="white",font=("Courier New",12))
        result_lbl.place(relx=.15,rely=.45)
    
    
    
    
    
    
    
    
    
              
    show_btn=Button(frm,text='show Details',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=show) 
    show_btn.place(relx=.01,rely=.1,relwidth=.18) 
    
    edit_btn=Button(frm,text='Edit details',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=Edit) 
    edit_btn.place(relx=.01,rely=.25,relwidth=.18) 
    
    dep_btn=Button(frm,text='Deposite',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=deposite) 
    dep_btn.place(relx=.01,rely=.4,relwidth=.18)
    
    witd_btn=Button(frm,text='withdraw',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=withdraw) 
    witd_btn.place(relx=.01,rely=.55,relwidth=.18) 
    
    trans_btn=Button(frm,text='Transfer',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=transfer) 
    trans_btn.place(relx=.01,rely=.7,relwidth=.18) 
    
    mini_statment_btn=Button(frm,text='Mini Statment',font=("Arial",15,'bold'),bd=2,bg="white",fg='blue',command=ministatment) 
    mini_statment_btn.place(relx=.01,rely=.85,relwidth=.18)

##############################################################################################################################################
main_screen()
update_time()     
root.mainloop()