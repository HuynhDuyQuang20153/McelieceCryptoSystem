from sklearn.preprocessing import LabelEncoder
import multiprocessing as mp
from mceliececipher import *
from excel_output import *
from excel_input import *
from mathutils import *
from compress import *
import numpy as np
import joblib
import os 


def read_output(choose, path_save):
    try:
        if choose == '2':
            with open(path_save, encoding='utf-8') as f:
                read_output = f.readlines()

            read_output = [line.strip() for line in read_output]  
            return read_output

        elif choose == '1':
            header = list(range(pd.read_excel(path_save).shape[1]))
            df = pd.read_excel(path_save, header=None)
            df.columns = header + df.columns[len(header):].tolist()

            data = np.array(df)
            return data

    except Exception as e:
        print("ERROR READ OUTPUT FILE: ", e)


def read_input(choose):
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
            file_name_1 = "text_2.xlsx"
            data_path = os.path.join(os.getcwd(), "..", "data", file_name_1)

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
        print("ERROR READ INPUT FILE: ", e)


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


def decrypt(k, n, matrix_text, matrix_output, public_key, private_key, orther):
    try:
        S = private_key['S']
        t = public_key['t']
        P_inv = orther['P_inv']
        S_inv = orther['S_inv']
        y = matrix_output

        mc = McElieceCipher(k, n, t)
        mc.decrypt(matrix_text, y, P_inv, S_inv, S)

        direc_plaintText = {
            'vector': mc.y_,
            'xS': mc.xS,   
            'plainText': mc.x
        }
        return direc_plaintText


    except Exception as e:
        print("ERROR DECRYPT:", e)


def save_cipher_file(choose_type_file, already_assigned, encoder, t, k, n, orther, private_key, direc_cipherText, data_line):
    try:
        print("\n\n\t************************* SAVE DATA CIPHER *************************")
        excel = Excel_input(choose_type_file, already_assigned, encoder, t, k, n, orther, private_key, direc_cipherText, data_line)
        excel.Excel_Write_input()
        return excel.path_location_save

    except Exception as e:
        print("ERROR SAVE DATA CIPHER:", e)


def save_plain_file(choose_type_file, already_assigned, encoder, texts, path_location_save, data_line):
    try:
        print("\n\n\t***************************** SAVE DATA PLAIN ******************************")
        excel = Excel_output(choose_type_file, already_assigned, encoder, texts, path_location_save, data_line)
        excel.Excel_Write_output()

    except Exception as e:
        print("ERROR SAVE DATA PLAIN:", e)


def save_compress_file(text, data_line, matrix_text, already_assigned, t, k, n, 
                        encoder, private_key, public_key, orther, direc_cipherText, 
                        path_location_save, matrix_output, direc_plaintText, text_recovery, texts):
    try:
        print("\n\n\t***************************** SAVE COMPRESS DATA ***************************")
        compress = Compress(text, data_line, matrix_text, already_assigned, t, k, n, 
                            encoder, private_key, public_key, orther, direc_cipherText, 
                            path_location_save, matrix_output, direc_plaintText, text_recovery, texts)
        compress.Compress_Write()

    except Exception as e:
        print("ERROR SAVE DATA COMPRESS:", e)

def backtext(already_assigned, direc_plaintText):
    try:
        plainText = direc_plaintText['plainText']
        dir_path = os.path.join(os.getcwd(), "..", "data", "Save_file")
        max_index = 0
        for filename in os.listdir(dir_path):
            if filename.startswith("Save_turn_") and os.path.isdir(os.path.join(dir_path, filename)):
                index = int(filename.split("_")[2])
                if index > max_index:
                    max_index = index
        new_dir_path = os.path.join(dir_path, "Save_turn_" + str(max_index))
        encoder = joblib.load(os.path.join(new_dir_path, "CipherText", "encoder.joblib"))

        if already_assigned is not None:
            X = []
            for i, row in enumerate(plainText):
                if np.all(already_assigned[i, :len(row)]):
                    X.append(list(row))

                elif not np.all(already_assigned[i, :len(row)]):
                    positive_indices = np.where(row >= 0)[0][:len(row)]
                    X.append(list(row[positive_indices]))

            for i in range(len(X)):
                for j in range(len(X[i])):
                    X[i][j] = int(X[i][j])

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
    choose_input = input("- UPLOAD DATA FILE (y or n)? ")

    if choose_input == 'y':
        choose_type_file = input("- DO YOU WANT TO INPUT DATA FROM EXCEL OR TXT (1 or 2)? ")

        text, data_line, matrix_text, already_assigned, t, k, n, encoder = read_input(choose_type_file)
        private_key, public_key, orther = key(t, k, n)
        direc_cipherText = encrypt(t, k, n, matrix_text, public_key, orther)
        path_location_save = save_cipher_file(choose_type_file, already_assigned, encoder, t, k, n, orther, private_key, direc_cipherText, data_line)

        choose_input_2 = input("\n\n\n- DO YOU WANT TO UPLOAD CIPHER FILE TOO (y or n)? ")

        if choose_input_2 == 'n':
            print("\t\t---> EXIT PROGRAM !!!")

        elif choose_input_2 == 'y':
            matrix_output = read_output(choose_type_file, path_location_save)
            direc_plaintText = decrypt(k, n, matrix_text, matrix_output, public_key, private_key, orther)

            if np.array_equal(direc_plaintText['plainText'], matrix_text):
                print("\n\n\t****************************************************************************")        
                print("\t*** The decoding result matches the original matrix: Matrix == PlainText ***")
                print("\t****************************************************************************")

                text_recovery, texts = backtext(already_assigned, direc_plaintText)
                save_plain_file(choose_type_file, already_assigned, encoder, texts, path_location_save, data_line)
                save_compress_file(text, data_line, matrix_text, already_assigned, t, k, n, 
                        encoder, private_key, public_key, orther, direc_cipherText, 
                        path_location_save, matrix_output, direc_plaintText, text_recovery, texts)

            else:
                print("\n\n\t****************************************************************************")        
                print("\t*** The decoding result does not match the original matrix: Matrix != PlainText ***")
                print("\t******************************************************************************")

    if choose_input == 'n':
        print("\t\t---> EXIT PROGRAM !!!")

