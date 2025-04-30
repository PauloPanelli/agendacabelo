from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Agenda com horários ocupados
agendamentos = {}

# Gera os horários disponíveis de segunda a sábado, das 09h às 18h (a cada 1 hora)
def gerar_horarios():
    dias = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado']
    horarios = {}
    for dia in dias:
        horarios[dia] = []
        for hora in range(9, 18):  # 09h às 18h
            horarios[dia].append(f"{hora:02d}:00")
    return horarios

@app.route('/')
def index():
    horarios = gerar_horarios()
    return render_template('index.html', horarios=horarios, agendamentos=agendamentos)

@app.route('/agendar', methods=['POST'])
def agendar():
    dia = request.form['dia']
    hora = request.form['hora']
    cliente = request.form['cliente']
    celular = request.form['celular']
    tipo_corte = request.form['tipo_corte']

    if dia not in agendamentos:
        agendamentos[dia] = {}

    if hora in agendamentos[dia]:
        return "Horário já agendado!", 400

    agendamentos[dia][hora] = {
        'cliente': cliente,
        'celular': celular,
        'tipo_corte': tipo_corte
    }
    return redirect(url_for('index'))

@app.route('/cancelar', methods=['POST'])
def cancelar():
    dia = request.form['dia']
    hora = request.form['hora']

    if dia in agendamentos and hora in agendamentos[dia]:
        del agendamentos[dia][hora]
        return redirect(url_for('index'))
    return "Agendamento não encontrado!", 400

if __name__ == '__main__':
    app.run(debug=True)
