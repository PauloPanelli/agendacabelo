from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'chave-secreta'  # Necessário para usar sessões

# Agenda com horários ocupados
agendamentos = {}

# Usuários (simulação de banco de dados)
usuarios = {
    'admin': {'senha': 'admin123'}  # Administrador
}

# Gera os horários disponíveis de segunda a sábado, das 09h às 18h (a cada 1 hora)
def gerar_horarios():
    dias = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado']
    hoje = datetime.now()
    horarios = {}
    for i, dia in enumerate(dias):
        data = (hoje + timedelta(days=i - hoje.weekday())).strftime('%d/%m')  # Calcula a data do dia
        dia_com_data = f"{dia.capitalize()} ({data})"  # Adiciona a data ao lado do dia
        horarios[dia_com_data] = []
        hora_atual = 9 * 60  # Início do horário: 09:00 em minutos
        fim_horario = 18 * 60  # Fim do horário: 18:00 em minutos
        while hora_atual < fim_horario:
            horas = hora_atual // 60
            minutos = hora_atual % 60
            horarios[dia_com_data].append(f"{horas:02d}:{minutos:02d}")
            hora_atual += 40  # Incrementa 40 minutos
    return horarios

@app.route('/')
def index():
    if 'usuario' in session and session['usuario'] == 'admin':
        return render_template('admin.html', agendamentos=agendamentos)
    horarios = gerar_horarios()
    return render_template('cliente.html', horarios=horarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form.get('senha')

        # Login do administrador
        if usuario == 'admin' and senha == usuarios['admin']['senha']:
            session['usuario'] = 'admin'
            return redirect(url_for('index'))

        return "Credenciais inválidas!", 400
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    dia = request.form['dia']
    hora = request.form['hora']
    nome = request.form['nome']
    telefone = request.form['telefone']
    tipo_corte = request.form['tipo_corte']

    # Remove espaços do telefone
    telefone = telefone.replace(" ", "")

    # Define os valores dos cortes
    valores_cortes = {
        "Corte Simples": 35.00,
        "Barba": 15.00,
        "Cabelo + Barba": 45.00
    }

    if dia not in agendamentos:
        agendamentos[dia] = {}

    if hora in agendamentos[dia]:
        flash("Horário já agendado! Por favor, escolha outro horário.")
        return redirect(url_for('index'))

    agendamentos[dia][hora] = {
        'cliente': nome,
        'telefone': telefone,
        'tipo_corte': tipo_corte,
        'valor': valores_cortes[tipo_corte]  # Adiciona o valor do corte
    }

    # Redireciona para a página de sucesso
    return redirect(url_for('sucesso'))

@app.route('/cancelar', methods=['POST'])
def cancelar():
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect(url_for('login'))

    dia = request.form['dia']
    hora = request.form['hora']

    if dia in agendamentos and hora in agendamentos[dia]:
        del agendamentos[dia][hora]
        return redirect(url_for('index'))
    return "Agendamento não encontrado!", 400

if __name__ == '__main__':
    app.run(debug=True)
