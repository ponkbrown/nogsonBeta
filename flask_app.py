from flask import Flask, render_template, request, redirect
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from lafila import laFila

app = Flask(__name__)

bootstrap = Bootstrap(app)
manager = Manager(app)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/fila')    
def fila():
    try:
        with open('info.txt', 'r') as inf:
            lafila = eval(inf.read()) 
            # la fecha es bien generica, hay que hacerla un poco mas especifica. nota que 
            # nomas usa la fecha de actualizacion de la linea vehicular deconcini.
            # ahorita esta bien pero en produccion hazlo mas especifico
            fecha = lafila['deconcini']['fecha'] + " " + " ".join(lafila['deconcini']['peat']['standard']['uptime'].split()[1:3])
            deconcini = { 'vehic': (lafila['deconcini']['vehic']['standard']['lineas'], lafila['deconcini']['vehic']['standard']['minutos'],
                                " ".join(lafila['deconcini']['vehic']['standard']['uptime'].split()[1:3])),
                          'peat': (lafila['deconcini']['peat']['standard']['lineas'], lafila['deconcini']['peat']['standard']['minutos'],
                                " ".join(lafila['deconcini']['peat']['standard']['uptime'].split()[1:3]))}

            mariposa = { 'vehic': (lafila['mariposa']['vehic']['standard']['lineas'], lafila['mariposa']['vehic']['standard']['minutos'],
                                " ".join(lafila['mariposa']['vehic']['standard']['uptime'].split()[1:3]))}

            morley = { 'peat': (lafila['deconcini']['peat']['standard']['lineas'], lafila['deconcini']['peat']['standard']['minutos'],
                                " ".join(lafila['deconcini']['peat']['standard']['uptime'].split()[1:3]))}

    except IOError:
        lineas, minutos, update = (0,0,0)
        pass
    client = request.headers.get('Usesr-Agent')
    return render_template('fila.html', fecha=fecha, deconcini=deconcini, mariposa=mariposa, morley=morley)

@app.route('/clima')
def clima():
    return render_template('clima.html')

@app.route('/google')
def google():
    return redirect('https://google.com/')

if __name__ == '__main__':
    manager.run()
