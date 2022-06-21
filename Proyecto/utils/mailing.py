from glob import glob

import yagmail

yag = None

def init_app():
    global yag
    yag = yagmail.SMTP('ardapendragon@gmail.com',oauth2_file='/home/sabino/Escritorio/secretredesSAB.json')
    return

def send_email(message,subject,to="sabino.snm@gmail.com"):
    global yag
    print(f"Enviando correo a {to}")
    yag.send(to=to,subject=subject,contents=message)
    return
