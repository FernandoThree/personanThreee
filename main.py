import json
import sys
from flask import Flask, render_template, jsonify, make_response, request, abort
from Autoregulacion.AutoRegul import AutoRegulacion
#from Autoregulacion import autoRegul

# Inicializamos el flask
app = Flask(__name__)
#puntualidad = autoRegula()

#@app.route('/')
#def index():
#    return render_template('index.html')

@app.route('/API/v1.0/AutoReg/Get', methods=['GET'])
# @auth.login_required
def api_v1_0_test_hi():
    #loglocalizacion.getDiccionario(1)
    return jsonify(puntualidad.CargaCRD())
    #return jsonify({'error': '0'})
# En caso de no encontrar la aplicación.

@app.route('/API/v1.0/AutoReg/Send', methods=['GET'])
def api_v1_AutoReg_send():
    mns_Txt = AutoRegulacion()
    return mns_Txt.getRegulaP(1, "Table_Position")

@app.errorhandler(404)
def page_not_foud(error):
    return "I'm afraid, the page doesn't exists!", 404

@app.errorhandler(405)
def page_405(error):
    return "Stop, it's forbidden!", 405

@app.errorhandler(500)
def page_500(error):
    return  make_response(jsonify({'error': 'Oops 500!'}), 500)
    #return 'Oops!, 500!'

@app.errorhandler(502)
def page_502(error):
    return  make_response(jsonify({'error': 'Oops 502!'}), 502)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """

    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"

    # r.headers['Cache-Control'] = 'public, max-age=60, s-maxage=60, must-revalidate'
    r.headers['X-Robots-Tag'] = 'none'
    return r


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run('0.0.0.0',port=7070,debug=False)


