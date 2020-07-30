import Math_geo.Math as smate
from Math_geo.Point import Point as spoint
#from vertices import Trayecto
from Parada_Colision.Parada_Colision import Trayecto
from flask import Flask, jsonify, make_response, render_template

app = Flask(__name__)
Trayecto()

 #<editor-fold desc="Paginas webs">

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/API/V1.0/Test/Geo', methods=['GET'])
def api_v1_0_test_stPoligono():
    return ('¡¡Prueba de Paradas Poligono...!!')

@app.route('/API/v1.0/Test/Poly', methods=['GET'])
#@auth.login_required
def api_v1_0_test_Geo():
    punto1 = spoint(20.2914, 89.0049)
    punto2 = spoint(19.4198007189416, -99.0966198964256)
    myvar = smate.get_distance(punto1, punto2)
    return jsonify(myvar)

@app.route('/Test/getPoligonos', methods = ['GET'])   # POST
def getPoligonos():
    return jsonify('Salio bien')
    #args = request.get_json()


# En caso de no encontrar la aplicación.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#Ejecución principal
def main():
    app.run(host='0.0.0.0', port=8080, debug=True)

#Preguntamos si es ejecución principal
if __name__ == '__main__':
   main()