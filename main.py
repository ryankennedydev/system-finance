import _sqlite3
from datetime import datetime

conexao = _sqlite3.connect("banco_financas.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS controle_financeiro(
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               tipo TEXT NOT NULL CHECK(tipo in ('receita','despesa')),
               valor REAL NOT NULL,
               descricao TEXT,
               mes INTEGER NOT NULL,
               ano  INTEGER NOT NULL
               )
""")


def adicionar_transacao(conexao,tipo,valor,descricao,mes,ano):
    cursor = conexao.cursor()


    cursor.execute("""
    INSERT INTO controle_financeiro (tipo,valor,descricao,mes,ano)
    VALUES (?,?,?,?,?)
""", (tipo,valor,descricao,mes,ano))

    conexao.commit()
    
def editar_transacao(conexao,id):
    cursor = conexao.cursor()

    try:
        editar_transacao = int(input(f"1-Tipo\n2-Valor\n3-Descricao\n4-DATA\nEscolha uma das opções para editar na transação de id {id}"))
         
        match editar_transacao:
            case 1:
                tipo_editado = input("Digite o texto que você quer editar:")
                try:

                    cursor.execute(f"""
                    UPDATE controle_financeiro SET tipo = (?) WHERE id = (?)
                """,(tipo_editado,id))
                    conexao.commit()

                except:
                    print("Utiliza apenas PALAVRAS!")
            case 2:
                valor_editado = float(input("Digite o valor que você quer editar:"))
                try:
                    cursor.execute(f"""
                    UPDATE controle_financeiro SET valor = ? WHERE id = ?
                """,(valor_editado,id))
                    conexao.commit()
                    print("Valor editado com sucesso!")
                except:
                    print("Utilize apenas Números")
            case 3:
                descricao_editado = input("Digite o valor que você quer editar:")
                try:

                    cursor.execute(f"""
                    UPDATE controle_financeiro SET descricao = ? WHERE id = ?
                    """,(descricao_editado,id))
                    conexao.commit()
                    print("Descrição atualizada com sucesso!")
                except:
                    print("Utilize apenas PALAVRAS!")
            case 4:
                data_transacao = int(input(f"1-Mês\n2-Ano\n3-Mês e Ano\nEscolha uma das opções:"))
                try:
                    match data_transacao:
                        case 1:
                            mes_transacao = int(input("Escolha um mês de Janeiro(1) à Dezembro(12)"))
                            if mes_transacao >= 1 and mes_transacao <=12:
                                cursor.execute(f"""
                                UPDATE controle_financeiro SET mes = (?) WHERE id = (?)
                                    """,(mes_transacao,id))
                                conexao.commit()
                                print("Mês atualizado com sucesso!")
                            else:
                                print("Esse mês não existe!")
                        case 2:
                            ano_atual = datetime.now().year
                            ano_transacao = int(input(f"Escolha um ano que seja menor ou igual à {ano_atual}:"))
                            if ano_transacao <= ano_atual:
                                cursor.execute(f"""
                                UPDATE controle_financeiro SET ano = (?) WHERE id = (?)  
                                    """,(ano_transacao,id))
                                conexao.commit()
                                print("Ano atualizado com sucesso!")
                            else:
                                print("Digite um ano válido!")
                except:
                    print("Utilize apenas números!")
    except:
        print("Id de transação não encontrado!")

def remover_transacao(conexao,id):
    cursor = conexao.cursor()
    try:
        cursor.execute(f"""
        DELETE FROM controle_financeiro WHERE id= (?)
""",(id,))
        conexao.commit()
        print("Transação removida com sucesso!")

    except:
        print("ID não encontrado!")

def listar_transacao(conexao):
    cursor = conexao.cursor()
    
    menu_lista = int(input("1-Listar Todas Transações\n2-Listar Transação Específica\nEscolha uma das opções"))

    try:
        match menu_lista:
            
            case 1:
                cursor.execute("""SELECT * FROM controle_financeiro""")
                contas = cursor.fetchall()
                for i in contas:
                    print(i)
            case 2:
                id_listagem = int(input("Digite o id da transação que você deseja visualizar: "))
                try:
                    cursor.execute("""SELECT * FROM controle_financeiro WHERE id = (?)""",(id_listagem,))
                    conta = cursor.fetchone()
                    print(conta)
                    
                except:
                    print("Erro, Verifique o id!")
    except:
        print("Utilize apenas NÚMEROS")


while True:

    menu = int(input("1-Adicionar Transação\n2-Editar Transação\n3-Listar Transações\n4-Remover Transação\n5-Sair"))

    try:

        match menu:
            case 1:
                tipo = input("Tipo da transação (receita/despesa): ")
                valor = float(input("Valor: "))
                descricao = input("Descrição: ")
                mes = int(input("Mês: "))
                ano = int(input("Ano: "))
                adicionar_transacao(conexao, tipo, valor, descricao, mes, ano)
            
            
            case 2:
                valor_id = int(input("Qual o id? "))
                editar_transacao(conexao,valor_id)

            case 3:
                listar_transacao(conexao)

            case 4:
                valor_id = int(input("Qual o valor do id da transação a ser removido:"))
                remover_transacao(conexao,valor_id)
            
            case 5:
                print("Obrigado por usar nosso sistema financeiro.\nSaindo...")
                break
    except:
        print("Escolha apenas as opções fornecidas!")
    
