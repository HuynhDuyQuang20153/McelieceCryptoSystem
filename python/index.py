from mceliececipher import *
from mathutils import *
from compress import *
from excel import *
from txt import *
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder


def generate(t, k, n):
    # Create McElieceCipher object and key
    mc = McElieceCipher(t, k, n)
    mc.generate_create_keys()

    # Create a directionary that stores the result 
    private_key = {
        'S': mc.S,
        'P': mc.P,
        'G': mc.G   
    }
    public_key = {
        't': t,
        'Gp': mc.Gp
    }
    orther = {
        'Gp_row': mc.Gp_row,
        'Gp_col': mc.Gp_col,
        'P_inv': mc.P_inv,
        'S_inv': mc.S_inv
    }

    return private_key, public_key, orther


def encrypt(t, k, n, Matrix, public_key, orther):
    Gp = public_key['Gp']
    Gp_col = orther['Gp_col']

    # Create McElieceCipher object
    mc = McElieceCipher(k, n, t)

    # Encrypt matrix
    mc.encrypt(Matrix, Gp, Gp_col, t)

    # Create a directionary that stores the result 
    direc_cipherText = {
        'vector': mc.Cp,
        'error_e': mc.e,
        'ciphertext': mc.y
    }

    return direc_cipherText


def decrypt(k, n, matrix, direc_ma_hoa, public_key, private_key, orther):
    S = private_key['S']
    t = public_key['t']
    P_inv = orther['P_inv']
    S_inv = orther['S_inv']
    y = direc_ma_hoa['ciphertext']

    # Create McElieceCipher object
    mc = McElieceCipher(k, n, t)

    # Decrypt matrix
    mc.decrypt(matrix, y, P_inv, S_inv, S)

    # Create a directionary that stores the result
    direc_plaintText = {
        'vector': mc.y_,
        'xS': mc.xS,
        'plainText': mc.x
    }

    return direc_plaintText


def read_data_file():
    # Create path to local of data 
    data_path = os.path.join(os.getcwd(), "..", "data", "data.txt")
    with open(data_path, encoding='utf-8') as f:
        corpus = f.readlines()

    corpus = [line.strip() for line in corpus]  # Loại bỏ ký tự xuống dòng ở cuối mỗi dòng

    # Split words into tokens
    tokens = [doc.split() for doc in corpus]

    # Use LabelEncoder to convert tokens to unique integers
    label_encoder = LabelEncoder()
    encoder = label_encoder
    label_encoder.fit([token for doc in tokens for token in doc])

    # Representing documents as integer matrices
    X = [[label_encoder.transform([token])[0] for token in doc] for doc in tokens]

    # Convert list to numpy matrix
    input_matrix = np.array(X)

    # Check shape of matrix
    if input_matrix.ndim == 1:
        t = 1

    elif input_matrix.ndim > 1 or len(input_matrix.shape) > 1:
        t = len(input_matrix)

    return corpus, input_matrix, t, input_matrix.shape[0], input_matrix.shape[1], encoder


def save_data(private_key, public_key, orther, direc_cipherText, direc_plaintText, matrix, data, text):
    # Save data into '.xlsx' file
    print("\n\n\t************************* SAVE MATRIX IN '.XLSX' FILE *************************")
    excel = Excel(private_key, public_key, orther, direc_cipherText, direc_plaintText, matrix)
    excel.Excel_Write()


    # Save data into '.npz' file
    print("\n\n\t************************** SAVE MATRIX IN '.NPZ' FILE *************************")
    compress = Compress(private_key, public_key, orther, direc_cipherText, direc_plaintText, matrix)
    compress.Compress_Write()


    # Save data into '.txt' file
    print("\n\n\t*************************** SAVE TEXT IN '.TXT' FILE *************************")
    txt = TXT(data, text)
    txt.TXT_Write()


def back_text(encoder, plainText):
    # Convert the matrix back to a list of documents
    texts = []
    for doc in plainText:
        words = encoder.inverse_transform(doc)
        text = " ".join(words)
        texts.append(text)
    return texts


if __name__ == '__main__':
    # Read data file
    data, matrix, t, k, n, encoder = read_data_file()


    # Step 1: Key formation process
    private_key, public_key, orther = generate(t, k, n)


    # Step 2: Encryption process
    direc_cipherText = encrypt(t, k, n, matrix, public_key, orther)


    # Step 3: Decryption process
    direc_plaintText = decrypt(k, n, matrix, direc_cipherText, public_key, private_key, orther)


    # Compare the original matrix with the plaintext
    print("\n\n\t****************************************************************************")
    if np.array_equal(direc_plaintText['plainText'], matrix):
        print("\t*** The decoding result matches the original matrix: Matrix == PlainText ***")
        print("\t****************************************************************************")

        # Text recovery
        # text = back_text(direc_plaintText['plainText'], vectorizer)
        text = back_text(encoder, direc_plaintText['plainText'])

        # Save data into 'xlsx' file, 'txt' file and '.npz' file
        save_data(private_key, public_key, orther, direc_cipherText, direc_plaintText, matrix, data, text)

        print("\n\n\t****************************************************************************")
        print(f"\t\t- Original data: \n", data)
        print(f"\t- Original matrix: \n", matrix)
        print(f"\t- PlainText: \n", direc_plaintText['plainText'])
        print(f"\t\t- Text: \n", text)

    else:
        print("\t*!*!*! The decoding result does not match the original matrix: Matrix != PlainText *!*!*!")
        print("\t****************************************************************************")
        print(f"\t- Original matrix: \n", matrix)
        print(f"\t- PlainText: \n", direc_plaintText['plainText'])