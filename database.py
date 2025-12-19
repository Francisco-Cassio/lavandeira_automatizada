import sqlite3

DB_NAME = "lavanderia.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    
    conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL
        )
    ''')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            valor_bruto REAL NOT NULL,
            desconto REAL NOT NULL,
            valor_liquido REAL NOT NULL,
            status TEXT NOT NULL,
            status_pagamento TEXT NOT NULL,
            forma_pagamento TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            tipo TEXT,
            material TEXT,
            cor TEXT,
            estado TEXT,
            servico TEXT,
            valor REAL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        )
    """)

    conn.commit()
    conn.close()
