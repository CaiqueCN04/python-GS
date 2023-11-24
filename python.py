import json
import requests
 
def cadastrar_usuario(tipo_usuario):


    while True:
        
    # Função para cadastrar médico ou paciente
        if tipo_usuario == 'medico':
            # Solicitar informações específicas do médico
            crm = input("Digite o CRM: ")
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
            usuario = {"crm": crm, "cep": cep,"UF":uf,"Município":municipio,"Bairro":bairro,"Rua":rua, "numero": numero, "complemento": complemento}
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
            usuario = {"cep": cep,"UF":uf,"Município":municipio,"Bairro":bairro,"Rua":rua, "numero": numero, "complemento": complemento}
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
        if "@" not in email:
            print("o email deve ter um @")
            continue
        senha = input("Digite a senha: ")
        if len(senha) != 8:
            print("a senha deve conter no minimo 8 caracteres")
            continue
 
        # Adicionar informações ao arquivo JSON correspondente
        arquivo_json = f"{tipo_usuario}s.json"
        try:
            with open(arquivo_json, 'r') as arquivo_leitura:
                usuarios = json.load(arquivo_leitura)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            # Se o arquivo estiver vazio ou com formato inválido, cria uma lista vazia
            usuarios = []
 
        
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
    cpf = input("Digite o CPF: ")
    senha = input("Digite a senha: ")
 
    # Verificar se o usuário existe no arquivo JSON correspondente
    arquivo_json = f"{tipo_usuario}s.json"
    try:
        with open(arquivo_json, 'r') as arquivo:
            usuarios = json.load(arquivo)
            usuario = next((u for u in usuarios if u.get("cpf") == cpf), None)
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
 
def medico_presencial():
    print('1 - Analisar diagnósticos')
    print('0 - Sair do programa')
    opcao = input('Escolha:')
    if opcao == '1':
        print('\nAguardando pré-diagnósticos para análise\n')
        medico_presencial()
    elif opcao == '0':
        return
   
def medico_online():
    print("1 - Validar pré-diagnósticos")
    print("2 - Ficar disponível para telemedicina")
    print("0 - Sair do programa")
    opcao = input("Escolha uma opção: ")
    if opcao == '1':
        print('Nenhum pré-diagnóstico para validação disponível até o momento')
        medico_online()
    elif opcao == '2':
        print("\nAguardando por paciente...\n")
        medico_online()
    elif opcao == '0':
        return
 
def menu_medico():
    # Menu para médicos
    print('\nVocê está trabalhando:\n')
    print("1 - Presencial em um hospital")
    print("2 - Online")
    opcao = input("Escolha uma opção: ")
 
    if opcao == '1':
        medico_presencial()
    elif opcao == '2':
        medico_online()
    else:
        print('Opção invalida, tente novamente')
           
 
def menu_paciente():
  while True:
    # Menu para pacientes
    print("1 - Pré-diagnóstico com chatbot")
    print("2 - Marcar exames")
    print("0 - Sair do programa")
    opcao = input("Escolha uma opção: ")
 
    if opcao == '2':
        print("\nAinda em desenvolvimento...\n")
 
    elif opcao == '1':
        print("Quais sintomas você está sentindo?")
        sintomas = input()
        print("Há quanto tempo você está sentindo cada sintoma?")
        tempo_sintomas = input()
        print("\nDiagnóstico por IA ainda em desenvolvimento.\n")
        print("1 - Atendimento por telemedicina")
        print("2 - Atendimento em hospital")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            print("\nAguardando atendimento por telemedicina...\n")
        elif opcao == '2':
            print("\nDirija-se ao hospital mais próximo.\n")
        elif opcao == '0':
            menu_paciente()
    elif opcao == '0':
        return
 
# Programa principal
print("Bem-vindo ao sistema médico!")
print('Você é um:')
print(' - Médico')
print(' - Paciente')
tipo_usuario = input("Digite 'medico' ou 'paciente': ")
 
while True:
    opcao = input("Escolha:\n1 - para login\n2 - para cadastro\n3 - para mudar o tipo de usuário \n0 - para encerrar programa\n")
 
    if opcao == '1':
        realizar_login(tipo_usuario)
    elif opcao == '2':
        cadastrar_usuario(tipo_usuario)
    elif opcao == '3':
        tipo_usuario = input('Deseja entrar como medico ou paciente:\n')
    elif opcao == '0':
        print("Encerrando programa. Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")