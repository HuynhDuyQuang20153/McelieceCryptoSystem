from sklearn.preprocessing import LabelEncoder
import multiprocessing as mp
from mceliececipher import *
from mathutils import *
from compress import *
from df_Excel import *
from excel import *
import numpy as np
from txt import *
import os 


def read(choose):
    try:
        if choose == '2':
            file_name_1 = 'test.txt'
            data_path = os.path.join(os.getcwd(), "..", "data", file_name_1)
            with open(data_path, encoding='utf-8') as f:
                data_line = f.readlines()
                    
            with open(data_path, encoding='utf-8') as f:
                text = f.read()

            data_line = [line.strip() for line in data_line]  
            tokens = [doc.split() for doc in data_line]
            
            label_encoder = LabelEncoder()
            encoder = label_encoder
            label_encoder.fit([token for doc in tokens for token in doc])
            X = [[label_encoder.transform([token])[0] for token in doc] for doc in tokens]

            already_assigned = None 

            check = can_create_matrix(X)
            if check:
                matrix_text = np.array(X)
            else:
                matrix_text, already_assigned = paddingMatrix(X)

            if matrix_text.ndim == 1:
                t = 1
            elif matrix_text.ndim > 1 or len(matrix_text.shape) > 1:
                t = len(matrix_text)

            input_matrix_col = matrix_text.shape[1]
            return text, data_line, matrix_text, already_assigned, t, matrix_text.shape[0], input_matrix_col, encoder

        elif choose == '1':
            file_name_2 = "def.xlsx"
            data_path = os.path.join(os.getcwd(), "..", "data", file_name_2)

            header = list(range(pd.read_excel(data_path).shape[1]))
            df = pd.read_excel(data_path, header=None)
            df.columns = header + df.columns[len(header):].tolist()

            df.fillna('', inplace=True)

            data_line = np.array(df)
            for i in range(len(data_line)):
                for j in range(len(data_line[i])):
                    if isinstance(data_line[i][j], int) or isinstance(data_line[i][j], float):
                        data_line[i][j] = str(data_line[i][j])

            label_encoder = LabelEncoder()
            encoder = label_encoder
            label_encoder.fit([token for doc in data_line for token in doc])

            already_assigned = None 
            text = None

            X = [[label_encoder.transform([token])[0] for token in doc] for doc in data_line]
            max_length = max([len(row) for row in X])
            input = np.zeros((len(X), max_length))
            already_assigned = np.zeros_like(input, dtype=bool)

            for i, row in enumerate(X):
                input[i, :len(row)] = row
                already_assigned[i, :len(row)] = True

            matrix_text = input.astype(int)

            if matrix_text.ndim == 1:
                t = 1
            elif matrix_text.ndim > 1 or len(matrix_text.shape) > 1:
                t = len(matrix_text)

            input_matrix_col = matrix_text.shape[1]
            return text, data_line, matrix_text, already_assigned, t, matrix_text.shape[0], input_matrix_col, encoder

    except Exception as e:
        print("ERROR READ FILE: ", e)


def key(t, k, n):
    try:
        mc = McElieceCipher(t, k, n)
        mc.generate_create_keys()

        private_key = {
            'S': mc.S,
            'G': mc.G,
            'P': mc.G
        } 
        public_key = {
            't': t,
            'Gp': mc.Gp   
        }
        orther = {
            'Gp_col': mc.Gp_col,
            'Gp_row': mc.Gp_row,
            'P_inv': mc.P_inv,
            'S_inv': mc.S_inv    
        }
        return private_key, public_key, orther

    except Exception as e:
        print("ERROR CREATE KEY:", e)


def encrypt(t, k, n, matrix_text, public_key, orther):
    try:
        Gp = public_key['Gp']
        Gp_col = orther['Gp_col']

        mc = McElieceCipher(k, n, t)
        mc.encrypt(matrix_text, Gp, Gp_col, t)

        direc_cipherText = {
            'vector': mc.Cp,
            'e': mc.e,   
            'ciphertext': mc.y
        }
        return direc_cipherText

    except Exception as e:
        print("ERROR ENCRYPT:", e)


