import gmail

email="" #write your email
pwd="" #write your App password

def openanc_mail(to,text):
    con=gmail.GMail(email,pwd)
    mg=gmail.Message(to=to, subject="Account oppend in pnb bank",text=text)
    con.send(mg)
    
    

def close_otp_mail(to,text):
    con=gmail.GMail(email,pwd)
    mg=gmail.Message(to=to, subject="Otp for close account",text=text)
    con.send(mg)
    
def frogot_otp_mail(to,text):
    con=gmail.GMail(email,pwd)
    mg=gmail.Message(to=to, subject="Otp for forgot pass",text=text)
    con.send(mg)
