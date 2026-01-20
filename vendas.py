import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent
PRODUTOS_FILE = BASE_DIR / "produtos.json"
VENDAS_FILE = BASE_DIR / "vendas.json"


class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def to_dict(self):
        return {
            "preco": self.preco,
            "estoque": self.estoque
        }


class SistemaVendas:
    def __init__(self):
        self.produtos = self.carregar_dados(PRODUTOS_FILE)
        self.vendas = self.carregar_dados(VENDAS_FILE)

    def carregar_dados(self, arquivo):
        if arquivo.exists():
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def salvar_dados(self, arquivo, dados):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def cadastrar_produto(self):
        nome = input("Nome do produto: ").strip()
        preco = float(input("Preço: "))
        estoque = int(input("Estoque: "))

        produto = Produto(nome, preco, estoque)
        self.produtos[nome] = produto.to_dict()
        self.salvar_dados(PRODUTOS_FILE, self.produtos)

        print("Produto cadastrado com sucesso.\n")

    def listar_produtos(self):
        if not self.produtos:
            print("Nenhum produto cadastrado.\n")
            return

        for nome, dados in self.produtos.items():
            print(f"{nome} | Preço: R$ {dados['preco']} | Estoque: {dados['estoque']}")
        print()

    def editar_produto(self):
        self.listar_produtos()
        nome = input("Produto a editar: ").strip()

        if nome not in self.produtos:
            print("Produto não encontrado.\n")
            return

        preco = float(input("Novo preço: "))
        estoque = int(input("Novo estoque: "))

        self.produtos[nome]["preco"] = preco
        self.produtos[nome]["estoque"] = estoque
        self.salvar_dados(PRODUTOS_FILE, self.produtos)

        print("Produto atualizado.\n")

    def remover_produto(self):
        self.listar_produtos()
        nome = input("Produto a remover: ").strip()

        if nome in self.produtos:
            del self.produtos[nome]
            self.salvar_dados(PRODUTOS_FILE, self.produtos)
            print("Produto removido.\n")
        else:
            print("Produto não encontrado.\n")

    def registrar_venda(self):
        self.listar_produtos()
        nome = input("Produto vendido: ").strip()

        if nome not in self.produtos:
            print("Produto não encontrado.\n")
            return

        quantidade = int(input("Quantidade: "))

        if quantidade > self.produtos[nome]["estoque"]:
            print("Estoque insuficiente.\n")
            return

        total = quantidade * self.produtos[nome]["preco"]
        self.produtos[nome]["estoque"] -= quantidade

        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.vendas[data] = {
            "produto": nome,
            "quantidade": quantidade,
            "total": total
        }

        self.salvar_dados(PRODUTOS_FILE, self.produtos)
        self.salvar_dados(VENDAS_FILE, self.vendas)

        print(f"Venda registrada. Total: R$ {total}\n")

    def historico_vendas(self):
        if not self.vendas:
            print("Nenhuma venda registrada.\n")
            return

        for data, venda in self.vendas.items():
            print(f"{data} - {venda['produto']} x{venda['quantidade']} = R$ {venda['total']}")
        print()

    def relatorio_faturamento(self):
        total = sum(venda["total"] for venda in self.vendas.values())
        print(f"Faturamento total: R$ {total}\n")

    def menu(self):
        while True:
            print("===== SISTEMA DE VENDAS =====")
            print("1 - Cadastrar produto")
            print("2 - Listar produtos")
            print("3 - Editar produto")
            print("4 - Remover produto")
            print("5 - Registrar venda")
            print("6 - Histórico de vendas")
            print("7 - Relatório de faturamento")
            print("0 - Sair")

            opcao = input("Escolha: ")

            if opcao == "1":
                self.cadastrar_produto()
            elif opcao == "2":
                self.listar_produtos()
            elif opcao == "3":
                self.editar_produto()
            elif opcao == "4":
                self.remover_produto()
            elif opcao == "5":
                self.registrar_venda()
            elif opcao == "6":
                self.historico_vendas()
            elif opcao == "7":
                self.relatorio_faturamento()
            elif opcao == "0":
                break
            else:
                print("Opção inválida.\n")


if __name__ == "__main__":
    sistema = SistemaVendas()
    sistema.menu()
