import smtplib

smtpUser = 'nbpshrestha4@gmail.com'
smtpPass = 'sexyboypabin'

toAdd = 'nbpshrestha4@gmail.com'
fromAdd = smtpUser

subject = 'Test email'
header = 'To:' + toAdd + '\n' + fromAdd + '\n' + 'Subject:' + subject
body = 'From Python Program sending EMAIL, ALert !!! Alert !!!'
print(header + '\n' +body)

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login(smtpUser,smtpPass)
print("login Successfull")
s.sendmail(fromAdd,toAdd,header + '\n\n' +body)

s.quit
