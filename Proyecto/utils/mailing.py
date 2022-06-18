from glob import glob

import yagmail

yag = None

def init_app():
    global yag
    yag = yagmail.SMTP('saturn.sofiax13@gmail.com',oauth2_file='/home/sofia/Escritorio/sofiaoauth.json')
    return

def send_email(message,subject,to="aarongamasc@gmail.com"):
    global yag
    print(f"Enviando correo a {to}")
    yag.send(to=to,subject=subject,contents=message)
    return
