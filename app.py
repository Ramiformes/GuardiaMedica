import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime, time, timedelta


# Configure application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<template_name>.html')
def render_page(template_name):
    if os.path.exists(f'templates/{template_name}.html'):
        return render_template(f'{template_name}.html')
    else:
        return "Página no encontrada", 404


#Calculadora para dividir la guardia
@app.route('/division_guardia', methods=['POST'])
def division_guardia():

    # Obtener los datos del formulario
    num_personas = int(request.form['number'])
    hora_inicio = datetime.strptime(request.form['time1'], '%H:%M').time()
    hora_fin = datetime.strptime(request.form['time2'], '%H:%M').time()

    # Calcular la diferencia total en minutos
    diferencia = ((hora_fin.hour * 60 + hora_fin.minute) - (hora_inicio.hour * 60 + hora_inicio.minute)) % 1440

    # Calcular el tiempo por persona
    minutos_por_persona = diferencia // num_personas
    tiempo_extra = diferencia % num_personas

    # Crear una lista para almacenar los turnos de cada persona
    turnos = []

    # Asignar los turnos
    for i in range(num_personas):
        minutos_asignados = minutos_por_persona
        if tiempo_extra > 0:
            minutos_asignados += 1
            tiempo_extra -= 1

        fin_turno = (hora_inicio.hour * 60 + hora_inicio.minute + minutos_asignados) % 1440
        turnos.append((hora_inicio, time(fin_turno // 60, fin_turno % 60)))

        hora_inicio = time(fin_turno // 60, fin_turno % 60)

 # Devuelve los turnos como una respuesta JSON
    turnos_str = [(t[0].strftime('%H:%M'), t[1].strftime('%H:%M')) for t in turnos]
    return jsonify(turnos=turnos_str)

#calculadora Cockroft Gault y CKDEPI
@app.route('/calcular_tfg', methods=['POST'])
def calcular_tfg():
    edad = int(request.form.get('edad'))
    creatinina = float(request.form.get('creatinina'))
    sexo = request.form.get('sexo')
    raza = request.form.get('raza')  # Asumiendo que tienes un campo 'raza' en tu formulario
    peso = float(request.form.get('peso'))  # Asumiendo que tienes un campo 'peso' en tu formulario
    formula = request.form.get('formula')

    if formula == "cockroft_gault":
        if sexo == "masculino":
            tfg = ((140 - edad) * peso) / (72 * creatinina)
        else:  # femenino
            tfg = (((140 - edad) * peso) / (72 * creatinina)) * 0.85
    elif formula == "ckdepi":
        if sexo == "femenino":
            if creatinina <= 0.7:
                tfg = 144 * (creatinina / 0.7)**-0.329 * 0.993**edad
            else:
                tfg = 144 * (creatinina / 0.7)**-1.209 * 0.993**edad
        else:  # masculino
            if creatinina <= 0.9:
                tfg = 141 * (creatinina / 0.9)**-0.411 * 0.993**edad
            else:
                tfg = 141 * (creatinina / 0.9)**-1.209 * 0.993**edad

        if raza == "negra":  # Asumiendo que el valor para raza negra en tu formulario es 'negra'
            tfg *= 1.159



    return jsonify({"tfg": tfg})



#Calculadora de semanas de gestación
# Función para cambiar el formato de la fecha
def format_date_to_ddmmyyyy(input_date):
    return input_date.strftime('%d/%m/%Y')

@app.route('/calcular_gestacion', methods=['POST'])

def calcular_gestacion():
    fum = request.form.get('fum')
    ultrasound_date = request.form.get('ultrasoundDate')
    ultrasound_weeks = int(request.form.get('ultrasoundWeeks')) if request.form.get('ultrasoundWeeks') else None

    # Calcular las semanas de gestación basadas en la FUM
    if fum:
        fum_date = datetime.strptime(fum, '%Y-%m-%d').date()
        today = datetime.today().date()
        difference_fum = (today - fum_date).days
        weeks_fum = difference_fum // 7
        days_fum = difference_fum % 7
        fpp_fum = fum_date + timedelta(days=280)  # 40 semanas desde la FUM
    else:
        weeks_fum, days_fum, fpp_fum = None, None, None

    # Calcular las semanas de gestación basadas en el ultrasonido
    if ultrasound_date and ultrasound_weeks is not None:
        ultrasound_date_obj = datetime.strptime(ultrasound_date, '%Y-%m-%d').date()
        difference_ultrasound = (today - ultrasound_date_obj).days
        total_days_ultrasound = difference_ultrasound + (ultrasound_weeks * 7)
        weeks_ultrasound = total_days_ultrasound // 7
        days_ultrasound = total_days_ultrasound % 7
        fpp_ultrasound = ultrasound_date_obj + timedelta(days=(280 - (ultrasound_weeks * 7)))
    else:
        weeks_ultrasound, days_ultrasound, fpp_ultrasound = None, None, None

    return jsonify({
    'weeks_fum': f"{weeks_fum}.{days_fum}" if weeks_fum is not None else None,
    'weeks_ultrasound': f"{weeks_ultrasound}.{days_ultrasound}" if weeks_ultrasound is not None else None,
    'fpp_fum': format_date_to_ddmmyyyy(fpp_fum) if fpp_fum else None,
    'fpp_ultrasound': format_date_to_ddmmyyyy(fpp_ultrasound) if fpp_ultrasound else None
})



#Calculadora CURB65
@app.route('/calcular_curb65', methods=['POST'])
def calcular_curb65():
    confusión = request.form.get('confusion') == 'si'
    urea = float(request.form.get('urea'))
    frecuencia_respiratoria = int(request.form.get('frecuencia_respiratoria'))
    presion_sistolica = int(request.form.get('presion_sistolica'))
    presion_diastolica = int(request.form.get('presion_diastolica'))
    edad = int(request.form.get('edad'))

    score = 0
    if confusión:
        score += 1
    if urea > 7:
        score += 1
    if frecuencia_respiratoria >= 30:
        score += 1
    if presion_sistolica < 90 or presion_diastolica <= 60:
        score += 1
    if edad >= 65:
        score += 1

    return jsonify({"score": score})

#Child Pugh
@app.route('/calcular_childpugh', methods=['POST'])
def calcular_childpugh():
    bilirrubina = float(request.form.get('bilirrubina'))
    albumina = float(request.form.get('albumina'))
    tiempo_protrombina = float(request.form.get('tiempo_protrombina'))
    ascitis = request.form.get('ascitis')  # asumimos que puede ser 'ausente', 'leve' o 'moderada'
    encefalopatia = request.form.get('encefalopatia')  # asumimos que puede ser 'ausente', 'grado I-II' o 'grado III-IV'

    score = 0

    # Bilirrubina total
    if bilirrubina <= 2:
        score += 1
    elif 2 < bilirrubina <= 3:
        score += 2
    else:
        score += 3

    # Albúmina sérica
    if albumina >= 3.5:
        score += 1
    elif 2.8 <= albumina < 3.5:
        score += 2
    else:
        score += 3

    # Tiempo de protrombina
    if tiempo_protrombina <= 4:
        score += 1
    elif 4 < tiempo_protrombina <= 6:
        score += 2
    else:
        score += 3

    # Ascitis
    if ascitis == 'ausente':
        score += 1
    elif ascitis == 'leve':
        score += 2
    else:
        score += 3

    # Encefalopatía hepática
    if encefalopatia == 'ausente':
        score += 1
    elif encefalopatia == 'grado I-II':
        score += 2
    else:
        score += 3

    return jsonify({"score": score})

#conteo absoluto de eosinófilos
@app.route('/calcular_eosinofilos', methods=['POST'])
def calcular_eosinofilos():
    # Obtener los datos del formulario
    wbc = float(request.form.get('wbc'))
    eosinofilos = float(request.form.get('eosinofilos'))

    # Calcular el conteo absoluto de eosinófilos
    conteo_absoluto = wbc * eosinofilos / 100

    return jsonify({"conteo_absoluto": conteo_absoluto})



#calcuadora de IMC

@app.route('/calcular_imc', methods=['POST'])
def calcular_imc():
    try:
        # obtener altura y peso
        altura = float(request.form.get('altura'))
        peso = float(request.form.get('peso'))

        # Validar que los valores sean positivos
        if altura <= 0 or peso <= 0:
            return jsonify({"error": "Altura y peso deben ser valores positivos"}), 400

        # calcular IMC
        imc = peso / altura**2

        return jsonify({"imc": imc})

    except ValueError:
        return jsonify({"error": "Por favor, ingrese valores numéricos válidos para altura y peso"}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error al calcular el IMC: " + str(e)}), 500

#Escala peso predicho ARDS

@app.route('/calcular_peso_predicho', methods=['POST'])
def calcular_peso_predicho():
    try:
        # obtener género y altura
        genero = request.form.get('genero')
        altura = float(request.form.get('altura'))

        # Validar que los valores sean correctos
        if altura <= 0:
            return jsonify({"error": "La altura debe ser un valor positivo"}), 400
        if genero not in ['hombre', 'mujer']:
            return jsonify({"error": "Género no válido"}), 400

        # calcular peso predicho
        if genero == 'hombre':
            peso_predicho = 50 + 0.91 * (altura - 152.4)
        else:  # mujer
            peso_predicho = 45.5 + 0.91 * (altura - 152.4)

        return jsonify({"peso_predicho": peso_predicho})

    except ValueError:
        return jsonify({"error": "Por favor, ingrese un valor numérico válido para la altura"}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error al calcular el peso predicho: " + str(e)}), 500

if __name__ == '__main__':
    app.run()

#Calculadora de sodio corregido por glucosa


@app.route('/correccion_sodio', methods=['GET', 'POST'])
def correccion_sodio():
    if request.method == 'POST':
        # Obtener los valores del formulario
        measured_sodium = float(request.form['measuredSodium'])
        serum_glucose = float(request.form['serumGlucose'])
        correction_factor = float(request.form['correctionFactor'])

        # Realizar el cálculo de corrección de sodio
        corrected_sodium = measured_sodium + ((serum_glucose - 100) / 100) * correction_factor

        # Enviar el resultado en formato JSON
        return jsonify({"corrected_sodium": corrected_sodium})

    return render_template('correccion_sodio.html')

#Calculadora de superficie corporal
@app.route('/bsa_calculator', methods=['GET', 'POST'])
def bsa_calculator():
    if request.method == 'POST':
        # Obtener los valores del formulario
        formula = request.form['formula']
        weight = float(request.form['weight'])

        # Realizar el cálculo de BSA
        if formula == 'dubois':
            bsa = 0.007184 * (height ** 0.725) * (weight ** 0.425)
        elif formula == 'costeff':
            if weight <= 10:
                bsa = ((weight * 4) + 9) / 100
            else:
                bsa = ((weight * 4) + 7) / (weight + 90)
        else:
            bsa = None

        # Enviar el resultado en formato JSON
        return jsonify({"bsa_result": bsa})

    return render_template('superficiecorporal.html')



#Escala SLEDAI
@app.route('/sledai', methods=['GET', 'POST'])
def sledai():
    score = None
    if request.method == 'POST':
        # Obtener los valores de cada ítem del formulario
        items = [
            'recentSeizure', 'psychosis', 'organicBrainSyndrome', 'visualDisturbance',
            'neuropathy', 'lupusHeadache', 'newStroke', 'vasculitis', 'arthritis',
            'myositis', 'hematuria', 'proteinuria', 'pyuria', 'inflammatoryRash',
            'alopecia', 'oralNasalUlcers', 'pleuriticPain', 'pericarditis',
            'lowComplement', 'highDnaBinding', 'temperature', 'lowPlatelets', 'lowWbc'
        ]

        # Calcular la puntuación total
        score = sum([int(request.form.get(item, 0)) for item in items])

        # Si la solicitud es AJAX, devolvemos la puntuación en formato JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print("Solicitud AJAX a /sledai")  # Añade esta línea para depuración
            return jsonify({ "score": score })

    return render_template('sledai.html', score=score)  # Asume que tu archivo HTML se llama 'sledai.html'

