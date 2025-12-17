import datetime

class Cliente:
    def __init__(self, id, nome, cpf_telefone, endereco):
        self.id = id
        self.nome = nome
        self.cpf_telefone = cpf_telefone
        self.endereco = endereco
        self.fidelidade = 0

class Peca:
    TABELA_PRECOS = {
        'Camisa': 15.0,
        'Calça': 20.0,
        'Toalha': 10.0,
        'Roupa Delicada': 25.0
    }

    def __init__(self, tipo, cor, estado, servico):
        self.tipo = tipo
        self.cor = cor
        self.estado = estado
        self.servico = servico
        self.preco = self._calcular_preco_peca()

    def _calcular_preco_peca(self):
        return self.TABELA_PRECOS.get(self.tipo, 10.0)

class Pedido:
    def __init__(self, id_pedido, cliente):
        self.id = id_pedido
        self.cliente = cliente
        self.pecas = []
        self.status = "Recebido"
        self.pagamento = "Aberto"
        self.valor_bruto = 0.0
        self.desconto = 0.0
        self.valor_liquido = 0.0
        self.data_criacao = datetime.datetime.now()

    def adicionar_peca(self, peca):
        self.pecas.append(peca)
        self.atualizar_totais()

    def atualizar_totais(self):
        self.valor_bruto = sum(p.preco for p in self.pecas)
        
        if len(self.pecas) >= 5:
            self.desconto = self.valor_bruto * 0.10
        
        self.valor_liquido = self.valor_bruto - self.desconto