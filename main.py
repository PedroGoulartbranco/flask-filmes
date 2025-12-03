from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
import google.generativeai as genai
import os 
from dotenv import load_dotenv

load_dotenv()

chave_api = os.getenv("API_KEY")


app = Flask(__name__)
app.secret_key = 'chave_super_secreta_do_mooflix'

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# ... (Rotas de Cadastro e Login continuam iguais) ...
@app.route('/', methods=['GET', 'POST'])
def pagina_inicial():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db_connection()
        conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
        conn.commit()
        conn.close()
        return "<h1>Cadastrado!</h1> <a href='/login'>Fazer Login</a>"
    return render_template("Cadastro/cadastro.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db_connection()
        usuario = conn.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        conn.close()
        if usuario:
            session['id_usuario'] = usuario['id']
            return redirect(url_for('dashboard'))
        else:
            return render_template("Login/login.html", erro_login=True)
    return render_template("Login/login.html")

# --- Rota Dashboard com Histórico ---
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    sugestao_resposta = None 
    id_logado = session['id_usuario']

    # Se for POST (Gerar nova sugestão)
    if request.method == 'POST':
        gosto = request.form['gosto_usuario']
        try:
            genai.configure(api_key=chave_api) 
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            
            prompt = f"Sugira 1 musica baseada neste gosto: {gosto}. Responda estritamente no formato: Nome da Música - Nome do Artista"
            resposta = model.generate_content(prompt)
            sugestao_resposta = resposta.text

            if ' - ' in sugestao_resposta:
                musica, artista = sugestao_resposta.split(' - ', 1)
            else:
                musica = sugestao_resposta
                artista = "IA Sugestão"

            conn = get_db_connection()
            conn.execute('INSERT INTO sugestoes (id_usuario, nome_musica, artista) VALUES (?, ?, ?)', 
                           (id_logado, musica, artista))
            conn.commit()
            conn.close()

        except Exception as e:
            sugestao_resposta = f"Erro: {e}"
    
    # --- PARTE NOVA: BUSCAR O HISTÓRICO ---
    conn = get_db_connection()
    # Pega as últimas 10 sugestões desse usuário (ORDER BY id DESC)
    historico_db = conn.execute('SELECT * FROM sugestoes WHERE id_usuario = ? ORDER BY id DESC LIMIT 10', (id_logado,)).fetchall()
    conn.close()

    # Passamos a lista 'historico' para o HTML
    return render_template("Principal/principal.html", sugestao=sugestao_resposta, historico=historico_db)

if __name__ == '__main__':
    app.run(debug=True)