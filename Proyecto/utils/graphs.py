import pygal, pathlib, numpy
from pygal.style import Style
from apps.monitor.models import IfData, Interface

def get_packets_per_seconds(arr):
    differences = numpy.diff(arr)
    return numpy.insert(differences,0,0.0) #SE LE AGREGA UN 0.0 AL INICIO PARA QUE LA GRAFICA SE VEA COMO QUE CRECE

"""SNMP por defecto maneja los estados (1) up, (2) down. Necesitamos que en la grafica, down sea (0) y up (X).
Para eso se crea esta funcion"""
def translate_interface_status(arr):
    new_arr = []
    for item in arr:
        if item == '2':
            new_arr.append(0.0)
        else:
            new_arr.append(100.0)
    return new_arr

def create_graph_interface(data,interface):
    custom_style = Style(
        background='transparent',
        plot_background='transparent',
        foreground='#000000',
        foreground_strong='#000000',
        foreground_subtle='#000000',
        #Aqui es un color por cada linea que agregues a la grafica
        colors=('#00a140', '#a10000', '#021ed4', '#000000'))

    chart = pygal.Line(style = custom_style)
    chart.title = f"Paquetes entrantes a la interface {interface}"

    #Obtenemos la informacion que va a contener la grafica
    times = [item.time for item in data]
    chart.x_labels = times

    inpackets = list(map(float,[item.inpackets for item in data]))
    inerrors = list(map(float,[item.inerrors for item in data]))
    outpackets = list(map(float,[item.outpackets for item in data]))
    operstatus = translate_interface_status([item.ifstatus for item in data])
    
    chart.add('Entrantes', inpackets) #op1
    chart.add('Errores', inerrors) #op2
    chart.add('Salientes',outpackets)
    chart.add('Estado', operstatus) #OBLIGATORIA
    return chart

def generate_graphs_interfaces():
    """Obtenemos los datos para cada interface"""
    for item in Interface.get_interfaces():
        print("generate graph for ",item.interface)
        if_data = IfData.get_data(item.interface)
        if_chart = create_graph_interface(if_data,item.interface)    
        name = item.interface.replace("/","_")
        if_chart.render_to_png(filename=f'{pathlib.Path().resolve()}/static/files/{name}.png')
    return