def decrypt(k, n, matrix_text, direc_cipherText, public_key, private_key, orther):
    try:
        S = private_key['S']
        t = public_key['t']
        P_inv = orther['P_inv']
        S_inv = orther['S_inv']
        y = direc_cipherText['ciphertext']

        mc = McElieceCipher(k, n, t)
        mc.decrypt(matrix_text, y, P_inv, S_inv, S)

        direc_cipherText = {
            'vector': mc.y_,
            'xS': mc.xS,   
            'plainText': mc.x
        }
        return direc_cipherText


    except Exception as e:
        print("ERROR DECRYPT:", e)


def save_file(choose_type_file, private_key, public_key, direc_cipherText, direc_plaintText, matrix, texts, data_line):
    try:
        print("\n\n\t************************* SAVE MATRIX IN '.XLSX' FILE *************************")
        excel = Excel(private_key, public_key, direc_cipherText, direc_plaintText, matrix)
        excel.Excel_Write()

        print("\n\n\t************************** SAVE MATRIX IN '.NPZ' FILE *************************")
        compress = Compress(private_key, public_key, direc_cipherText, direc_plaintText, matrix)
        compress.Compress_Write()

        if choose_type_file == '1':
            print("\n\n\t*************************** SAVE DATAFRAME IN '.XLSX' FILE *************************")
            df_excel = df_Excel(data_line)
            df_excel.df_Write()

        elif choose_type_file == '2':
            print("\n\n\t*************************** SAVE TEXT IN '.TXT' FILE **************************")
            txt = TXT(data_line, texts)
            txt.TXT_Write()

    except Exception as e:
        print("ERROR SAVE FILE:", e)


def backtext(encoder, already_assigned, plainText):
    try:
        if already_assigned is not None:
            X = []
            for i, row in enumerate(plainText):
                if np.all(already_assigned[i, :len(row)]):
                    X.append(list(row))

                elif not np.all(already_assigned[i, :len(row)]):
                    non_zero = np.nonzero(row)[:len(row)]
                    X.append(list(row[non_zero]))
        
            texts = []
            for doc in X:
                words = encoder.inverse_transform(doc)
                text = " ".join(words)
                texts.append(text)

        else:
            texts = []
            for doc in plainText:
                words = encoder.inverse_transform(doc)
                text = " ".join(words)
                texts.append(text)
    
        text_final = '\n'.join(texts)
        return text_final, texts

    except Exception as e:
        print("ERROR RECOVERY TEXT:", e)


if __name__ == '__main__':
    choose_type_file = input("DO YOU WANT TO INPUT DATA FROM EXCEL OR TXT (1 or 2)? ")

    pool = mp.Pool(processes=4)

    data_ = pool.starmap(read, choose_type_file)
    text, data_line, matrix_text, already_assigned, t, k, n, encoder = get_input_data(data_)

    args_list_tkn = [(t, k, n)]
    key_ = pool.starmap(key, args_list_tkn)
    private_key, public_key, orther = get_key_data(key_)

    args_list_encrypt = [(t, k, n, matrix_text, public_key, orther)]
    enc_ = pool.starmap(encrypt, args_list_encrypt)
    direc_cipherText = get_encrypt_data(enc_)

    args_list_decrypt = [(k, n, matrix_text, direc_cipherText, public_key, private_key, orther)]
    dec_ = pool.starmap(decrypt, args_list_decrypt)
    direc_plaintText = get_decrypt_data(dec_)

    args_list_backtext = [(encoder, already_assigned, direc_plaintText['plainText'])]
    rec_ = pool.starmap(backtext, args_list_backtext)
    text_recovery, texts = get_backtext(rec_)

    pool.close()
    pool.join()

    if np.array_equal(direc_plaintText['plainText'], matrix_text):
        print("\n\n\t****************************************************************************")        
        print("\t*** The decoding result matches the original matrix: Matrix == PlainText ***")
        print("\t****************************************************************************")

        process_save_data = mp.Process(target=save_file, args=(choose_type_file, private_key, public_key, direc_cipherText, direc_plaintText, matrix_text, texts, data_line))
        process_save_data.start()
        process_save_data.join()  

        if choose_type_file == '1':
            print(f"\t- Text: \n", data_line)

        elif choose_type_file == '2':
            print(f"\t- Text: \n", text)

        print(f"\n\t- Text_recovery: \n", text_recovery)

    else:
        print("\t*!*!*! The decoding result does not match the original matrix: Matrix != PlainText *!*!*!")
        print("\t******************************************************************************")
        print("\t- Matrix_text: \n", matrix_text)
        print(f"\n\t- Matrix_plain: \n", direc_plaintText['plainText'])
