import json
import os
import getpass

PRECO_KWH = 0.95

def input_as_type(tp, prompt, error_message="Entrada inválida. Tente novamente.", default=None):
    while True:
        try:
            v = input(prompt)
            if v == "" and default is not None:
                return default
            if tp is None: return v
            return tp(v)
        except ValueError:
            print(error_message)
            if default is not None:
                print(f"Usando valor padrão: {default}")
                return default
            raise
def confirmar_acao(mensagem):
    resposta = input(f"{mensagem} (s/n): ").strip().lower()
    if resposta == 's':
        return True
    else:
        print("Ação cancelada.")
        return False

# Função para criar um novo usuário
def criar_usuario():
    print("=== Criar Novo Usuário ===")
    username = input_as_type(str, "Digite o nome de usuário: ")
    password = getpass.getpass("Digite a senha: ")

    # Verificar se o arquivo de usuários existe, se não, criar um novo
    if not os.path.exists("usuarios.json"):
        with open("usuarios.json", "w") as file:
            json.dump({}, file)

    # Carregar os usuários existentes
    with open("usuarios.json", "r") as file:
        usuarios = json.load(file)

    # Verificar se o nome de usuário já existe
    if username in usuarios:
        print("Nome de usuário já existe. Tente novamente.")
        return

    # Adicionar o novo usuário ao dicionário
    usuarios[username] = password

    # Salvar os usuários atualizados no arquivo
    with open("usuarios.json", "w") as file:
        json.dump(usuarios, file)

    print("Usuário criado com sucesso!")

# Função para fazer login
def login():   
    print("=== Login ===")
    username = input_as_type(str, "Digite o nome de usuário: ")
    password = getpass.getpass("Digite a senha: ")

    # Verificar se o arquivo de usuários existe
    if not os.path.exists("usuarios.json"):
        print("Nenhum usuário encontrado. Por favor, crie um usuário primeiro.")
        return False

    # Carregar os usuários existentes
    with open("usuarios.json", "r") as file:
        usuarios = json.load(file)

    # Verificar as credenciais do usuário
    if username in usuarios and usuarios[username] == password:
        print("Login bem-sucedido!")
        return True
    else:
        print("Nome de usuário ou senha incorretos. Tente novamente.")
        return False

# Função para criar um novo registro de energia
def criar_registro():
    print("=== Criar Novo Registro de Energia ===")
    regiao = input_as_type(str, "Digite a região: ")
    periodo = input_as_type(str, "Digite o período: ")
    energia_consumida = input_as_type(float, "Digite a energia consumida: ")
    energia_distribuida = input_as_type(float, "Digite a energia distribuída: ")
    if energia_distribuida < energia_consumida:
        print("A energia distribuída não pode ser menor que a energia consumida. Tente novamente.")
        return

    registro = {
        "regiao": regiao,
        "periodo": periodo,
        "energia_consumida": energia_consumida,
        "energia_distribuida": energia_distribuida
    }

    # Verificar se o arquivo de registros existe, se não, criar um novo
    if not os.path.exists("registros.json"):
        with open("registros.json", "w") as file:
            json.dump([], file)

    # Carregar os registros existentes
    with open("registros.json", "r") as file:
        registros = json.load(file)

    # Adicionar o novo registro à lista
    registros.append(registro)

    # Salvar os registros atualizados no arquivo
    with open("registros.json", "w") as file:
        json.dump(registros, file)

    print("Registro criado com sucesso!")

# Função para listar todos os registros de energia
def listar_registros():
    print("=== Listar Registros de Energia ===")
    # Verificar se o arquivo de registros existe
    if not os.path.exists("registros.json"):
        print("Nenhum registro encontrado.")
        return

    # Carregar os registros existentes
    with open("registros.json", "r") as file:
        registros = json.load(file)

    # Exibir os registros
    for idx, registro in enumerate(registros):
        print(f"Registro {idx + 1}:")
        print(f"Região: {registro['regiao']}")
        print(f"Período: {registro['periodo']}")
        print(f"Energia Consumida: {registro['energia_consumida']}")
        print(f"Energia Distribuída: {registro['energia_distribuida']}")
        print("-" * 20)

