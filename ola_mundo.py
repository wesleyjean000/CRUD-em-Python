import json

# --- Funções de Validação Centralizadas ---

def is_formato_nome_valido(nome):
    nome_tratado = nome.strip()
    if not nome_tratado:
        print("Erro: O nome não pode estar em branco.")
        return False
    if nome_tratado.isdigit():
        print("Erro: O nome não pode ser composto apenas por números.")
        return False
    if not all(c.isalpha() or c.isspace() for c in nome_tratado):
        print("Erro: O nome deve conter apenas letras e espaços.")
        return False
    return True

def is_formato_idade_valido(idade_str):
    if not idade_str.isdigit():
        print(f"Erro: '{idade_str}' não é uma idade válida. Por favor, use apenas números inteiros.")
        return False
    return True

# --- Funções Auxiliares ---

def obter_nome_valido():
    while True:
        nome = input("Por favor, digite seu nome: ")
        if is_formato_nome_valido(nome):
            return nome.strip()

def obter_idade_valida():
    while True:
        idade_str = input("Por favor, digite sua idade: ")
        if is_formato_idade_valido(idade_str):
            return int(idade_str)

def classificar_idade(idade):
    if idade < 13:
        return "criança"
    elif idade < 18:
        return "adolescente"
    else:
        return "adulto"

# --- Definição da Classe (O Molde) ---
# A classe é definida aqui para que ela possa usar a função classificar_idade, que já foi definida acima.
class Usuario:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        self.grupo = classificar_idade(idade)

    def atualizar_dados(self, novo_nome=None, nova_idade=None):
        if novo_nome:
            self.nome = novo_nome
        
        if nova_idade is not None: # Usamos 'is not None' para permitir idade 0
            self.idade = nova_idade
            self.grupo = classificar_idade(self.idade)

    def __str__(self):
        return f"Nome: {self.nome}, Idade: {self.idade}, Grupo: {self.grupo}"

def salvar_usuarios(lista_usuarios, nome_arquivo="usuarios.json"):
    
    try:
        # Usando List Comprehension para converter objetos em dicionários de forma concisa.
        lista_para_salvar = [{"nome": u.nome, "idade": u.idade} for u in lista_usuarios]

        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            # Agora salvamos a lista de dicionários, que o JSON entende
            json.dump(lista_para_salvar, f, indent=4, ensure_ascii=False)
        print(f"\nDados salvos com sucesso no arquivo '{nome_arquivo}'!")
    except IOError:
        print(f"Ocorreu um erro ao tentar salvar o arquivo '{nome_arquivo}'.")

def carregar_usuarios(nome_arquivo="usuarios.json"):
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            dados_em_dicionario = json.load(f)
            # Usando List Comprehension para converter dicionários em objetos.
            return [Usuario(nome=d['nome'], idade=d['idade']) for d in dados_em_dicionario]
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
    # Agora a verificação usa a notação de objeto: u.nome
    usuario_existe = any(u.nome.lower() == nome_usuario.lower() for u in usuarios_cadastrados)
    if usuario_existe:
        print(f"\nErro: O usuário '{nome_usuario}' já está cadastrado.")
        return
    
    idade_usuario = obter_idade_valida()
    # Criamos um novo OBJETO da classe Usuario
    novo_usuario = Usuario(nome=nome_usuario, idade=idade_usuario)
    usuarios_cadastrados.append(novo_usuario)
    print(f"\nUsuário {nome_usuario} cadastrado com sucesso!")
          
def listar_todos_usuarios(usuarios_cadastrados):
    
    print("\n--- Lista de Usuários Cadastrados ---")
    if not usuarios_cadastrados:
        print("Nenhum usuário cadastrado ainda.")
        return

    # Agora, o próprio objeto sabe como se apresentar de forma formatada.
    for usuario in usuarios_cadastrados:
         print(usuario)

def encontrar_usuario(nome_procurado, usuarios_cadastrados):
    
    for usuario in usuarios_cadastrados:
        if usuario.nome.lower() == nome_procurado.lower():
            return usuario
    return None

def deletar_usuario(usuarios_cadastrados):
    
    nome_para_deletar = input("Digite o nome do usuário que deseja deletar: ")

    usuario_encontrado = encontrar_usuario(nome_para_deletar, usuarios_cadastrados)

    if usuario_encontrado:
        confirmacao = input(f"Tem certeza que deseja deletar o usuário '{usuario_encontrado.nome}'? (s/n): ")
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
        print(f"\nEditando usuário: {usuario_encontrado.nome} (Idade atual: {usuario_encontrado.idade})")
                                                        
        print("Deixe em branco para não alterar.")

        # --- Loop para obter e validar o novo nome ---
        while True:
            novo_nome_str = input(f"Novo nome: ").strip()
            if not novo_nome_str: # Usuário deixou em branco para pular
                nome_para_atualizar = None
                break
            
            if not is_formato_nome_valido(novo_nome_str):
                continue # Formato inválido, pede o nome novamente
            
            if any(u.nome.lower() == novo_nome_str.lower() for u in usuarios_cadastrados if u is not usuario_encontrado):
                print(f"Erro: O nome '{novo_nome_str}' já está em uso. Tente outro.")
                continue # Nome já existe, pede o nome novamente
            
            nome_para_atualizar = novo_nome_str
            break # Nome é válido e único, sai do loop

        # --- Loop para obter e validar a nova idade ---
        while True:
            nova_idade_str = input(f"Nova idade: ").strip()
            if not nova_idade_str: # Usuário deixou em branco para pular
                idade_para_atualizar = None
                break
            
            if is_formato_idade_valido(nova_idade_str):
                idade_para_atualizar = int(nova_idade_str)
                break # Idade é válida, sai do loop

        # --- Chamada do Método (o objeto se atualiza) ---
        if nome_para_atualizar or idade_para_atualizar is not None:
            # A mágica acontece aqui: o próprio objeto é quem se atualiza.
            usuario_encontrado.atualizar_dados(novo_nome=nome_para_atualizar, nova_idade=idade_para_atualizar)
            print("Usuário atualizado com sucesso!")
        else:
            print("Nenhuma alteração fornecida.")
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

# Esta construção garante que a função main() só seja executada
# quando o script é rodado diretamente.
if __name__ == '__main__':
    main()