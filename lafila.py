#_*_ coding: utf-8 _*_ 
import requests
import xml.etree.ElementTree as ET

def cbp(site='http://apps.cbp.gov/bwt/bwt.xml'):
    try:
        response = requests.get(site)
    except ConnectionError:
        return ("No se pudo conectar")

    if response.status_code == 200:
        xml = response.text
    else:
        print ("Hubo un error de conexión")
        return 0
    return xml

def laFila(xml):
    ''' Regresa un diccionario con la informacion de los tiempos de espera en las garitas de nogales'''
        
    root = ET.fromstring(xml)
    garitas = []

    for port in root.findall('port'):
        for data in port.getchildren():
            if data.text == 'Nogales':
                garitas.append(port)

    fecha = root.find('last_updated_date').text
    garita = {}
    for dato in garitas:
        #Creando el diccionario para las info de las garitas
       nombre = dato.find('crossing_name').text.lower().split()[0] 
       garita[nombre] = {}
        # Actualizando el estado de las garitas y la fecha
       if dato.find('port_status').text.lower() == 'open':
           garita[nombre]['status'] = 'Abierto'
       elif dato.find('port_status').text.lower() == 'closed':
           garita[nombre]['status'] = 'Cerrado'
       else:
           garita[nombre]['status'] = 'No disponible'

       garita[nombre]['fecha'] =  dato.find('date').text


       vehiculos = dato.find('passenger_vehicle_lanes')
       garita[nombre]['vehic'] = {}
       for linea in vehiculos[1:]:

           update = linea.find('update_time').text
           delay_minutes = linea.find('delay_minutes').text
           lines = linea.find('lanes_open').text
           garita[nombre]['vehic'][linea.tag.split('_')[0]] = {'minutos':delay_minutes, 'lineas':lines, 'uptime' : update}

        
       peatonal = dato.find('pedestrian_lanes')
       garita[nombre]['peat'] = {}
       for linea in peatonal[1:]:

           update = linea.find('update_time').text
           delay_minutes = linea.find('delay_minutes').text
           lines = linea.find('lanes_open').text
           garita[nombre]['peat'][linea.tag.split('_')[0]] = {'minutos':delay_minutes, 'lineas':lines, 'uptime' : update}   

    return garita

if __name__ == "__main__":
    xml = cbp()
    print (laFila(xml))