# Função para atualizar um registro de energia
def atualizar_registro():
    print("=== Atualizar Registro de Energia ===")
    # Verificar se o arquivo de registros existe
    if not os.path.exists("registros.json"):
        print("Nenhum registro encontrado.")
        return

    # Carregar os registros existentes
    with open("registros.json", "r") as file:
        registros = json.load(file)

    # Listar os registros para o usuário escolher qual atualizar
    listar_registros()
    try:
        escolha = input_as_type(int, "Digite o número do registro que deseja atualizar: ", 
            error_message="Entrada inválida. Por favor, digite um registro válido.", default=None)
        escolha -= 1  # Ajustar para índice baseado em zero
    except ValueError:
        return
    if not (0 <= escolha < len(registros)):
        print("Número de registro inválido. Tente novamente.")
        return

    print("Digite enter para manter o valor anteriror do campo.")
    try:
        regiao = input_as_type(str, 
            f"Digite a nova região ({registros[escolha]['regiao']}): ", 
            default=registros[escolha]["regiao"])
        periodo = input_as_type(str, 
            f"Digite o novo período ({registros[escolha]['periodo']}): ", 
            default=registros[escolha]["periodo"])
        energia_consumida = input_as_type(float, 
            f"Digite a nova energia consumida ({registros[escolha]['energia_consumida']}): ", 
            default=registros[escolha]["energia_consumida"])
        energia_distribuida = input_as_type(float, 
            f"Digite a nova energia distribuída ({registros[escolha]['energia_distribuida']}): ", 
            default=registros[escolha]["energia_distribuida"])
        if energia_distribuida < energia_consumida:
            print("A energia distribuída não pode ser menor que a energia consumida. Tente novamente.")
            return
        registros[escolha] = {
            "regiao": regiao,
            "periodo": periodo,
            "energia_consumida": energia_consumida,
            "energia_distribuida": energia_distribuida,
        }
        # Salvar os registros atualizados no arquivo
        with open("registros.json", "w") as file:
            json.dump(registros, file)
    except ValueError:
        print("Entrada inválida. Tente novamente.")
        return
    except IndexError:
        print("Número de registro inválido. Tente novamente.")
        return


# Função para excluir um registro de energia
def excluir_registro():
    print("=== Excluir Registro de Energia ===")
    # Verificar se o arquivo de registros existe
    if not os.path.exists("registros.json"):
        print("Nenhum registro encontrado.")
        return

    # Carregar os registros existentes
    with open("registros.json", "r") as file:
        registros = json.load(file)

    # Listar os registros para o usuário escolher qual excluir
    listar_registros()
    try: 
        escolha = input_as_type(int, "Digite o número do registro que deseja excluir: ", "Entrada inválida. Por favor, digite um registro válido.")
        escolha -= 1  # Ajustar para índice baseado em zero
    except ValueError: return

    # confirmar a exclusão do registro
    if not confirmar_acao("Tem certeza que deseja excluir este registro? (s/n): "):
        return

    if not (0 <= escolha < len(registros)):
        print("Número de registro inválido. Tente novamente.")
        return
    registros.pop(escolha)

    # Salvar os registros atualizados no arquivo
    with open("registros.json", "w") as file:
        json.dump(registros, file)

    print("Registro excluído com sucesso!")

#Faça uma funcao que calcule a energia que foi perdida durante a distribuição, ou seja a diferença entre o consumo e a distruibuida. E faça com que ele retorne a representação
#do valor que foi gasto em energia perdida, a tarifa media é de R$ 0,95/kwh
def calcular_energia_perdida():
    print("=== Calcular Energia Perdida ===")
    # Verificar se o arquivo de registros existe
    if not os.path.exists("registros.json"):
        print("Nenhum registro encontrado.")
        return

    # Carregar os registros existentes
    with open("registros.json", "r") as file:
        registros = json.load(file)

    for idx, registro in enumerate(registros):
        energia_perdida = registro["energia_distribuida"] - registro["energia_consumida"]
        custo_perdida = energia_perdida * PRECO_KWH
        print(f"Registro {idx + 1}:")
        print(f"Região: {registro['regiao']}")
        print(f"Período: {registro['periodo']}")
        print(f"Energia Perdida: {energia_perdida} kWh")
        print(f"Custo da Energia Perdida: R$ {custo_perdida:.2f}")
        print("-" * 20)



# Função principal para executar o programa

def main():
    usuario_logado = False
    while True:
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Menu Principal ===")
        
        # As opções de CRUD de registros de energia só ficam disponíveis após o login bem-sucedido
        if usuario_logado:
            print("3. Criar Registro de Energia")
            print("4. Listar Registros de Energia")
            print("5. Atualizar Registro de Energia")
            print("6. Excluir Registro de Energia")
            print("7. Mostrar Energia Perdida")
        else:
            print("1. Criar Usuário")
            print("2. Login")
        print("8. Sair")

        escolha = input_as_type(int, "Digite o número da opção desejada: ", "Entrada inválida. Por favor, digite um número válido.")
        if not usuario_logado:
            match escolha:
                case 1: criar_usuario()
                case 2:
                    if login():
                        usuario_logado = True
                case 8: print("Saindo do programa. Até mais!")
                case _: print("Opção inválida. Tente novamente.")
        else:
            match escolha:
                case 3: criar_registro()    
                case 4: listar_registros()
                case 5: atualizar_registro()
                case 6: excluir_registro()
                case 7: calcular_energia_perdida()
                case 8:
                    print("Saindo do programa. Até mais!")
                    break
                case _: print("Opção inválida. Tente novamente.")
        input("\nPressione Enter para continuar...\n")
        

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")