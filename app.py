from flask import Flask, render_template, request, redirect, url_for, flash
import database as db
from models import Cliente, Pedido, Peca

app = Flask(__name__)
app.secret_key = "ifpi_aps_key"

db.init_db()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('usuario')
    senha = request.form.get('senha')
    
    conn = db.get_db()
    user = conn.execute("SELECT * FROM usuarios WHERE username = ? AND senha = ?", (username, senha)).fetchone()
    conn.close()
    
    if user:
        return redirect(url_for('index_registro'))
    
    flash("Usuário ou senha incorretos!", "danger")
    return redirect(url_for('login_page'))

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    username = request.form.get('usuario')
    senha = request.form.get('senha')
    
    conn = db.get_db()
    try:
        conn.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, senha))
        conn.commit()
        flash("Conta criada com sucesso! Faça login.", "success")
    except:
        flash("Erro: Este usuário já existe.", "warning")
    finally:
        conn.close()
        
    return redirect(url_for('login_page'))

@app.route('/registro')
def index_registro():
    return render_template('index.html')

@app.route('/registrar_pedido_multiplo', methods=['POST'])
def registrar_pedido_multiplo():
    dados = request.get_json()
    nome = dados.get('cliente')
    tel = dados.get('telefone')
    itens = dados.get('itens', [])

    if not itens:
        return "Nenhum item adicionado", 400

    conn = db.get_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO clientes (nome, cpf, telefone, endereco) VALUES (?, ?, ?, ?)", 
                  (nome, tel, tel, "Teresina-PI"))
    cliente = cursor.execute("SELECT id FROM clientes WHERE telefone = ?", (tel,)).fetchone()
    cliente_id = cliente['id']

    cliente_obj = Cliente(cliente_id, nome, tel, "")
    pedido_obj = Pedido(0, cliente_obj)
    
    for item in itens:
        peca_info = Peca(item['tipo'], item['cor'], "Recebido", item['servico'])
        for _ in range(int(item['qtd'])):
            pedido_obj.adicionar_peca(peca_info)
    
    cursor.execute("""INSERT INTO pedidos (cliente_id, valor_bruto, desconto, valor_liquido, status, status_pagamento) 
                      VALUES (?, ?, ?, ?, ?, ?)""", 
                   (cliente_id, pedido_obj.valor_bruto, pedido_obj.desconto, pedido_obj.valor_liquido, "Recebido", "Aberto"))
    
    conn.commit()
    conn.close()
    return {"status": "sucesso"}, 200

@app.route('/gestao')
def gestao():
    conn = db.get_db()
    pedidos = conn.execute("SELECT p.*, c.nome as cliente_nome FROM pedidos p JOIN clientes c ON p.cliente_id = c.id ORDER BY p.id DESC").fetchall()
    conn.close()
    return render_template('gestao.html', pedidos=pedidos)

@app.route('/atualizar/<int:id>')
def atualizar_status(id):
    conn = db.get_db()
    p = conn.execute("SELECT status FROM pedidos WHERE id = ?", (id,)).fetchone()
    if p:
        fluxo = ["Recebido", "Lavagem", "Secagem", "Pronto para Retirada"]
        if p['status'] in fluxo:
            idx = fluxo.index(p['status'])
            if idx < len(fluxo) - 1:
                conn.execute("UPDATE pedidos SET status = ? WHERE id = ?", (fluxo[idx+1], id))
                conn.commit()
    conn.close()
    return redirect(url_for('gestao'))

@app.route('/entregar/<int:id>')
def entregar_pedido(id):
    conn = db.get_db()
    conn.execute("UPDATE pedidos SET status = 'Entregue', status_pagamento = 'Pago' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('gestao'))

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    pedido = None
    progresso = 0
    if request.method == 'POST':
        id_b = request.form.get('id_pedido')
        conn = db.get_db()
        pedido = conn.execute("SELECT p.*, c.nome as cliente_nome FROM pedidos p JOIN clientes c ON p.cliente_id = c.id WHERE p.id = ?", (id_b,)).fetchone()
        if pedido:
            mapa = {'Recebido': 25, 'Lavagem': 50, 'Secagem': 75, 'Pronto para Retirada': 100, 'Entregue': 100}
            progresso = mapa.get(pedido['status'], 10)
        conn.close()
    return render_template('consulta.html', pedido=pedido, progresso=progresso)

if __name__ == '__main__':
    app.run(debug=True)