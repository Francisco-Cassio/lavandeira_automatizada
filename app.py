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
    if username == "admin" and senha == "123":
        return redirect(url_for('index_registro'))
    flash("Usuário ou senha inválidos")
    return redirect(url_for('login_page'))

@app.route('/registro')
def index_registro():
    return render_template('index.html')

@app.route('/registrar_pedido', methods=['POST'])
def registrar_pedido():
    nome = request.form.get('cliente')
    tel = request.form.get('telefone')
    
    # Captura os dados da peça e a quantidade
    tipo = request.form.get('tipo')
    material = request.form.get('material')
    cor = request.form.get('cor')
    estado = request.form.get('estado')
    servico = request.form.get('servico')
    quantidade = int(request.form.get('quantidade', 1))
    
    conn = db.get_db()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO clientes (nome, cpf, telefone) VALUES (?, ?, ?)", (nome, tel, tel))
    cliente_id = cursor.execute("SELECT id FROM clientes WHERE telefone = ?", (tel,)).fetchone()['id']
    
    peca_obj = Peca(tipo, material, cor, estado, servico)
    pedido_obj = Pedido(0, Cliente(cliente_id, nome, tel, ""))
    
    for _ in range(quantidade):
        pedido_obj.adicionar_peca(peca_obj)
    cursor.execute("""
        INSERT INTO pedidos (cliente_id, valor_bruto, desconto, valor_liquido, status, status_pagamento) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente_id, pedido_obj.valor_bruto, pedido_obj.desconto, pedido_obj.valor_liquido, "Recebido", "Aberto"))
    
    conn.commit()
    conn.close()
    return redirect(url_for('gestao'))

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