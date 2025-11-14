import json

def obter_nome_valido():
    
    while True:
        nome = input("Por favor, digite seu nome: ")
        
        if nome.strip() and not nome.strip().isdigit():
            return nome  
        else:
            print("Isso não parece um nome válido. Por favor, não use apenas números ou deixe em branco.")

def obter_idade_valida():
    
    while True:
        idade_str = input("Por favor, digite sua idade: ")
        try:
            idade_int = int(idade_str)
            return idade_int 
        except ValueError:
            print(f"'{idade_str}' não é uma idade válida. Por favor, use apenas números inteiros.")

def classificar_idade(idade):
    
    if idade < 13:
        return "criança"
    elif idade < 18:
        return "adolescente"
    else:
        return "adulto"

def salvar_usuarios(lista_usuarios, nome_arquivo="usuarios.json"):
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_usuarios, f, indent=4, ensure_ascii=False)
        print(f"\nDados salvos com sucesso no arquivo '{nome_arquivo}'!")
    except IOError:
        print(f"Ocorreu um erro ao tentar salvar o arquivo '{nome_arquivo}'.")

def carregar_usuarios(nome_arquivo="usuarios.json"):
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] 
    except (json.JSONDecodeError, IOError):
        print(f"Ocorreu um erro ao ler ou decodificar o arquivo '{nome_arquivo}'.")
        return [] 
    
def mostrar_menu():
    
    print("\n--- MENU PRINCIPAL ---")
    print("1. Cadastrar novo usuário")
    print("2. Listar todos os usuários")
    print("3. Deletar usuário")
    print("4. Editar usuário")
    print("5. Sair")
    return input("Escolha uma opção: ")

def adicionar_novo_usuario(usuarios_cadastrados):
    
    nome_usuario = obter_nome_valido()
    
    usuario_existe = any(u['nome'].lower() == nome_usuario.lower() for u in usuarios_cadastrados)
    if usuario_existe:
        print(f"\nErro: O usuário '{nome_usuario}' já está cadastrado.")
        return
    
    idade_usuario = obter_idade_valida()
    classificacao = classificar_idade(idade_usuario)
    
    dados_usuario = {
        "nome": nome_usuario,
        "idade": idade_usuario,
        "grupo": classificacao
    }
    usuarios_cadastrados.append(dados_usuario)
    print(f"\nUsuário {nome_usuario} cadastrado com sucesso!")
          
def listar_todos_usuarios(usuarios_cadastrados):
    
    print("\n--- Lista de Usuários Cadastrados ---")
    if not usuarios_cadastrados:
        print("Nenhum usuário cadastrado ainda.")
        return

    for usuario in usuarios_cadastrados:
         print(f"Nome: {usuario['nome']}, Idade: {usuario['idade']}, Grupo: {usuario['grupo']}")

def encontrar_usuario(nome_procurado, usuarios_cadastrados):
    
    for usuario in usuarios_cadastrados:
        if usuario['nome'].lower() == nome_procurado.lower():
            return usuario
    return None

def deletar_usuario(usuarios_cadastrados):
    
    nome_para_deletar = input("Digite o nome do usuário que deseja deletar: ")

    usuario_encontrado = encontrar_usuario(nome_para_deletar, usuarios_cadastrados)

    if usuario_encontrado:
        confirmacao = input(f"Tem certeza que deseja deletar o usuário '{usuario_encontrado['nome']}'? (s/n): ")
        if confirmacao.lower() == 's':
            usuarios_cadastrados.remove(usuario_encontrado)
            print("Usuário deletado com sucesso!")
        else:
            print("Operação cancelada.")
    else:
        print(f"Usuário com o nome '{nome_para_deletar}' não encontrado.")
def editar_usuario(usuarios_cadastrados):
    

    nome_para_editar = input("Digite o nome do usuário que deseja editar: ")

    usuario_encontrado = encontrar_usuario(nome_para_editar, usuarios_cadastrados)

    if usuario_encontrado:
        print(f"\nEditando usuário: {usuario_encontrado['nome']} (Idade: {usuario_encontrado['idade']})")
                                                        
        print("Deixe em branco para não alterar.")
        novo_nome = input(f"Novo nome (atual: {usuario_encontrado['nome']}): ")
        nova_idade_str = input(f"Nova idade (atual: {usuario_encontrado['idade']}): ")

        alguma_alteracao_sucesso = False

        
        if novo_nome.strip():
            nome_candidato = novo_nome.strip()
            
            if nome_candidato.isdigit():
                print("\nErro: O nome não pode ser composto apenas por números.")
            
            elif any(u['nome'].lower() == nome_candidato.lower() for u in usuarios_cadastrados if u is not usuario_encontrado):
                print(f"\nErro: O nome '{nome_candidato}' já está em uso. A alteração do nome foi cancelada.")
            else:
                usuario_encontrado['nome'] = nome_candidato
                alguma_alteracao_sucesso = True

        
        if nova_idade_str.strip().isdigit():
             usuario_encontrado['idade'] = int(nova_idade_str)
             usuario_encontrado['grupo'] = classificar_idade(usuario_encontrado['idade'])
             alguma_alteracao_sucesso = True
        elif nova_idade_str.strip(): 
            print("\nErro: A idade informada é inválida. Use apenas números.")

        
        if alguma_alteracao_sucesso:
            print("Usuário atualizado com sucesso!")
    else:
         print(f"Usuário com o nome '{nome_para_editar}' não encontrado.")                                                                            

def main():
    
    usuarios_cadastrados = carregar_usuarios() 
    print("--- Bem-vindo ao nosso programa de cadastro! ---")

    while True:
        escolha = mostrar_menu()
        if escolha == '1':
            adicionar_novo_usuario(usuarios_cadastrados)
        elif escolha == '2':
            listar_todos_usuarios(usuarios_cadastrados)
        elif escolha == '3':
            deletar_usuario(usuarios_cadastrados)
        elif escolha == '4':
            editar_usuario(usuarios_cadastrados)
        elif escolha == '5':
            salvar_usuarios(usuarios_cadastrados) 
            print("Saindo do programa. Até logo!")
            break
        else:
            print("\nOpção inválida. Por favor, escolha uma das opções do menu.")


main()