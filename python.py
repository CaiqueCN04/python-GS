import json
import requests

def cadastrar_usuario(tipo_usuario):
    while True:
    # Função para cadastrar médico ou paciente
        if tipo_usuario == 'medico':
            # Solicitar informações específicas do médico
            crm = input("Digite o CRM: ")
            usuario = {"crm": crm}
        elif tipo_usuario == 'paciente':
            
            # Solicitar informações específicas do paciente
            cep = input("Digite o CEP: ")

            endereco = buscar_cep(cep)
            print("\nConfirme as informações do CEP:")
            print(f"CEP: {endereco['cep']}")
            print(f"Logradouro: {endereco['logradouro']}")
            print(f"Complemento: {endereco['complemento']}")
            print(f"Bairro: {endereco['bairro']}")
            print(f"Localidade: {endereco['localidade']}")
            print(f"UF: {endereco['uf']}")
            
            confirmar_cep = input("As informações do CEP estão corretas? (s/n): ").lower()
            if confirmar_cep != 's':
                print("Cadastro cancelado.")
                return

            if not endereco:
                print('CEP não encontrado. Verifique o CEP e tente novamente.')
                return

            rua = endereco.get('logradouro', '')
            bairro = endereco.get('bairro', '')
            municipio = endereco.get('localidade', '')
            uf = endereco.get('uf', '')
            complemento = endereco.get('complemento','')

            numero = input("Digite o número da residência: ")
            complemento = input("Digite o complemento: ")
            usuario = {"cep": cep, "numero": numero, "complemento": complemento}
        else:
            print("Tipo de usuário inválido.")
            return

        # Solicitar informações comuns a ambos os usuários
        nome = input("Digite o nome: ")

        cpf = input("Digite o CPF: ")
        if len(cpf) != 11 or not cpf.isdigit():
            print("O número do CPF de identificação deve conter 11 dígitos numéricos. Tente novamente.")       
            continue
        
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")

        # Adicionar informações ao arquivo JSON correspondente
        arquivo_json = f"{tipo_usuario}s.json"
        try:
            with open(arquivo_json, 'r') as arquivo_leitura:
                usuarios = json.load(arquivo_leitura)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            # Se o arquivo estiver vazio ou com formato inválido, cria uma lista vazia
            usuarios = []

        with open(arquivo_json, 'w') as arquivo:
            # Adiciona o novo usuário à lista existente
            usuarios.append({"cpf": cpf, "nome": nome, "email": email, "senha": senha, **usuario})
            json.dump(usuarios, arquivo, indent=2)
        return
def buscar_cep(cep):
    while True:
        try:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dicionario = resposta.json()
                if 'erro' in dicionario:
                    print("Erro: CEP não existe. ")
                    novo_cep = input("Digite o CEP novamente: ")
                    if novo_cep.isdigit() and len(novo_cep) == 8:
                        cep = novo_cep
                    else:
                        print("CEP invalido. Tente novamente. ")
                else:
                    return dicionario
            else:
                print(f"Erro: Status code {resposta.status_code}")
                novo_cep = input("Digite o CEP novamente: ")
                if novo_cep.isdigit() and len(novo_cep) == 8:  #verifica se tem 8 dígitos no CEP
                    cep = novo_cep
                else:
                    print("CEP inválido. Tente novamente. ")
        except requests.exceptions.ConnectTimeout:
            print('Erro ao carregar API, aguarde..')
            continue

def realizar_login(tipo_usuario):
    # Função para realizar login como médico ou paciente
    cpf_ou_crm = input("Digite o CPF ou CRM: ")
    senha = input("Digite a senha: ")

    # Verificar se o usuário existe no arquivo JSON correspondente
    arquivo_json = f"{tipo_usuario}s.json"
    try:
        with open(arquivo_json, 'r') as arquivo:
            usuarios = json.load(arquivo)
            usuario = next((u for u in usuarios if u.get("cpf") == cpf_ou_crm), None)
            if usuario and usuario["senha"] == senha:
                print("Login bem-sucedido.")
                if tipo_usuario == 'medico':
                    menu_medico()
                elif tipo_usuario == 'paciente':
                    menu_paciente()
            else:
                print("Credenciais inválidas.")
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("Nenhum usuário cadastrado. Faça o cadastro primeiro.")

def menu_medico():
    # Menu para médicos
    print("1. Presencial em um hospital")
    print("2. Online")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        print("Opções para analisar pré-diagnósticos ou sair do programa.")
    elif opcao == '2':
        print("1. Validar pré-diagnósticos")
        print("2. Ficar disponível para telemedicina")
        print("3. Sair do programa")
        opcao = input("Escolha uma opção: ")
        if opcao == '2':
            print("Aguardando por paciente... (Pressione 0 para retornar ao menu)")

def menu_paciente():
   
    # Menu para pacientes
    print("1. Pré-diagnóstico com chatbot")
    print("2. Marcar exames")
    print("3. Sair do programa")
    opcao = input("Escolha uma opção: ")

    if opcao == '2':
        print("Ainda em desenvolvimento. (Pressione 0 para voltar ao menu)")

    elif opcao == '1':
        print("Quais sintomas você está sentindo?")
        sintomas = input()
        print("Há quanto tempo você está sentindo cada sintoma?")
        tempo_sintomas = input()
        print("Diagnóstico por IA ainda em desenvolvimento.")
        print("1. Atendimento por telemedicina")
        print("2. Atendimento em hospital")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            print("Aguardando atendimento por telemedicina...")
        elif opcao == '2':
            print("Dirija-se ao hospital mais próximo.")
        elif opcao == '0':
            menu_paciente()

# Programa principal
print("Bem-vindo ao sistema médico!")
tipo_usuario = input("Você é um médico ou paciente? Digite 'medico' ou 'paciente': ")

while True:
    opcao = input("Escolha 1 para login, 2 para cadastro ou 0 para sair: ")

    if opcao == '1':
        realizar_login(tipo_usuario)
    elif opcao == '2':
        cadastrar_usuario(tipo_usuario)
    elif opcao == '0':
        print("Saindo do programa. Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")
