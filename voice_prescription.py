#1] TAKING VOICE INPUT
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say patient name!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
name=r.recognize_google(audio)

with sr.Microphone() as source:
    print("Symptoms")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
sympt=r.recognize_google(audio)
    
with sr.Microphone() as source:
    print("Prescription")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
diag=r.recognize_google(audio)

with sr.Microphone() as source:
    print("Advice")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
advice=r.recognize_google(audio)    




# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    #print("Name-",name)
    #print("Symptoms-",sympt)
    #print("Prescription-",diag)
    #print("Advice-",advice)
    pass
    
    
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    
    
    
#2] CREATING TEXT FILE    
# Python code to create a file 
file = open('pres.txt','w') 
file.write(name+"\n") 
file.write(sympt+"\n")
file.write(diag+"\n")
file.write(advice+"\n")
file.close()
import os
file = "notepad.exe pres.txt"
os.system(file)



#3]CREATING DIGITAL PRESCRIPTION
l=[['Name','Symptoms','Prescription','Advice']]
li=[]
 
with open("pres.txt") as file:   
    dataa = file.read()
    li.append(dataa.split("\n"))
[li]=li
li.pop()
l.append(li)
data=l
fileName = 'pres.pdf'

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

pdf = SimpleDocTemplate(
    fileName,
    pagesize=letter
)

from reportlab.platypus import Table
table = Table(data)

# add style
from reportlab.platypus import TableStyle
from reportlab.lib import colors

style = TableStyle([
    ('BACKGROUND', (0,0), (3,0), colors.green),
    ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

    ('ALIGN',(0,0),(-1,-1),'CENTER'),

    ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),

    ('BOTTOMPADDING', (0,0), (-1,0), 12),

    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
])
table.setStyle(style)

#  Alternate backgroud color
rowNumb = len(data)
for i in range(1, rowNumb):
    if i % 2 == 0:
        bc = colors.burlywood
    else:
        bc = colors.beige
    
    ts = TableStyle(
        [('BACKGROUND', (0,i),(-1,i), bc)]
    )
    table.setStyle(ts)

#  Add borders
ts = TableStyle(
    [
    ('BOX',(0,0),(-1,-1),2,colors.black),

    ('LINEBEFORE',(2,1),(2,-1),2,colors.white),
    ('LINEABOVE',(0,2),(-1,2),2,colors.white),

    ('GRID',(0,1),(-1,-1),2,colors.black),
    ]
)
table.setStyle(ts)

elems = []
elems.append(table)

pdf.build(elems)



#4] SENDING EMAIL TO PATIENT
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = ''
email_password =''
email_send = input()

subject = ''

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = ''
msg.attach(MIMEText(body,'plain'))

filename='pres.pdf'
attachment  =open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()