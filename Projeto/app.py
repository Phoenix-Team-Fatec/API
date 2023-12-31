from flask import Flask, render_template, request, redirect, render_template_string
from flask_mail import Mail
from flask_mail import Message


# CLASSE PARA SALVAR AS AVALIAÇÕES
class avaliacao:
    def __init__(self, papel, proatividade, autonomia, colaboracao, entrega):
        self.papel = papel
        self.proatividade = proatividade
        self.autonomia = autonomia
        self.colaboracao = colaboracao
        self.entrega = entrega

notas = []
limite = []

app = Flask("__name__")

# CONFIGURAÇÕES PARA O EMAIL 

app.secret_key = 'phoenix'
app.config['SECRET_KEY'] = "tsfyguaistyatuis589566875623568956"
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "phoenix.team.sjc@gmail.com"
app.config['MAIL_PASSWORD'] = "tera dxis ktfz sria"

mail = Mail(app)


# ROTAS DA WEB

@app.route('/')
def boas():
    return render_template('boas-vindas.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/Eventos')
def Eventos():
    return render_template('eventos.html')

@app.route('/CriarEquipe')
def teste():
    return render_template('teste.html')

@app.route('/limitante', methods=['POST',])
def limitante():
    notas.clear()
    limite.clear()
    limite.append(int(request.form['quantidade_de_dev_teams']))
    return redirect('/Pacer')


@app.route('/Pacer')
def pacer():
    if len(notas) > 2 + limite[0]:
        notas.clear()
        return render_template('pacer.html', listas = notas, lim = limite[0])
    return render_template('pacer.html', listas = notas, lim = limite[0])

@app.route('/Criar', methods=['POST',])
def criar():
    notas.clear()

    # RECEBENDO DADOS DO FORMULÁRIO
    papel = ['P.O', 'S.M']
    proatividade = [request.form['proat_po'],request.form['proat_sm']]
    autonomia = [request.form['aut_po'],request.form['aut_sm']]
    colaboracao = [request.form['colab_po'],request.form['colab_sm']]
    entrega = [request.form['entrega_po'],request.form['entrega_sm']]

    for i in range(limite[0]):
        i = str(i)
        papel.append("D.T"+i)
        proatividade.append(request.form['proat_dt'+i])
        autonomia.append(request.form['aut_dt'+i])
        colaboracao.append(request.form['colab_dt'+i])
        entrega.append(request.form['entrega_dt'+i])

    email_destinatario = request.form['email_destinatario']

    # ENVIANDO DADOS PARA UM OBJETO E GUARDANDO NUM VETOR
    for i in range(len(papel)):
        avaliado = avaliacao(papel[i], proatividade[i], autonomia[i], colaboracao[i], entrega[i])
        notas.append(avaliado)
        

    # ENVIANDO DADOS PARA UM EMAIL
    msg = Message("Avaliação", sender="noreply@app.com", recipients=[email_destinatario])
        
        # CRIANDO UM EMAIL
    html_content = """
     <table style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">papel</th>
                <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">proatividade</th>
                <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">autonomia</th>
                <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">colaboracao</th>
                <th style="border: 1px solid black; padding: 8px; text-align: center; background-color: #f2f2f2;">entrega</th>
            </tr>
        </thead>
        <tbody>
            {% for item in listas %}
            <tr>
                <td style="border: 1px solid black; padding: 8px; text-align: center;">{{ item.papel }}</td>
                <td style="border: 1px solid black; padding: 8px; text-align: center;">{{ item.proatividade }}</td>
                <td style="border: 1px solid black; padding: 8px; text-align: center;">{{ item.autonomia }}</td>
                <td style="border: 1px solid black; padding: 8px; text-align: center;">{{ item.colaboracao }}</td>
                <td style="border: 1px solid black; padding: 8px; text-align: center;">{{ item.entrega }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    """

    # Renderize o conteúdo HTML usando render_template_string
    rendered_html = render_template_string(html_content, listas=notas)

    msg.html = rendered_html

    mail.send(msg)    
    return redirect('/Pacer')


@app.route('/artefatos')
def artefatos():
    return render_template('artefatos.html')

@app.route('/Papéis')
def papeis():
    return render_template('papeis.html')

@app.route('/Apendice')
def apendice():
    return render_template('apendice.html')

@app.route('/Bibliografia')
def bibliografia():
    return render_template('bibliografia.html')

app.run(debug=True)