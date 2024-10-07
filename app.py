from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Mude para uma chave secreta real

# Configurações do MySQL
app.config['MYSQL_HOST'] = '181.41.200.56'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Depoistroco14@'
app.config['MYSQL_DB'] = 'filmoteca'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username = %s AND senha = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))  # Redireciona para a página de dashboard
        else:
            flash('Usuário ou senha inválidos!')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redireciona se não estiver logado
    return render_template('dashboard.html', username=session['username'])

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redireciona se não estiver logado

    if request.method == 'POST':
        if 'delete_account' in request.form:
            # Deletar a conta
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM usuarios WHERE username = %s", (session['username'],))
            mysql.connection.commit()
            cur.close()
            session.pop('username', None)  # Remove a sessão do usuário
            flash('Conta deletada com sucesso!')
            return redirect(url_for('home'))  # Redireciona para a página inicial

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Atualize as informações no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET nome = %s, email = %s, senha = %s WHERE username = %s",
                    (nome, email, senha, session['username']))
        mysql.connection.commit()
        cur.close()

        flash('Informações atualizadas com sucesso!')
        return redirect(url_for('dashboard'))

    return render_template('settings.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('As senhas não coincidem!')
            return redirect(url_for('register'))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nome, username, email, senha) VALUES (%s, %s, %s, %s)", (name, username, email, password))
        mysql.connection.commit()
        cur.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Lógica para enviar um e-mail de redefinição de senha
        flash('Instruções de redefinição de senha foram enviadas para o seu e-mail!')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
