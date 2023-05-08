import numpy as np
import os

class Compress:
    def __init__(self, text, data_line, matrix_text, already_assigned, t, k, n, 
                        encoder, private_key, public_key, orther, direc_cipherText, 
                        path_location_save, matrix_output, direc_plaintText, text_recovery, texts):
        self.text = text
        self.data_line = data_line
        self.matrix_text = matrix_text
        self.already_assigned = already_assigned
        self.t = t
        self.k = k
        self.n = n
        self.encoder = encoder
        self.private_key = private_key
        self.public_key = public_key
        self.orther = orther
        self.direc_cipherText = direc_cipherText
        self.path_location_save = path_location_save
        self.matrix_output = matrix_output
        self.direc_plaintText = direc_plaintText
        self.text_recovery = text_recovery
        self.texts = texts


    def Compress_Write(self):
        dir_path = os.path.join(os.getcwd(), "..", "data", "Save_file")
        max_index = 0
        for filename in os.listdir(dir_path):
            if filename.startswith("Save_turn_") and os.path.isdir(os.path.join(dir_path, filename)):
                index = int(filename.split("_")[2])
                if index > max_index:
                    max_index = index

        new_dir_path = os.path.join(dir_path, "Save_turn_" + str(max_index))
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)

        path_cipher = os.path.join(new_dir_path, "Compress")
        if not os.path.exists(path_cipher):
            os.mkdir(path_cipher)




        compress_file = "Compress_All_Data.npz"
        compress_path = os.path.join(path_cipher, compress_file)
        np.savez_compressed(compress_path, text = self.text, data_line = self.data_line, matrix_text = self.matrix_text,
                                already_assigned = self.already_assigned, t = self.t, k = self.k, n = self.n,
                                encoder = self.encoder, private_key = self.private_key, public_key = self.public_key,
                                orther = self.orther, direc_cipherText = self.direc_cipherText, path_location_save = self.path_location_save,
                                matrix_output = self.matrix_output, direc_plaintText = self.direc_plaintText,
                                text_recovery = self.text_recovery, texts = self.texts)

        print(f"\t- Compress all data in: '{compress_path}'\n")

        # data = np.load(compress_path, allow_pickle=True)
        # t = data['t']
        # k = data['k']
        # n = data['n']
        # text = data['text']
        # data_line = data['data_line']
        # matrix_text = data['matrix_text']
        # already_assigned = data['already_assigned']
        # encoder = data['encoder']
        # private_key = data['private_key']
        # public_key = data['public_key']
        # orther = data['orther']
        # direc_cipherText = data['direc_cipherText']
        # path_location_save = data['path_location_save']
        # matrix_output = data['matrix_output']
        # plainText = data['plainText']
        # direc_plaintText = data['direc_plaintText']
        # matrix_text = data['matrix_text']
        # text_recovery = data['text_recovery']
        # texts = data['texts']

        # print(f"\n- File '{compress_file}' vua duoc nen: ")
        # print(f"t: ", t)
        # print(f"k: ", k)
        # print(f"n: ", n)
        # print(f"\text: \n", text)
        # print(f"\data_line: \n", data_line)
        # print(f"\matrix_text: \n", matrix_text)
        # print(f"\already_assigned: \n", already_assigned)
        # print(f"\encoder: \n", encoder)
        # print(f"\private_key: \n", private_key)
        # print(f"\public_key: \n", public_key)
        # print(f"\orther: \n", orther)
        # print(f"\direc_cipherText: \n", direc_cipherText)
        # print(f"\path_location_save: \n", path_location_save)
        # print(f"\matrix_output: \n", matrix_output)
        # print(f"\plainText: \n", plainText)
        # print(f"\direc_plaintText: \n", direc_plaintText)
        # print(f"\matrix_text: \n", matrix_text)
        # print(f"\text_recovery: ", text_recovery)
        # print(f"\texts: \n", texts)