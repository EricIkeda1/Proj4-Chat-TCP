import socket
import threading

# Escolha da cifra de criptografia pelo usuário
print("Escolha a cifra de criptografia: ")
print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")
print("5. RC4")
print("6. DES")
escolha = input("Digite o número da cifra desejada: ")

# Solicitação da chave de criptografia
chave = input("Digite a chave:")

# Solicitação do texto plano apenas se RC4 for selecionada
texto_plano = ""
if escolha == '5':
    texto_plano = input("Digite o texto plano: ")
elif escolha == '6':
    pass

# Função que implementa a Cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''
    deslocamento = chave if criptografar else -chave
    for caractere in mensagem:
        if caractere.isalpha():
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere
    return resultado

# Função que implementa a Substituição Monoalfabética
def cifra_monoalfabetica(mensagem, chave, criptografar=True):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Alfabeto original
    alfabeto_substituido = 'QWERTYUIOPLKJHGFDSAZXCVBNM'  # Alfabeto substituído
    
    chave = chave.upper()  # Converte a chave para maiúsculas
    
    if criptografar:
        # Cria um mapa de substituição usando o alfabeto original e substituído
        mapa_chave = {alfabeto[i]: alfabeto_substituido[i] for i in range(26)}
    else:
        # Cria um mapa de substituição invertido para descriptografar
        mapa_chave = {alfabeto_substituido[i]: alfabeto[i] for i in range(26)}

    resultado = ''  # Inicializa a string para armazenar o resultado
    for caractere in mensagem.upper():  # Converte a mensagem para maiúsculas e itera sobre cada caractere
        resultado += mapa_chave.get(caractere, caractere)  # Substitui o caractere ou mantém o original
    return resultado  # Retorna a mensagem criptografada ou descriptografada

# Função que implementa a Cifra de Playfair
# Função para criar a matriz de Playfair
def criar_matriz_playfair(chave):
    alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # I e J combinados
    matriz = []
    used = {}

    # Adiciona a chave à matriz, removendo duplicatas
    for char in chave.upper():
        if char not in used and char != ' ':
            matriz.append(char)
            used[char] = True

    # Adiciona as letras restantes do alfabeto à matriz
    for char in alfabeto:
        if char not in used:
            matriz.append(char)

    # Forma a matriz 5x5
    return [matriz[i:i + 5] for i in range(0, 25, 5)]

# Função para encontrar a posição de uma letra na matriz
def encontrar_indices(matriz, letra):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == letra.upper():
                return (i, j)
    return (-1, -1)  # Letra não encontrada

# Função de criptografia com a cifra de Playfair
def criptografar_playfair(mensagem, chave):
    matriz = criar_matriz_playfair(chave)
    mensagem_cifrada = ''
    digrama = ''
    mensagem_sem_espacos = mensagem.replace(' ', '')  # Remove espaços temporariamente

    if len(mensagem_sem_espacos) % 2 != 0:
        mensagem_sem_espacos += 'X'  # Adiciona um X se o comprimento for ímpar

    for i in range(len(mensagem_sem_espacos)):
        char = mensagem_sem_espacos[i]
        char_upper = char.upper()
        if char_upper == 'J':
            digrama += 'I'
        else:
            digrama += char_upper

        if len(digrama) == 2:
            i1, j1 = encontrar_indices(matriz, digrama[0])
            i2, j2 = encontrar_indices(matriz, digrama[1])

            if i1 == i2:  # Mesma linha
                mensagem_cifrada += matriz[i1][(j1 + 1) % 5] + matriz[i2][(j2 + 1) % 5]
            elif j1 == j2:  # Mesma coluna
                mensagem_cifrada += matriz[(i1 + 1) % 5][j1] + matriz[(i2 + 1) % 5][j2]
            else:  # Retângulo
                mensagem_cifrada += matriz[i1][j2] + matriz[i2][j1]
            digrama = ''

    return mensagem_cifrada

# Função de descriptografia com a cifra de Playfair
def descriptografar_playfair(mensagem_cifrada, chave):
    matriz = criar_matriz_playfair(chave)
    mensagem_clara = ''
    digrama = ''
    mensagem_sem_espacos = mensagem_cifrada.replace(' ', '')  # Remove espaços temporariamente

    for i in range(0, len(mensagem_sem_espacos), 2):
        char1 = mensagem_sem_espacos[i].upper()
        char2 = mensagem_sem_espacos[i + 1].upper()

        i1, j1 = encontrar_indices(matriz, char1)
        i2, j2 = encontrar_indices(matriz, char2)

        if i1 == i2:  # Mesma linha
            mensagem_clara += matriz[i1][(j1 - 1 + 5) % 5] + matriz[i2][(j2 - 1 + 5) % 5]
        elif j1 == j2:  # Mesma coluna
            mensagem_clara += matriz[(i1 - 1 + 5) % 5][j1] + matriz[(i2 - 1 + 5) % 5][j2]
        else:  # Retângulo
            mensagem_clara += matriz[i1][j2] + matriz[i2][j1]

    return mensagem_clara

