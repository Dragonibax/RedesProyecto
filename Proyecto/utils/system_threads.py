import sys
import threading as th
from tracemalloc import start
from utils.topology import detect
from apps.monitor.snmpget import get_interfaces_data
from apps.monitor.snmptraps import start_listen, stop_listen
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(job_defaults={'max-instances':3})
sched.start()

def init_threads():
    global sched
    sched = BackgroundScheduler(job_defaults={'max-instances':3})
    sched.start()


def start_thread(name,interval = None):
    global sched
    try:
        if name == "traps":
            sched.add_job(start_listen,'interval',minutes=1,id='traps')
        elif name == "topology":
            print(f"Iniciando el hilo de deteccion de la topologia cada {interval} segundos")
            print(sched)
            sched.add_job(detect,'interval',seconds=interval,id='topology')
        else:
            #Nada mas queda el de las interfaces
            print(f"Iniciando el hilo de snmp query cada {interval} segundos")
            sched.add_job(get_interfaces_data,'interval',seconds=interval,id='interfaces')
        return
    except RuntimeError:
        sched = BackgroundScheduler(job_defaults={'max-instances':3})
        sched.start()
        start_thread(name,interval)

def stop_thread(name):
    global sched, traps_thread
    print(f"Deteniendo el hilo {name}...",end='')
    sched.remove_job(name)
    print("[OK]")

def change_interval(name,interval):
    stop_thread(name)
    start_thread(name,interval)
        
def stop_scheduler():
    global sched
    sched.shutdown()

def start_scheduler():
    global sched
    if not sched.running:
        sched.start()