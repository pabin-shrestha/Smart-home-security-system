import smtplib

smtpUser = 'raspberrypitest2022@gmail.com'
smtpPass = 'raspberrypi2022'

toAdd = 'nbpshrestha4@gmail.com'
fromAdd = smtpUser

subject = 'Test email from raspberrypi'
header = 'To:' + toAdd + '\n' + 'From:' +fromAdd + '\n' + 'Subject:' + subject
body = 'From Python Program sending EMAIL, ALert !!! Alert !!!'
print(header + '\n' +body)

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login(smtpUser,smtpPass)
print("login Successfull")
s.sendmail(fromAdd,toAdd,header + '\n\n' +body)

s.quit()
