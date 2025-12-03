from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)

# --- Conexão ---
def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Rota 1: Cadastro ---
@app.route('/', methods=['GET', 'POST'])
def pagina_inicial():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', 
                     (nome, email, senha))
        conn.commit()
        conn.close()
        return "<h1>Cadastrado!</h1> <a href='/login'>Fazer Login</a>"

    return render_template("Cadastro/cadastro.html")

# --- Rota 2: Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        usuario = conn.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        conn.close()

        if usuario:
            return redirect(url_for('dashboard'))
        else:
            return "<h1>Erro no login</h1> <a href='/login'>Tentar de novo</a>"

    return render_template("Login/login.html")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    sugestao_resposta = None # Começa vazio

    # Se o usuário clicou em "Enviar" (POST)
    if request.method == 'POST':
        gosto = request.form['gosto_usuario']
        
    cliente = genai.Client(api_key=chave_api)
    resposta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents= "Resuma mais esse texto (quando a linha estiver muito grande quebre ela, sem deixar linhas vazias): " + texto
    )
    return resposta.text

        sugestao_resposta = f"Como você gosta de '{gosto}', recomendo ouvir: Coldplay - Yellow"
    

    return render_template("Principal/principal.html", sugestao=sugestao_resposta)

if __name__ == '__main__':
    app.run(debug=True)