# Função que implementa a Cifra de Vigenère
def cifra_de_vigenere(mensagem, chave, criptografar=True):
    resultado = ''
    chave = chave.lower()
    indice_chave = 0
    
    for caractere in mensagem:
        if caractere.isalpha():
            deslocamento = ord(chave[indice_chave]) - ord('a')
            deslocamento = deslocamento if criptografar else -deslocamento
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
            indice_chave = (indice_chave + 1) % len(chave)
        else:
            resultado += caractere
    return resultado

texto_plano = "ATACARBASENORTE"
chave = chave.upper()
texto_criptografado = cifra_de_vigenere(texto_plano, chave)

# Função RC4
def rc4(key, text):
    # Inicialização do vetor S
    S = list(range(256))
    j = 0
    key_length = len(key)

    # Inicialização da chave
    for i in range(256):
        j = (j + S[i] + ord(key[i % key_length])) % 256  # Convertendo para ASCII
        S[i], S[j] = S[j], S[i]

    # Geração do fluxo de chave e criptografia do texto
    i = j = 0
    result = []
    
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(chr(ord(char) ^ K))

    # Preparação do resultado criptografado
    encrypted_text = ''.join(result)
    return encrypted_text

# Função que implementa o DES
def rotate_left(bits, n):
    return bits[n:] + bits[:n]

def permute(key, pc_2_table):
    return ''.join([key[i-1] for i in pc_2_table])

def generate_subkey(c1, d1, pc_2_table, shift_amount):
    # Realizar a rotação à esquerda
    c2 = rotate_left(c1, shift_amount)
    d2 = rotate_left(d1, shift_amount)
    
    # Concatenar c2 e d2
    combined = c2 + d2
    
    # Aplicar permutação PC-2
    k2 = permute(combined, pc_2_table)
    
    return k2

# Dados de entrada
c1 = "11100001100110010101010111111"
d1 = "10101010110011001111100011110"

# Tabela PC-2 fornecida na imagem
pc_2_table = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
              26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
              51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

# Número de rotações à esquerda para k2 (2ª iteração)
shift_amount = 1

# Gerar a subchave k2
k2 = generate_subkey(c1, d1, pc_2_table, shift_amount)


# Função que aplica a cifra escolhida na mensage
def criptografar_mensagem(mensagem, escolha, chave):
    chave = chave.upper()  # Converte a chave para letras maiúsculas
    chave_bytes = chave.encode()
    
    if escolha == '1':
        return cifra_de_cesar(mensagem, int(chave))
    elif escolha == '2':
        return cifra_monoalfabetica(mensagem, chave)
    elif escolha == '3':
        return criptografar_playfair(mensagem, chave)
    elif escolha == '4':
        return cifra_de_vigenere(mensagem, chave)
    elif escolha == '5':  # RC4
        return rc4(chave, mensagem)
    elif escolha == '6':
        k2 = generate_subkey(c1, d1, pc_2_table, shift_amount)
        print(f"Resultado do DES (Subchave k2): {k2}")
        return None 
    else:
        raise ValueError("Cifra inválida.")

# Função que recebe mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            if escolha == '3':
                print(f"Texto Plano: {texto_plano}")
            if escolha == '5':  # RC4
                print(f"Texto Plano: {texto_plano}")
                texto_plano_ascii = [ord(c) for c in texto_plano]
                print(f"Texto Plano ASCII: {texto_plano_ascii}")
                mensagem_criptografada = criptografar_mensagem(texto_plano, escolha, chave)
                print(f"Texto Criptografado: {[ord(c) for c in mensagem_criptografada]}")
                print(f"Chave: {chave}")
                chave_ascii = [ord(c) for c in chave]
                print(f"Chave ASCII: {chave_ascii}")
            elif escolha == '6':
                # Gera a subchave k2 para DES e exibe o resultado apenas para a escolha DES
                k2 = generate_subkey(c1, d1, pc_2_table, shift_amount)
                print(f"Resultado do DES (Subchave k2): {k2}")
            
            # Para todas as outras cifras, exibe a mensagem recebida
            else:
                print(mensagem)
        except:
            print("Ocorreu um erro!")
            cliente.close()
            break
        
# Função que envia mensagens para o servidor
def enviar_mensagens():
    while True:
        mensagem = '{}: {}'.format(apelido, input(''))
        mensagem_criptografada = criptografar_mensagem(mensagem, escolha, chave)
        if escolha == '5':  # RC4
            print(f"Texto Criptografado a ser enviado: {[ord(c) for c in mensagem_criptografada]}")
        # Encode em utf-8 para evitar erro de caracteres fora do padrão ASCII
        cliente.send(''.join(mensagem_criptografada).encode('ASCII'))
        
def conectar():
    global cliente
    target_host = input("Digite o IP do servidor ao qual deseja se conectar: ")
    target_port = 50000  # Porta padrão
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((target_host, target_port))
    print(f"Conectado ao servidor {target_host} na porta {target_port}")
    print("Aperte Enter para Prosseguir")
    print("Digite a mensagem:")
    
def main():
    conectar()
    while True:
        global comandos
        comandos = cliente.recv(4000).decode()
            
# Iniciando o cliente
apelido = input("Escolha um apelido: ")
conectar()

# Iniciando threads para envio e recebimento de mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagens)
thread_enviar.start()
