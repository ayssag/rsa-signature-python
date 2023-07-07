from ..utils.general import readFile
from keyGenerator import generateAesKey
import numpy as np

def formatInput(string_bytes):
    data = [byte for byte in string_bytes]
    # Calcula o número de bytes extras para preencher a matriz
    matrix = np.resize(data,(4,4))
    # # Preenche o array de bytes com zeros extras, se necessário
    # padded_bytes = data + bytes([0] * extra_bytes)

    # # Cria a matriz 4x4
    # number_of_blocks = len(padded_bytes)//16
    # i = 0
    # matrix_transposed = []
    # for _ in range(number_of_blocks):
    #     block = padded_bytes[i:i+16]
    #     matrix_transposed.append(block)
    #     i += 16

    # missing_blocks = 16 - len(matrix_transposed)
    # if missing_blocks:
    #     for _ in range(missing_blocks):
    #         matrix_transposed.append(b'0')
    # matrix_transposed = np.reshape(matrix_transposed, (4,4))
    # matrix = np.transpose(matrix_transposed)

    return matrix

SBOX = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]


RCON = [
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1B, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00]
]

def expandKey(key):
    # RCON (Round Constant) para a expansão da chave
    rcon = [
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
    ]

    # Tamanho da chave e número de palavras de 32 bits
    key_size = len(key)
    num_words = key_size // 4

    # Número de rodadas para o AES-128
    num_rounds = 10

    # Inicialização da chave expandida
    expanded_key = list(key)

    # Expansão da chave
    for i in range(num_words, 4 * (num_rounds + 1)):
        temp = expanded_key[(i-1)*4:i*4]

        if i % num_words == 0:
            # Realiza a rotação de uma palavra
            temp = temp[1:] + temp[:1]

            # Substitui cada byte pelo byte correspondente na S-Box
            temp = [SBOX[byte] for byte in temp]

            # Realiza o XOR com a RCON atual
            temp[0] ^= rcon[i//num_words - 1]
        elif num_words > 6 and i % num_words == 4:
            # Substitui cada byte pelo byte correspondente na S-Box
            temp = [SBOX[byte] for byte in temp]

        # Realiza o XOR com a palavra anterior
        temp = [temp[j] ^ expanded_key[(i-num_words)*4+j] for j in range(4)]

        # Adiciona a palavra expandida à chave expandida
        expanded_key.extend(temp)

    return expanded_key

def roundKeys(expanded_key):
    matrixes = []

    for i in range(0, len(expanded_key), 16):
        matrix = []
        for j in range(4):
            linha = expanded_key[i+j*4:i+j*4+4]
            matrix.append(linha)
        matrixes.append(matrix)

    return matrixes

def replaceBytes(state):
    state_matrix = np.array(state)
    # Convert numpy array to Python list
    state_list = state_matrix.tolist()

    # Convert each element to a list of integer byte values
    state_bytes = [[ch for ch in bytes(element)] for row in state_list for element in row]
    # Reshape the list of byte values into a 4x4 matrix
    new_state_matrix = np.array(state_bytes).reshape(4, 4)

    for i in range(4):
        for j in range(4):
            state[i][j] = SBOX[state[i][j]]

    return state

def shiftRows(state):
    for i in range(1, 4):
        state[i] = state[i][i:] + state[i][:i]
    
    return state

def mixColumns(state):
    for j in range(4):
        column = [state[i][j] for i in range(4)]
        state[0][j] = (column[0] << 1) ^ (column[1] ^ column[2] ^ (column[3] << 1))
        state[1][j] = (column[1] << 1) ^ (column[2] ^ column[3] ^ (column[0] << 1))
        state[2][j] = (column[2] << 1) ^ (column[3] ^ column[0] ^ (column[1] << 1))
        state[3][j] = (column[3] << 1) ^ (column[0] ^ column[1] ^ (column[2] << 1))
    
    return state

def addRoundKey(state, round, round_keys):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_keys[round][i][j]
    
    return state

def aesRound(state, round, round_keys):
    state = replaceBytes(state)
    state = shiftRows(state)
    if not round == 10:
        state = mixColumns(state)
    state = addRoundKey(state, round, round_keys)
    print(state)
    return state



def aesEncryption():
    """
    PRÉ-RODADA
    1. Ler o texto cifrado
    2. Transformar o texto em uma matrix 4x4 com blocos de 16 byes
    3. Incluir a chave de rodada
    """
    filename = "./texts/plaintext/rumbling-plain.txt"
    file_data = readFile(filename)

    matrix = formatInput(file_data)
    print(matrix)
    key = generateAesKey(128)
    expanded_key = expandKey(key)

    round_keys = roundKeys(expanded_key)

    state = matrix
    for round in range(10):
        state = aesRound(state,round,round_keys)
    

    # Imprime a chave expandida
    """
    RODADA 1-9
    1. Substituir bytes
    2. Deslocar linhas
    3. Embaralhar colunas
    4. Incluir chave de rodada

    
    RODADA 10
    1. Substituir bytes
    2. Deslocar linhas
    3. Incluir chave de rodada
    4. Retornar o texto cifrado
    """
    pass

def aesDecryption(key):
    """
    PRÉ-RODADA
    1. Ler o texto cifrado
    2. Incluir chave de rodada
    
    RODADA 1-9
    1. Inverter linhas deslocadas
    2. Inverter bytes substituídos
    3. Incluir chave de rodada
    4. Inverter colunas embaralhadas

    RODADA 10
    1. Inverter linhas deslocadas
    2. Inverter bytes substituídos
    3. Incluir chave de rodada
    4. Retornar texto decifrado
    """
    pass